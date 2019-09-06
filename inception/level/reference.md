# Level references
Level uses references to represent a memory location of data structures and objects. Level references are safe. We can''t do reference arithmetics and can''t have direct memory access ulike C. 

Most operators are referring to value represented by the reference and not to the reference address. We can''t print the address represented by a reference only it''s data string representation. 

## Punctuation
When we declare a variable we know is a reference from it''s type. If the type starting with uppercase letter then is a reference. Native types are starting with lowercase letters. 

```
procedure test:
  x   : integer; --define a native type
  p,m : Integer; --define two references
execute
  x = 10;  --set variable x to constant literal 10
  p = x;   --bound reference "p" to variable x
  p = 11;  --modify underline variable x to 11
  p += 10;  --modify underline variable x = 11 + 10 = 22
  print(s) ;--expect 22
procedure; 
```

## Reference type
We can have references to all types including user defined types. However references have a fixed size in memory and it''s 8 bytes. Level is working only on 64 bit operating systems not 32 bit.

References contain information about data type, data size and reference count. When reference count is 0 then the memory location can be erased to be re-used by new references. 


## Primary usage
The assign operator "=" works "_by value_" for native types and "_by reference_" for references obviously. If the variable we assign to is _Null_ and there is no other reference to same location then the data is lost.

For composite types and classes: {Array, Matrix, Hash, Set, Queue, Stack, String, Unicode, Text} the assign operator "=" works _by reference_ avoidning large data movements. This makes Level an efficient language.

When we copy references the memory location is _shared_. We can use "?=" operator to check if two references are sharing the same address. Operator "==" first verify the address then verify the attributes but only if the address is not the same to improve performance. 

## Reference counting
A native variable has an address in memory that can change. Level has a symbol table that contains information about each variable type, location and reference count. Therefore Level can use introspection to find information about variables.

We can _share_ the memory location using one or more references. Every time when a share event take place the reference count is incremented with one. A reference to reference can''t exist. All references point to the original location. 

When a reference go out of scope the reference count is decremented with one. When _reference count_ is zero the memory can be free. Local variables that are using a prefix: @ are permanent. For these variables we do not free memory after variable is out of scope. 

## Mutability
We use modifiers {"+=, -=, /=, *=, %=, ^="} to change reference underline value. If the reference is not initialized and is Null it can''t be modified and is an error. 

Operator "=" and ":>" initialize a variable reference to a new memory location. If is already initialized then the original location becomes "garbage" and will be removed from memory.

## Reference Comparison
To check if two references are the same we use "?=" and "!=". If two references point to the same location and have the same type then also have the same value so they are equal. When the location is different the data content is not compared.

## Data Comparison
Symbol "==" and "<>" will compare data and not the location of data. This is a requirement for making a readable program and avoid any confusion about fundamental role of relation operators. These operators work for references but also for native types.


**Example of relation**
```
let
   p=10 :integer;
   c,d:Integer;   
do
  c = p;  -- borrow address of p
  d = 10; -- new reference
    
  print (c ?= p); -- True
  print (c ?= d); -- False
  
  -- data comparison
  if c == d then 
    print("same value"); 
  end if;
end do;
```

## Use Cases
In Level there are 3 use-cases for references:
 
1. We can use references as input/output parameters in procedures and functions.
1. We can declare complex composite types that have as members references to other types;
1. We can use references to transmit data to subroutines created with other languages;
1. We can "box" a native type to it''s reference data type.
1. We can "un-box" a reference type to it''s native data type.

**Example:**
```
-- this is simple example of reference usage
procedure main:
  v_int=100 :integer; --variable is initialized
  p_int     :Integer; --not initialized (void reference)
  o_ind=100 :Integer; --initialized with a literal (original)
execute
  p_int = v_int; --borrowing address of v_int
  print(“the value of p_int is: ” + p_int); --> 100
  p_int = p_int + 10;
  print(“the value of p_int is: ” + p_int); --> 110
  print(“the value of v_int is: ” + v_int); --> 110
procedure;
```

## In/Out Parameters
References can be useful to create input/output parameters. 

**Example:** 
```
-- local procedure
procedure add_numbers(p1, p2 :integer, p_result :Integer):
execute
  p_result = p1+p2; -- modify the parameter value
procedure;

procedure main:
  v_result=10 :Integer;
execute
  add_numbers(10, 20, v_result);
  print(v_result); --> New value is 40
procedure;
```

## Null references
Programs are not permitted to access memory at address 0 because that memory is reserved by the operating system. This represents _null reference_. Null references can''t be used until they have a valid memory address.

In Level Null references are void. We can use "is" operator to check if a reference "is Null" or "is not Null". "Null" is a data type. This operator check also other data types: "is Integer", "is Real" and so on. 

**Example of Null reference:**
```
---------------------------------------------------------
-- this is simple example of deferred array  initialization 
---------------------------------------------------------
procedure test():
  @result: Array of Integer;
execute
  if @result is Null then
     @result = Array(10);
  end if;
  print(result);  
procedure;
```
=\> [0,0,0,0,0,0,0,0,0,0]

## Null & Empty versus Zero Value

Level define a zero value for numeric data types. In Level all native variables are automatically initialized to zero or Empty. Objects are Null until initialization operator "=" or "=" is used.

Empty and Null are two polimorphic data types.

**Default Zero Values:**
* Zero number is: 0
* Empty string is: "" 
* Empty tuple  is: () 
* Empty array  is: [] 
* Empty matrix is: []
* Empty set    is: {}

## Introspection Proposal

We can use "is" operator to check "status" of any variable not only references: 
```
let
   p=1,d:Integer; -- p is owner
   c    :Integer; -- reference
   v=1  :Integer; -- not a reference
do
   -- check the status
   print(p is Null);  --False
   print(d is Null);  --True

   c = p -- borrowing
   
   -- relation operators for references
   print(c ?= p); --> True (same location)
   print(p ?= c); --> True (same location)   
   print(p ?= v); --> False (different location)
   print(p == v); --> True (different location but same value)
end do;
```

## Member initialization
Composite variables and members must be initialized separately. It is possible one composite variable to be initialized but it''s members are not. Later we can initialize all members using a loop. Native type members are initialized automatically. Composite type members must be initialized in the executable region of a section.
