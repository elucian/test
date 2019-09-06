## Active expression

An expression is active if it modifies a variable. An active expression has a logic result: $0 or $1. The result can be captured using assignment ":=" or it can be used in a conditional.

**syntax**
```
  <variable_name> <op> <mutating_expression>;
```

Where: <op> can be any [modifier operator](operators.md#arithmetic-modifiers).

**examples**
```
new a := 0;
-- active conditional
when a += 1:
   put a; -- expect 1
when;

-- protect zero division
new b ε L;
let b := (a := 1/0); -- not failing
put b ; -- expected $0 (false)
put a := 1; (unmodified)
```