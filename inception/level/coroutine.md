Co-routines are subroutines designed for multitasking. 
They allows multiple entry points for suspending and resuming execution. 
A typical design pattern for coroutines is producer-consumer executed in multi-thread mode.

## Multi-tread producer-consumer
To communicate a producer and consumer uses a _queue_ that is a List with capacity. 
This is the communication channel between coroutines. When the list is full the producer is waiting, 
until consumer give signal to continue. When a consumer find queue empty will wait for producer. 
If producer give the signal but the queue is still empty then the consumer stop execution.

```
{* This is a producer-consumer program example *}
-----------------------------------------------
-- declare producer co-routine
-----------------------------------------------
procedure produce(q: List):
  item:0 Integer;
begin
  loop
    when q.full exit;
    -- create some new items
    item = random(100);
    q.enqueue(item);
    yield to consume;
  end loop;
end procedure;
-----------------------------------------------
-- declare consumer co-routine
-----------------------------------------------
procedure consume(q: List): 
begin  
  loop
    when q is empty exit;
    -- remove some items from q
    item = q.dequeue();
    -- use the item                 
    yield to produce;
  end loop;
end procedure;
-----------------------------------------------
-- Implement main program
-----------------------------------------------
procedure main:
  queue: List(10) of Integer; -- communication channel
begin
  job
    -- produce in parallel on 2 threads
    produce(queue); 
    produce(queue); 
    -- consume in parallel on 8 threads
    for i in [1..8] loop
      consume(queue); 
    end loop;
  end job;
end procedure;
```

**Note:** The program do not end until all consumers are finishing. 
The "rest" statement is required only when we need to create a synchronization point after a multi-threaded job. 
If we do not use _rest_ the program just continue it''s own execution.