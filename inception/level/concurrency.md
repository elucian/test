## Concurrency

Wee is designed for high performance computing and massive parallelization.

**features:**

* asynchronous call
* resumable coroutines 


## Asynchronous call

One or more methods can be run in parallel if the call is asynchronous.

keyword | description
--------|---------------------------------------------------------------
run     | start a procedure asynchronously and create new thread
rest    | temporary stop main thread and wait for synchronization
wait    | suspend for specific number of seconds, milliseconds


**pattern**

Usually asynchronous call is done from a control loop.

```
let i = 0; -- control variable

-- suspend for 2.5 sec
test() 
  wait 2.5;
test

-- start 4 threads
cycle
  run test;    
  let i = i + 1;    
  stop if x > 4;
cycle;
rest;
```

example: [ac.wee](../demo/ac.wee)

## Resumable Coroutines 

Coroutines are two methods that wait for each other to execute in turn.

* coroutines can be executed on multiple threads
* coroutines can be used in producer/consumer paradigm

keyword | description
--------|---------------------------------------------------------------
yield   | interrupting current thread and give priority to other thread


**design pattern**

```
#driver

let n ∈ N; -- control variable

-- first coroutine
foo(x ∈ N)
  let x = x + 1;
  wait 5;  
  yield bar if x < 10;
foo;
-- second coroutine
bar(x ∈ N) 
  let x = x + 1;
  wait 10;    
  yield foo if x < 10;
bar;
-- call foo and bar asynchronously
run foo(n);
run bar(n);
-- wait for both foo and bar to finish
rest;

over;
``` 

example: [pp.wee](../demo/pp.wee)
