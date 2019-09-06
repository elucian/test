# Level references
In Level language a reference is a reference to a memory location. Like any other variable, you must declare a reference before using it. references are useful to create input/output parameters, collections of records and recursive records.

## Safe references
Unlike C references, Level references are safe. We can''t do reference arithmetic and can''t have direct memory access. All math operators are referring to value represented by the reference and not to the reference address. We can''t even print the address represented by a reference. When we print we will print the underling variable not the reference.

## Punctuation
The general form of a reference declaration is using "at" symbol "@". We have chosen this symbol to suggest the memory address location. Using references with @type we can define _"reference"_ variables. We can use unary operator ? to extract address of a variable:

```
procedure test is
global
  n: Integer;
  p: @Integer; --define a reference to Integer global
execute
  p = n;   --transfer address of "n" to "p" (p is not initialized)
  p = n;   --allocate new memory then transfer value of n into p
  p = 10;  --create new reference modify the "n" variable from 0 to 10
  print(n); --n has value 10
procedure; 
```

## reference type
A reference has a static type. We can have references to all types including user defined types. However references have a fixed size in memory and it''s 8 bytes. Level is working only on 64 bit operating systems and we do not support 32 bit os.

## Primary usage
Normally the assign operator "=" works "_by value_".  It make a clone of the original value. If the variable we assign to is _void_ then a new memory location is establish. By using references we can transmit value "_by reference_".

For composite types: {Array, Matrix, Record, Tuple, String} the assign operator "=" can create large _"data movement"_ that can be avoided by using references. This is the primary usage of references.

When we use references to {@Array, @Matrix, @Record, @Tuple, @String} The memory location is _shared_ using "?=" operator that is "address of". This will transfer the address of variable to reference and will not make a copy. 

## Reference counting
When we create a new memory location the variable we create is called "owner". A native variable is initialized automatically with zero value and is the "owner" of it''s address. For composite types we use "=" to initialize a new address location and create a new "owner".

We can _share_ the _"owner"_ location with one or more references. Every time when a share event take place using "?" the _"owner"_ reference count is incremented with one. A reference can re-share the reference using the same operator. 

When a reference go out of scope the _"owner"_ reference count is decremented with one. The _"owner"_ can''t go out of scope until the _reference count_ is zero. This verification is done during compilation time.

Reference count is a compile time property attached to "owner". It is incremented and decremented every time an assignment is performed between two variables using operator "?=". If operator "-" is used the reference count is not incremented.
 
## Initialization
When we define a reference (reference) this is not initialized. It points to zero (is void). A reference can receive value with two methods: We can allocate new memory for it using "=" like any other variable or We can use "?=" to "borrow" location from another variable that can be "owner" or "share". 

## Modifiers
In-place operators or modifiers: "=", "+=, -=, /=, *=, %=, ^=" do not change a reference but the value. Operator "=" will change the value stored where the reference points to. Operator "?=" can _"borrow"_ location from another variable.

## Mutability
We use "=" or other modifier to change value. If the reference is not initialized and is void, a new location is created and the reference becomes the _original_. If variable already point to a location the underlined value is modified in place. 

## Sage programming
Level do not have a garbage collector. Rebinding operations could create garbage. To avoid it cleanup must be done immediately. First we update all the sharing references and then we free the memory. Memory cleanup can be done when a wrapping section go out of scope.

## Programming example
Next program show a bad usage of extend(). This can copy a lot of data to a new location, therefore leaving behind garbage. To avoid the garbage we free the previous memory but this takes time, therefore the program is slow. We can avoid this making a better memory allocation of Matrix outside of the loop.
```
procedure main:
  a: Matrix(0) of Integer; -- initialized empty matrix (not a reference)
  b: Matrix of Integer;    -- not initialized matrix (not a reference)
execute
  for i in (0..999) loop
    a.extend(1000); --add a new row
    for j in (0..999) loop
      a[i,j] = j; --set value for new member
    loop;
    print(a[999,999]); --last element
  loop;  -- we have a lot of garbage associated with a
  b = a;     -- make a copy of a, b is initialized using "=" 
  print(b);
procedure;
```
## Relation Operators
Symbol "==" and "<>" work for basic types, collections and references. This is a requirement for making a readable program and avoid any confusion about fundamental role of relation operators. If we wish to know if two references have same location we use same() built-in function. 

