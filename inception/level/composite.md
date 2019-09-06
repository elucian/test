## Composite Types

Composite types are complex data structure in memory. 
We can use composite types to declare variables, constants or other composite types.

## String composite type "S"

* S strings are _tries_ data structures (radix tree) having unlimited capacity;
* A can be used to create arrays of ASCII characters compatible with C strings; 

```
new str ∈  S;      --Unlimited capacity string
new a   = [A](25); --array of 25 characters

let str = "Long string";
let a   = split(str);
```

## String conversion
Conversion of a string into number is done using _parse_ function:

```
new x,y ∈ R;

-- function parse return a Real number
let x = parse("123.5",2,",.");       --convert to real 123.5
let y = parse("10,000.3333",2,",."); --convert to real 10000.33
```

## Control codes:

Wee support escape notation using escape `\` symbol.
For each escape character Wee also define a constant CODE.

**escape characters**

DEC|HEX|CODE|ESCAPE|NAME
---|---|----|------|---------
0  |00 |NUL |\0    |Null
7  |07 |BEL |\a    |Bell
8  |08 |BS  |\b    |Backspace
9  |09 |HT  |\t    |Horizontal Tab
10 |0A |LF  |\n    |Line Feed
11 |0B |VT  |\v    |Vertical Tab
12 |0C |FF  |\f    |Form Feed
13 |0D |CR  |\r    |Carriage Return
27 |1B |ESC |\e    |Escape

**Note:** Escape characters are recognized in strings.

```
say("this represents \n new line in string")
```

## Unicode string

Default Unicode character set is UTF8. This has variable size: (1..4) Bytes.

```
new s = "This is a Unicode string"
say type(s)-- Print: S
```

**Note:** String literal "" is an empty string.

See also: https://utf8everywhere.org/

## String concatenation

Strings can be concatenated using operator "." or "+".

```
new u, c ∈ S;

-- string concatenation
let u = "This is" + " a long string.";
let c = "Unicode and"+_+"ASCII";

-- path concatenation
new test_file = $pro."src"."test.wee";

-- when $pro = c:\work\project\
say test_file; 
write; --> "c:\work\project\src\test.wee"
```

**Note:** Anonymous variable "_" is actually a constant equal to " " all the time.

Using "." will insert "\\" or "/" depending on the operating system.

## String format

We can include numbers into a string using template operator "<+" or "+>".
Inside template we use "{n}" notation to find a value using the member index.

**Template:**
```
new <variable> = <template> <+ <variable>;
new <variable> = <template> <+ (<var1>,[<var2>,]...);
```

**Examples:**
```
new x = 30; -- Code ASCII 0
new y = 41; -- Code ASCII A

--template writing
say ("{0} > {1}" <+ (x,y)); --print "30 > 41"
  
```
## String Generator

It is common to create strings automatically.

**Operator: Repeat = "↻"** 

```
new str = <constant> ↻ n;
```

**Example:**
```
new sep = "+" + ("-" ↻ 18) + "+";

say sep ;
say "|*  this is a test  *|";
say sep ;
```

**Output:**

```
+-------------------+
|*  this is a test *|
+-------------------+
```
**Range:**

Range notation works for strings and Unicode:

```
new alpha = A['a'..'z']; --lowercase letters
new beta  = A['A'..'Z']; --uppercase letters
```

## Enumeration

Enumeration is an abstract data set. It is a group of identifiers. Each identifier represents an integer value starting from 0 to n-1 by default.
Enumeration values can start with a different number. First value can be specified using pair-up ":" operator.

```
def TypeName = { name₁:2, name₂, name₃};

new a, b, c ∈ TypeName;

let a = TypeName.name₁; --a=2
let b = TypeName.name₂; --b=3
let c = TypeName.name₃; --c=4
```

**Note:** When element name start with "." no need to use qualifiers for individual values

```
-- using public elements in enumeration
def TypeName = { .name1, .name2 };

