## Functional Programming

Functional programming significant features:

**Functions ...*

* can create other functions;
* can receive functions as parameters;
* can behave like objects with attributes;

## Reference to function

A function is a reference of type F.

**syntax:**
```
new <reference_name> :F;
```

**Example:**
```
f(x,y : Z):Z => (x + y);

new g :F;   -- define a reference
let g :f;   -- create a reference to function
put g(1,2); -- using a reference as a function
```

## Closure

It is a _higher order_ function that create or enclose other functions. 

**usability**
A closure is used to simulate object oriented programming.

## Coroutine

A coroutine is a resumable function that is suspended and yield for other function.

**demo:** [ho.wee](../demo/ho.wee)
