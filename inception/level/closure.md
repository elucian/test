## Closure

A closure is a dynamic function that is created by another function. 
By using closures we can create stochastic functions that can return a different result for every call. 
This is advanced functionality that is typical to functional languages.

**Syntax:**
```
function <name>() => Function:
begin
  return function() => <type>:
  begin
   pass;
  end function;
end function;
```
## Context
Closure is an encapsulated object in memory. The outer scope of enclosed function 
must remain available and is not removed from memory as long as the inner function has active references. 
When all the active references are out of scope then the closure context is removed from memory.

**Example:**

```
-- higher order function: factory
function factory(min, max: Integer) => Function:
  m:Integer;
begin
  m=min;-- transfer "min" to context
  -- create closure as result
  return function()=> Integer:
    result:Integer;
  begin
    if m > max then
      result = 0; 
    else
      result = m; --> return current m
    end if;
    m+=1; --> increment m in context
    return result; 
  end function;  
end function;

procedure main(s:String, a,b:Integer, c,d:Real):
  closure: Function;
begin -- main
  -- first test case
  closure=factory(1,10);
  let
    test:Integer;
  loop
    when test==0 then exit;
    test = closure();
    print(test);   -- will print from 1 to 10
  end loop;
  -- second test case
  closure=factory(100,105); 
  let
    test:Integer; -- function result    
  loop
    when test==0 then exit;
    test=closure();
    print(test);   -- will print from 100 to 105
  end loop;  
end procedure;

run main;
```