new a, b = 0;

let a = name1; --a = 0
let b = name2; --b = 1

```

## Default Array Subscript (DAS)

Wee define Array variable using notation:[]().

```
new <array_name> =[<member-type>](c);   --one dimension with capacity c
new <matrix_name≥[<member-type>](n,m); --two dimensions with capacity n x m
```

Elements in default array are indexed from 0 to c-1 where c is capacity.
```
-- define DAS array with 10 Real elements
new test = [R](10); 

say test[!]; -- first element
say test[?]; -- last element

-- set value of element = subscript
new m = length(test);  
for x <: [0..m-1] 
  let test[i] = x;
for;

-- print all elements of array
for e <: test
  put (e,',');
for;

write 
```

**Output:**
```
 0,1,2,3,4,5,6,7,8,9,
```
**Note:** Elements start from 0. 

## Custom Array Subscript (CAS)

Optional we can specify subscript domain (n..m)

```
--one dimension array with subscript in range
new <array_name> =[<member-type>](n..m);

--one dimension array with unlimited capacity
new <array_name> =[<member-type>](n..∞);

--two dimension matrix with arbitrary index 
new <matrix_name≥[<member-type>](n..m,n..m);
```

**Example:**

```
-- define CAS array with 10 Real elements
new test = [R](1..10); 

say test[!]; -- first element
say test[?]; -- last element

-- set element of array = subscript
new n = test.!;  -- read first subscript
new m = test.?;  -- read last subscript
for i <: [n..m]
  let test[i] = i ;
for;
   
-- print the entire array
say test; -- expect: [1,2,3,4,5,6,7,8,9,10]

write;
```

**Notes:**
 
* Array of undefined capacity []() is ∅. Capacity can be established later.
* Array with capacity is automatically initialized, elements of array are 0 or 0.0.

## Array Slice

We can define a section of array using [n..m] notation. This is called slice. The numbers n and m represent the subscript of array element. First element of the array is [!] and last element is [?].

There are two kind of slices: View and Copy. The difference is View maintain references to same location for all members while a copy is cloning all members to new memory location.

**Syntax:**

```
-- declare an array with capacity (n)
new <array_name> = [<type>](c);

-- slice by-reference (view)
new <slice_name> : <array_name>[n..m];

-- transfer by-value (copy)
new <array_name> = <array_name>[n..m];

```

**Notes:** 
* Slice has references or a copy of original members;
* Last element of slice is symbolized by "?" first by "!"

```
-- slice examples with array
-- capacity is 5, last element is 0
new a = [1,2,3,4](5); 
say a -- [1,2,3,4,0];

-- making 4 slice views
new b : a[!..?]; -- [1,2,3,4,0]
new c : a[1..?]; -- [2,3,4,0]
new d : a[0..2]; -- [1,2,3]
new e : a[2..4]; -- [3,4,0]

--modify slice elements
let c[!] = 8; -- first element in c slice
let e[!] = 0; -- first element in e slice
let e[?] = 9; -- last element in e slice

--original array is modified
--                 ↧ ↧   ↧                        
say a; -- expect [1,8,0,4,9]

--modify last 3 elements
let a[2..?] = 0;
say a; -- expect [1,8,0,0,0]

```

## Matrix

It is an array with 2 or more indexes. We can have 2D or 3D array.

**Example:** 
```
new m = [R](4,4); -- define matrix

-- initialize matrix using "=" operator
let m = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]];

say m[0,0]; --first element
say m[3,3]; --last element

```

**Note:** Elements are organized in _row-major_ order.

So next program will print: 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,

```
-- elements in matrix can be accessed using single loop
for e <: m
  put (e, ',')
for;

