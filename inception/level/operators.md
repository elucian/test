## Operators

In Wee the most common operators are using ASCII symbols.    
Uncommon operators are using Unicode symbols and are difficult to input.

symbol| description
------|----------------------------------------------------------------
 ¹⁄    | Higher priority fraction. Usually for Unicode:  x^¹⁄₂ ≡ x^(¹⁄₂)
 ^    | Power symbol used with fractions or expressions
 ⋅    | Multiplication, used instead of (*)
 ÷    | Division, used instead of (/)
 %    | Reminder \| modulo operator
\+    | Addition \| collection union \| string concatenation
\-    | Subtraction \| difference between two collections 
 =    | Assign by value \| define data type     
 :    | Assign by reference \| borrow reference 

## Single Symbols

All these single symbols you find on your standard keyword.

symbol| description
------|-------------------------------------------------------------
 \#   | Compiler directives prefix
  $   | Global variables prefix \| System environment constants
  @   | Reserved for pointers \| Reference to "any" type
  ↻   | String repetition: `'*' ↻ 3 ≡ '***'`
  ;   | End of block statement  \| Many statements per line
  .   | Public member \| Public element \| Static variable
  .   | String concatenation for library/module path
  :   | Code block start \| Key:value pair-up
  '   | ASCII character literal is using single quotes "'"
  "   | Unicode string literals are using double quotes '"'
  !   | Factorial function: y = n!
  ?   | Last element subscript a[?] = a.last
  \*  | Parameter prefix for variable arguments \| [*] all elements
  \_  | Anonymous variable (constant  = ' ')
  /   | Symbol modifier: /∈ /≡ /⊂ /⊃ /≈ \| URL string concatenation
  \\  | Escape character (\\n = New Line) \| regular expression

## Brackets

Wee is using brackets for expressions and data structures.

symbol| description
------|-----------------------------------------------------
  ()  | Expression, group of expressions or empty List
  []  | Array or range \| access of elements by index 
  {}  | Enumeration, structure, set or hash map


## Double Symbols

Double symbols are ASCII symbols found on your keyboard.    
I have carefully selected these symbols for maximum usability.

symbol| description
------|------------------------------------------------------
\|\*  | Begin expression comment, or nested comment
 \*\| | End expression comment or nested comment
 \--  | Start for single line comment /separator
 \**  | Start for a subtitle comment /separator
 \##  | Start for a title comment /separator  
 ..   | Define range or array slice between two values [n..m]
 ->   | Function pipeline \| Conversion \| Boxing
 <+   | Insert one or more values into a string template 
 ==   | Same reference. Both arguments must be references
 !=   | Not the same reference. Useful only for references


## Logical

Logical operators return: 1 = true or 0 = false

symbol| meaning    | notes
------|------------|--------------------
   ↔  | Equivalent | not the same as ≡
   ~  | Logic NOT  | unary operator
   &  | Logic AND  | shortcut operator
   \| | Logic OR   | shortcut operator
    ↑ | Logic NAND | p ↑ q ↔  (¬p ∨ ¬q)
    ↓ | Logic NOR  | p ↓ q ↔ ¬( p ∨  q) 

**The table of through**

   n   | ~ n
-------|--------
   0   | 1      
  <1   | 1      
   1   | 0      
  >1   | 0      

 p | q | p ↔ q | p & q | p \| q
---|---|-------|-------|--------
 1 | 1 | 1     | 1     | 1      
 1 | 0 | 0     | 0     | 1      
 0 | 1 | 0     | 0     | 1      
 0 | 0 | 1     | 0     | 0      
--------------------------------

## Bitwise Operators

Result of these operators is a number >= 0

 symbol | description
--------|----------------------------------
  «     | shift bits to left  
  »     | shift bits to right
  ¬     | bit not
  ∧     | bit and
  ∨     | bit or
  ⊕     | bit xor

**Examples**

 A    | B   | A ∧ B  | A ∨ B   | A ⊕ B
------|-----|--------|---------|--------
 00   | 00  | 00     | 00      |  11    
 01   | 00  | 00     | 01      |  10    
 11   | 01  | 01     | 11      |  00    
 10   | 11  | 10     | 11      |  01    


**Bit Manipulation**

 A    | A « 1 | A » 2  |  ¬ A
------|-------|--------|-------
 0000 | 0000  | 0000   | 1111
 1111 | 1110  | 0011   | 0000
 0111 | 1110  | 0001   | 1000
 0110 | 1100  | 0001   | 1001

See also:[Bit Manipulation](https://en.wikipedia.org/wiki/Bit_manipulation)
 
## Relations

Relation operators are used to compare expressions.

symbol | meaning
-------|----------------------------------------------
 ≡     | equality of two values of the same type
 ≈     | almost equal or equal (works for numbers)
 ≠     | divergence of two values (not equal)
 \>    | value is greater than 
 \<    | value is less than
 ≥     | greater than or equal to
 ≤     | less than or equal to

**redundancy**
* Operator /≡ and ≠ are one and the same thing.
* Operator ≥ is the same as /< and >= 
* Operator ≤ is the same as /> and <=

## Set operators

symbol | meaning
-------|--------------------------------------------------
  ∅    | Represents empty collection: {},[],()
  ≡    | Equivalent objects, collections or structures
  ⊂    | Check if subset is of a larger set
  ∩    | Intersection between two sets
  ∪    | Union between two sets or maps. For lists use "+"
  ∈    | Define variable or check element belonging to set 

## Power Operator

Wee is using superscript numbers to represent power. 

**Superscript**
```
M ⁺ ⁻ · ⁰ ¹ ² ³ ⁴ ⁵ ⁶ ⁷ ⁸ ⁹ 
A ⁱ ʲ ᵏ ⁿ ᵒ ᵖ ʳ ˢ ˣ ʸ ᶻ 

A ᵃ ᵇ ᶜ ᵈ ᵉ ᶠ ᵍ ʰ ⁱ ʲ ᵏ ᶩ ᵐ ⁿ ᵒ ᵖ ʳ ˢ ᵗ ᵘ ᵛ ʷ ˣ ʸ ᶻ 
B ᴬ ᴮ ᴰ ᴱ ᴳ ᴴ ᴵ ᴶ ᴷ ᴸ ᴹ ᴺ ᴼ ᴾ ᴿ ᵀ ᵁ ᵂ 
```

**Subscript**
```
M . ‚ ₀ ₁ ₂ ₃ ₄ ₅ ₆ ₇ ₈ ₉ 
X ₐ ₑ ₕ ᵢ ⱼ ₖ ₗ ₘ ₙ ₒ ₚ ᵣ ₛ ₜ ᵤ ᵥ ₓ
```

**Fractions**
Wee has support for fraction sign:"⁄"
 
```
¹⁄₂ ¹⁄₃ ¹⁄₄ ¹⁄₅ ¹⁄₆ ¹⁄₇ ¹⁄₈ ¹⁄₉ ¹⁄₁₀
```
**Read Next:** [keywords](keywords.md)
