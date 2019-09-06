# Job section

A job is an _unnamed section_ that can execute procedures in parallel. Job section is used to improve performance. 

**Syntax:**
```
[with]
  <local_declarations>;
job
  <procedure_name>(<parameters>);
end job;
```

## Local scope
We can specify _let_ to create a local scope for the job. 
We may use this to define local variables that are not available after job is finishing. 
Here we can define communication channels that can be used as input output parameters in procedure call.

## Threads
Number of threads can be specified using [N >= 0]. This will specify how many core processors to use. 
We can use N=0 then the job will use all available cores. If we do not specify the number of threads default is [N=1]. 
In this mode each procedure will start when previous procedure has finished. 

## Usage:
We can start the same procedure several times using a loop. 
In the loop we can use different arguments for each call. 
When the number of threads is full the loop will automatically halt until one thread become available.

**Running one procedure in parallel**

Let''s consider procedure test();

```
job 
  for i in (1..20) loop
    test(); --> start 20 threads
  loop;
end job; 
```

** Running 4 procedures in parallel **
```
job
  procedure1();  
  procedure2();  
  procedure3();  
  procedure4();  
end job; 
-- continue when all threads are finished
```

**Using limited number of threads**
To reduce number of threads we can use _rest_ keyword. This will create a synchronization point inside the job.

```
job
  for i in (1..1000) loop
    for j in (1..10) loop
      test(i,j);
    loop;
    rest;
  loop; 
end job;
```
Equivalent to:
```
for i in (1..1000) loop
  job
    for j in (1..10) loop
      test(i,j);
    loop;
  end job;
loop; 
```

## [Critical section](https://en.wikipedia.org/wiki/Critical_section)
In concurrent programming, concurrent accesses to shared resources can lead to unexpected or erroneous behavior, 
so parts of the program where the shared resource is accessed are protected. 
This protected section is the critical section or critical region. 
It cannot be executed by more than one process at a time. 

## Race Condition
A race condition is a flaw that occurs when the timing or ordering of events affects a program’s correctness. 
This is a defect that can be introduced by using parallel programming.

## Data Races
A data race occurs when: two or more threads access the same memory location, and at least one of the accesses is for writing, and the threads are not using any exclusive locks to control their accesses to that memory. 

## Data channels
To avoid data races, for communication between threads we must use _dynamic collections_: 
{List, Map, Set} that are designed to be trade safe. 
We do not use Arrays, Matrices, Strings or Unicode that are not trade-safe. 
We can use non trade-safe variables only for read not for write. 

## Lock & Mutex
In computer science, a lock or mutex (from mutual exclusion) is a synchronization mechanism 
for enforcing limits on access to a resource in an environment where there are many threads of execution. 

## [Semaphore](https://en.wikipedia.org/wiki/Semaphore_(programming))
In computer science, a semaphore is a variable or abstract data type used to control access 
to a common resource by multiple processes in a concurrent system such as a multitasking operating system. 

## [Producer-consumer](https://en.wikipedia.org/wiki/Producer%E2%80%93consumer_problem)
In the producer–consumer problem, one process (the producer) generates data items 
and another process (the consumer) receives and uses them. 
They communicate using a queue of maximum size N and are subject to the following conditions:

    1.the consumer must wait for the producer to produce something if the queue is empty;
    2.the producer must wait for the consumer to consume something if the queue is full.

This pattern should be implemented using coroutines. 
We can also use a generator as producer and one procedure that start several times for consumer. 
Each consumer can ask for next value from generator until the generator have nothing to give and return 0 or -1. 

## Work Planning
Other solution to create a parallel program is to create a _work plan_ using a queue. 
We populate the queue with records for entire work. The producer run a single time and prepare the work by filling in the queue. 
Then we use a job to start several revolvers. 
Each resolver is a procedure that can extract one record from the queue and execute the work. 
When the queue is empty the work is done. For this pattern we can use a dynamic queue with infinite capacity.

**See also:**{
[coroutine](coroutine.md), 
[generator](generator.md)}