write;
```
Printing the entire matrix will use Unicode to represent the matrix.

```
new m = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]];
say m;
```

Will print:

```
⎡  1,  2,  3,  4 ⎤
⎢  5,  6,  7,  8 ⎥
⎢  9, 10, 11, 12 ⎥
⎣ 13, 14, 15, 16 ⎦
```

## Tuple Notation

Tuple is an immutable enumeration of constants, separated by coma and enclosed in round brackets (...).
Notice a tuple is not a variable data type, it is a constant embeded in the source code as literal.

**Syntax**
```
(<value1>, <value2>...<,value3>)
```

**Notes**: Tuple members can have different data types--

**Immutable**

Tuples are immutable. Once a tuple is initialized it can't be modified.

```
-- define a tuple using type inference
let v = (1,'a',2,'b'); 

say v[0]; --error members of a tuple are not accessible by index
let v[0] =  4; --two errors you try to modify a tuple by index
```

**Unit:**

An empty tuple () represents an _"unit"_ 

```
new a = (); -- empty tuple (partial)
      
let a = (1,2,3); -- initialize tuple
let a = (2,3,4); -- re-initialize and throw to garbage (1,2,3)
```

### Unpacking

Tuples can be assigned to multiple variables using unpacking:

**Example:**

```
--create 3 new variables using tuple notation
new x, y = 0 ∈ Z;
new z ∈ L;

--unpacking modify all 3 value
let x, y, z = (97, 65, True);

say x ; -->  97
say y ; -->  65
say z ; -->  1

--unpacking using string template
new s = "{0} > {1}, {2}" <+ (2,1,"True"); 
say s; -- "2 > 1, True"
```

## Multiple results

A function can have as a result a tuple.

```
--body-less function do not use ":" and "."
test(x,y ∈ Z) => (x+1, y+1) ∈ (Z, Z);

new n, m ∈ Z;

--unpacking the result
let n, m = test(1,2);

say n; --will print 2
say m; --will print 3

-- ignoring the result
let _,_ = test(3,4);

```

## Partial unpacking
Tuple members can be ignored when unpacking using anonymous variable: "_"

```
new t = (0, 1, 2, 3, 4, 5);
new x,y,z ∈ Z;

-- first element and last 2 are ignored
let _, z, y, z, _, _ = t;

```

**Note:** When we unpack a tuple all members of the tuple must unpack. If the number of variables is less or more then the tuple members you will pop a compilation error.

## Data Record

Data record is a nested data structure. Records are similar to objects in OOP.
Record elements are enclosed in curly brackets { , , ,} and are separated by comma. 
Each element has a identifier/name and type associated with it using "∈".

**Syntax:**
```
def <TypeName> = {<element> ∈ <type>, <element> ∈ <type>...};
new <var_name> ∈ <TypeName>;

--using qualifier with attributes
let <var_name.element> = <value>;

--pair-up literal and values using ":"
let <var_name> = {
     <element> :<value>,
     <element> :<value>,
     ...};
```

**Nested structure:** can be created using similar to Json notation.

**Example:**
```
def Person = {
      name ∈ S, 
      age  ∈ N,  
      children = [Person]
    }; 

new r1,r2 ∈ Person;

--person with no children          
let r1 = {name:'Mica', age:21};

--person with two children
let r2 = {name:'Barbu', age:25, 
             children : [
               {name:'Telu', age:4},
               {name:'Radu', age:1} 
             ]
          };
```
## Structure _size_

Structure size is a constant that can be calculated using size(T).

**Example:**
```
def Person = {name: U, age: N};

--array of 10 persons
new catalog = [Person](10); 
  
--assign value using literals
let catalog[0] = {name:"Cleopatra", age:15};
let catalog[1] = {name:"Martin", age:17};

--using one element with dot operators
say caralog[0].name; --will print Cleopatra
say caralog[1].name; --will print Martin

--member type can be check using _type()_ built in
say type(Person.name); -- will print U
say type(Person.age);  -- will print W

--print size of structure
say size(Person);

