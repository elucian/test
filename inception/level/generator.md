# Generator Function
A generator is a special kind of function that do not terminate immediate after call. 
Instead it’s instance is preserved in memory is a suspended state. 
A generator is a <em>"producer function"</em> that can create results on demand.

## Iteration
A generator is iterable and can be used in _for loop_ statement.

Available built-in methods:
* next;
* current;
* end;
* capacity;

**Example:**
```
-- This module demonstrate a generator
function generator(p_stop:Integer) => Integer:
  loop
    stop if result > p_stop;
    yield;
    result +=1;
  loop;
function;

procedure main:
  index Function;
  -- example 1 generator:"aindex"
  print("call generator using for");
  given
     index=generator(3);
  for i in index do
      output("i=#" <+ i);
  for;
    
  -- example 2 generator:"bindex"     
  print("call generator using loop");
  given
    i=0:Integer;  
    index=generator(3);
  loop
    i= index.next
    output("y=#" <+ i);
    stop if index.end;
  loop;
  print("done.");
procedure;
```
This will print:

```
call generator using for
i=0, i=1, i=2, i=3,

call generator using loop
i=0, i=1, i=2, i=3, 
done.
```

### generator()
This is a function that will persist in memory and wait for next() to be invoked. When the last element is generated the function terminate. A generator function is a “high order function” and must be instantiated with a parameter.

### index generator
I have created and recreated one generator named "index" using the same function test(). First generator is used into a for loop like an iterable collection. Not all values are generated in memory but one by one. This is very efficient.

For second generator I have used next(index) to create all values until finish(index) return true. Every time next() is invoked a new value is created until all values are printed.

## Keyword yield
Keyword _"yield"_ is specific to generators and coroutines. This keyword will suspend execution and give control to main program. The execution is resumed using next. When next() is invoked the program continue with statement after _yield_.