## Comparing references
To check if two references are equal we use "==" and "<>". This has significance "equal" and "not equal". If two references point to the same location and have the same type then also have the same value so they are equal. If location is divergent the underlying content become relevant and a deep comparison is performed to check if the variables are equal.

**Example of relation**
```
let
   p=10 :Integer;
   c:@Integer;   
do
  c ?= p; --borrow address
  if c == p then --> this is true
    print("equal"); 
  else
    print("not equal");
  end if;   
end do;
```
: equal

## reference Use Cases
In Level there are 3 use-cases for references:
 
1. We can use references as input/output parameters in procedures and functions.
1. We can declare complex composite types that have as members references to other types;
1. We can use references to transmit data to subroutines created with other languages;

**Example:**
```
-- this is simple example of reference usage
procedure main:
  v_int=100 :Integer;  --variable is initialized
  p_int     :@Integer; --not initialized (void reference)
  o_ind=100 :@Integer; --initialized with a literal (original)
execute
  p_int ?= v_int; --borrowing address of v_int (p_int is a share)
  print(“the value of p_int is ” & p_int); --> 100
  p_int= p_int + 10;
  print(“the value of p_int is ” & p_int); --> 110
  print(“the value of v_int is ” & v_int); --> 110
procedure;
```

## In/Out Parameters
references can be useful to create input/output parameters. By using a reference/reference we can avoid this data movement making the call faster. Composite types can take a long time to copy from heap to stack for normal parameters. 

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
  add_numbers(10, 20, ?v_result);
  print(v_result); --> New value is 40
procedure;
```

## Null references
Programs are not permitted to access memory at address 0 because that memory is reserved by the operating system. In C and C++ the memory address 0 signals a _null reference_. Null references can''t be used until they have a valid memory address.

In Level Null references are void. We can use "is" operator to check if a reference "is void" or "is not void". This operator is a polymorphic. It can check also: "is empty", "is full", "is null", "is owner", "is share". 

**Example of void reference:**
```
---------------------------------------------------------
-- this is simple example of deferred array  initialization 
---------------------------------------------------------
function reference_example(p_dim:Integer) : Array of Integer is
execute
  if result is void then
     result = Array(p_dim); --dynamic initialization
  end if;
  print(result);  
function;
```
=\> [0,1,2,3,4,5,6,7,8,9]

## Zero Values versus Null
Level define a zero value for every data types. This is different from void. To verify if a reference is empty we use is _is empty_ or "==" operator. An integer _is empty_ if contains 0 value. A string is empty if contains ''. A reference that _is void_ will fail if we try to check _is empty_.

This expression "==" or any other operator will fail for _void_ references. A void reference cannot be verified if is empty and can''t be used in expressions until initialized. We must use "is void" to avoid using void references in expressions.

**Default Zero Values (empty literals):**
* Empty number is: 0
* Empty string is: "" 
* Empty tuple  is: () 
* Empty record is: ()
* Empty array  is: [] 
* Empty matrix is: []

## Introspection Proposal

We can use "is" operator to check "status" of any variable not only references: 
```
let
   p=1,d:@Integer; -- p is owner
   c    :@Integer; -- reference
   v=1  :Integer;  -- not a reference
do
   c ?= p -- borrowing
   -- check the status
   print(p is void);  --false
   print(d is void);  --true
   print(p is owner); --true
   print(p is share); --false
   print(v is share); --false

   -- relation operators for references
   print(c == p); --> true (same location)
   print(p == c); --> true (same location)   
   print(p == v); --> true (different location but same value)
end do;
```

## Composite Types
Level language has capability to define composite types that are also known as collections. These types will be defined later. Is important to know that composite types can use references to other composite types. This can create complex in memory structures.

## Member initialization
Composite variables and members must be initialized separately. It is possible one composite variable to be initialized but it''s members are not. Later we can initialize all members using a loop. Native type members are initialized automatically. Composite type members must be initialized in the executable region of a section.