write;
```

## Dynamic structures

These are data structures that can grow or shrink size during program execution.
Dynamic structures are implicit references. Default value is empty collection.

**Syntax:**
```
new <var_name> = [<element_type>]; --list
new <var_name> = {<element_type>}; --set
new <var_name> = {<key_type>:<value_type>}; -- hash map

```

**Example:**
```
-- define a string
new m,n ∈ S;  --string 

let m = "This is ";          
let n = "a very long string";

-- define arrays of strings
new lst1,lst2,list3 = [S]; 
  
let lst1 = split(m);
let lst2 = split(n);

let list3 = lst1 + lst2; -- concatenate two arrays
say list3.join(n);        -- This is a very long string

write
```

## Dynamic set

A mathematical set is a collection of unique elements.

```
--define 3 collections
new s1 = {1,2,3}; 
new s2 = {2,3,4};
new s  = {N}; --this is an empty set

-- empty collection
say "set \"s\" is empty" if s ≡ ∅

-- set specific operations
let s = s1 ∪ s2; --{1,2,3,4} --union
let s = s1 ∩ s2; --{2,3}     --intersection
let s = s1 - s2; --{1}       --difference 1
let s = s2 - s1; --{4}       --difference 2

-- declare a new set
new a = {1,2,3};

-- using operator +/- to mutate set a
let a = a + 4; --> {1,2,3,4} --append 4
let a = a - 3; --> {1,2,4}   --remove 3 (not 3)

```

**Notes:** 

* Wee sets are internally sorted not indexed;
* From a set you can't pop elements;

## Dynamic List

A list is a collection of non unique elements. A list do not have capacity while an array do.

```
new l1 = [1,2,3];
new l2 = [2,3,4];

new l3, l4, l5 = [];

--addition between lists "+" 
l3 = l1 + l2; --[1,2,3,2,3,4]

--difference between lists "-"
l4 = l1 - l2;  --[1]
l5 = l2 - l1;  --[4]
```

Fist element in a list is [!] last is [?]

```
new ls = ['a','b','c'];
new first, last, any = '_';

--first and last
let first =  ls[!]; -- 'a'
let last  =  ls[?]; -- 'c'

-- modify first/last
let ls[!] = 'm'; -- ['m','b','c']
let ls[?] = 'n'; -- ['m','b','n']

-- find and remove an element
let ls = ls - 'b'; --> ['m','n']

-- append a new element
let ls = ls + 'c'; --> ['m','n','c']

-- remove one element by index
del ls[1]; --> ['m','c']
```

**Stack**

A stack is a LIFO collection of elements.

```
new a = [1,2,3];
new last ∈ N;

-- using set with operator "+"
let a = a + 4; -- [1,2,3,4]

-- read last element using "="
let last = a[?];  -- last = 4, a = [1,2,3,4]

-- remove last element using pop
pop last = a[?]; -- last = 4, a = [1,2,3]
```

**Queue**

A queue is a FIFO collection of elements.

```
new q = [1,2,3];
new first ∈ N;

-- using enqueue operator "+:" 
let q = q + 4; -- [1,2,3,4]

-- read first element using "=" and "let"
let first = a[!]; --> 1 and a = [1,2,3,4]

-- dequeue first element using deq method
deq first = a[!]; --> 1 and a = [2,3,4]
```

## Hash Map

A map is a hash collection of data indexed by a key.

```
new map = {A:S};

-- initial value of map
let map = {'a':"first", 'b':"second"};

-- create new element
new map['c'] = "third";

-- modification of non existent element will fail
let map['e'] = "forth"; --> ERROR

-- finding elements by key
say map['a']; --'first'
say map['b']; --'second'
say map['c']; --'third'

-- remove an element by key
del map['a']; --> remove 'first' element
say map;      --> expected: {'b':'second', 'c':'third'}

write
```

**Note:** Hash map operators work like for sets


## Check for inclusion

We can check if an element is included in a collection.

```
new map = {'a':"first", 'b':"second"};

case ('a' ∈ map)
  say("a is found");
else
  say("not found");
case;
  
write  
```

## Partial declaration

Declare empty collections are initialized later.

**Unbound literals:**
```
new a = []; -- define empty list
new b = {}; -- define empty set or map
new c = (); -- define empty tuple

--before initialization    
say a ≡ ∅; -- 1 
say b ≡ ∅; -- 1 
say c ≡ ∅; -- 1 
  
let a = ['A','B','C']; --Bound to List of A elements
let b = {'a','b','c'}; --Bound to Set of A elements
let c = ('a','b','c'); --Bound to Tuple of A elements 

--after initialization
say a ≡ ∅; --> 0 
say b ≡ ∅; --> 0 
say c ≡ ∅; --> 0 
```

## Range Subtype

Range notation is used to define a range of values.

```
new a = 0;
new b = 10;

say [a..b] ;
write --> [0,1,2,3,4,5,6,7,8,9,10];
```

**Examples:**
Open range 

```
-- sub-type declarations
def SmallRange    = B[0..9];
def NegativeRange = Z[-10...0];
def AlfaChar      = A['a'..'Z'];
def NumChar       = A['0'..'9'];
def Positive      = Z[0..+∞];
def Negative      = Z[-∞..-1];

--Check variable belong to sub-type
case 'x' ∈ AlfaChar
  say ('yes');
else
  say ('no');
case;

write;
```

**Notes:**

* Anonymous range expression [n..m] is of Integer
* Range can apply only to discrete types (A,B,Z,N)
* Control variable can be declared in range using "∈"
* To check value is in range use operator "∈"

## Collection builder

Wee is using a special notation to create a sub-set.

 symbol | meaning                                           |
--------|---------------------------------------------------|
   ∀    | For all elements in defined in set: (for ∀ e ∈ X).|
   ∃    | Exist element element in set (∃ 2 ∈ X)            |
   ∈    | Define or check element belonging to set          |
   ∩    | Intersection between two sets                     |
   ∪    | Union between two sets or maps. For lists use "+" |
 
```
new a,b = {Z};

let a = { e : e ∈ [0.,10] };
let b = { x : x ∈ Z if (0 ≤ x) | (x ≤ 10) };

say a ≡ b; --> 1 (a and b are equal)
```

## Copy collection

Default assignment and slicing copy collection members.

```
new a = [0,1,2,3,4];
new e,f ∈ [Z]; -- empty collections

-- two different collections
say e /≡ a; --> 1 (not equal)

-- by default assign "=" copy/clone an entire collection
let e = a; 

-- compare two collections using "≡"
say e ≡ a; --> 1 (equal collections)

-- by default a slice is a copy/clone of original data
let f = a[2..?];  -- slice copy 

```

## Collection filters

A filter is a logical expression after "if" keyword enclosed in parenthesis ().
In next example we convert a set into a list of elements.

```
new a = {0,1,2,3,4,5,6,7,8,9} ;
new b = [ x : x ∈ a if (x % 2 ≡ 0)];
  
say(b)--will print [0,2,4,6,8];
```

## Expression mapping

A convenient way create sub-lists or sub-sets is to use an expression:

**Example:**
```
new test   = [0,1,2,3,4,5,6,7,8,9];
new result = [ x ⋅ 2 : x ∈ test[0..4]];

say result --> [0,2,4,6,8];

write;
```

## Variable arguments

One function or method can receive variable number of arguments.   
Declare an array using prefix "*" for parameter name.

```
--parameter *bar must be an array 
foo(*bar = [Z]) => x ∈ Z
  for i <: bar
    let x = x + bar[i];
  for;
foo;

--we can call foo with variable number of arguments
say foo();     --> 0
say foo(1);    --> 1
say foo(1,2);  --> 3
say foo(1,2,3);--> 6

write;
```

**Read next:** [Type Inference](inference.md) 