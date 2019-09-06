## Unicode

Unicode string is a set of _code points_ using symbols from universal character set (UCS). There are many encoding techniques available. Java uses UTF-32. We will probably use UTF-8 to be more efficient.

*Example:*
```
   us: "I can write Greek: \"αβγδ\".";
   print(us);
```
> I can write Greek: "αβγδ".

To edit source code containing Unicode literals one must use a specific font and UTF-8 source files. The preferred font for Level programming is "DejaVu Sans Mono". 

**console**
Windows console can support Unicode fonts. You must add a new entry in registry:
```
1. run:> regedit
2. locate: HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Console\TrueTypeFont
3. add text entry:000 and modify to: "DejaVu Sans Mono"
4. close regedit
5. start/restart console
6. use: chcp 65001
7. edit default font and select "DejaVu Sans Mono"
```

**See also:** [wikipedia ucs](https://en.wikipedia.org/wiki/Universal_Coded_Character_Set), 
[unicode characters](https://en.wikipedia.org/wiki/List_of_Unicode_characters#Character_reference_overview)

## Editor Font
Best fonts for unicode symbols: 

* [DejaVu Sans Mono](https://dejavu-fonts.github.io/)
* [GNU Unifont](http://unifoundry.com/unifont/index.html)

Alternative fonts I have try:
* Lucida Sans Unicode.
* Fixedsys Excelsior.
* Everson Mono.
* GNU Freefont
* Ubuntu Unifont
* Google Roboto Mono

https://en.wikipedia.org/wiki/Lucida_Sans_Unicode
http://www.fixedsysexcelsior.com/
http://evertype.com/emono/
http://www.gnu.org/software/freefont/
http://www.unifoundry.com/unifont.html

**Numeric types**

* ℕ = Natural Numbers   
* ℤ = Integers          
* ℚ = Rational Numbers  
* ℝ = Real Numbers      
* ℂ = Complex Numbers  

Alternative notation for numeric types:
* ℙ = Maybe pointer ?
* ℍ = Hexadecimal number

**Greek Alphabet**

ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ
αβεδζη θικλμνξοπρσςτυφ


π = 180°

**Imaginary number** 

ⅈ = √(-1)

(λ expression)

Underline _ Overlie: ‾ Vertical |

Superscript numbers:
M⁽⁾ ⁺ ⁻ ⁼ · ⁰ ¹ ² ³ ⁴ ⁵ ⁶ ⁷ ⁸ ⁹
A ⁿ ʰ ˣ ʸ ʰ ʷ ʳ ʴ ˢ ʲ ʺ ʻ ʼ ™

Subscript numbers:
M . ‚ ₀ ₁ ₂ ₃ ₄ ₅ ₆ ₇ ₈ ₉ 
X ₋₊₌₍₎

Middle small symbols:
X · ‹› « »

Subscript letters: (b,c,d,y,z missing)
Xₐ…ₑₕᵢⱼₖₗₘₙₒₚᵣₛₜᵤᵥₓₔ

**Vulgar fraction**
⅟ ½ ¼ ¾ ⅛ ⅜ ⅝ ⅞ ⅓ ⅔ ⅕ ⅖ ⅗ ⅘ ⅙ ⅚ ⅛ ⅜ ⅝ ⅞ 

## Fraction sign

¹⁄₂ ²⁄₂ ³⁄₂ ⁴⁄₂ ⁵⁄₂ ⁶⁄₂ ⁷⁄₂ ⁸⁄₂ ⁹⁄₂ 
¹⁄₂ ¹⁄₃ ¹⁄₄ ¹⁄₅ ¹⁄₆ ¹⁄₇ ¹⁄₈ ¹⁄₉ ¹/₁₀

examples: 
A = (¹⁄₂,¹⁄₄,¹⁄₈)
B = [¹⁄₂,¹⁄₄,¹⁄₈]
C = {¹⁄₂,¹⁄₄,¹⁄₈}

## Power

  X⁻¹·⁵ 
  X²+6*A²

## Misc symbols

**Star shapes**
✡✢✣✤✥✦✬✭✮✯✱✲✳✴✵✶✷✸✹✺✻✼✽✾✿❀❂❃❄❅❆❇❈❉   

**Dice Symbols**
⚀ ⚁ ⚂ ⚃ ⚄ ⚅

**Bulet Points**
➀ ➁ ➂ ➃ ➄ ➅ ➆ ➇ ➈ ➉

**Arrows:**
 ⇤ ⇥ ↼ ⇀ ← → ↔ 
 ↑ ↓ ↕ ↥ ↧ ↯
 
## Unicode Operators

Using  "DejaVu Sans Mono" font we can define new operators and symbols. 
These symbols however can be used only in strings. We do not use Unicode operators in the language. 
This may be a nice feature to have but unfortunately not very practical.

## Other Resources

Brackets ⟨⟩❬❭❰❱❲❳❴❵

Unicode Math Symbols ∑ ∫ π ∞

-----------------------------------------------------------------

Complete list of math symbols in Unicode 11 grouped by purpose.

**Greek letters** 

Α Β Γ Δ Ε Ζ Η Θ Ι Κ Λ Μ Ν Ξ Ο Π Ρ Σ Τ Υ Φ Χ Ψ Ω 
α β γ δ ε ζ η θ ι κ λ μ ν ξ ο π ρ ς τ υ φ χ ψ ω

**Superscript**
A ⁰ ¹ ² ³ ⁴ ⁵ ⁶ ⁷ ⁸ ⁹ ⁺ ⁻ ⁼ ⁽ ⁾ 
A ⁿ ⁱ

**Subscript**
A ₀ ₁ ₂ ₃ ₄ ₅ ₆ ₇ ₈ ₉ ₊ ₋ ₌ ₍ ₎ 
A ₐ ₑ ₕ ᵢ ⱼ ₖ ₗ ₘ ₙ ₒ ₚ ᵣ ₛ ₜ ᵤ ᵥ ₓ ₔ


circled {plus, times, …} ⊕ ⊖ ⊗ ⊘ ⊙ ⊚ ⊛ ⊜ ⊝

squared {plus, minus, times, …} ⊞ ⊟ ⊠ ⊡

# Other operators
 
Roots √ ∛ ∜

* Infinity ∞
* Multiplication × ✕ ✖ 
* Division  ÷

∘ 2217 Ring Operator
∙ 2219 Bullet Operator
⋅      Middle dot 
⋆      Star operator

… u-2026 (Alt+0133) Horizontal ellipsis

⇒ ‼ ⁇ « »

**Set symbols**
```
∅ 
⊂ ⊃ ⊄ ⊅ ⊆ ⊇ ⊈ ⊉ ⊊ ⊋ ⋐ ⋑ 
∋ ∉ ∌
∪ ∩
```

**Order**

Precede and succeed ≺ ≻ ≼ ≽ ≾ ≿ ⊀ ⊁ ⋞ ⋟ ⋠ ⋡ ⋨ ⋩ 
less and greater < > ≮ ≯ ≤ ≥ ≰ ≱ ≦ ≧ ≨ ≩
less and greater 2 ⋜ ⋝ ≶ ≷ ≸ ≹ ⋚ ⋛ 

less and greater with equivalence ≲ ≳ ⋦ ⋧ ≴ ≵
less and greater misc ≪ ≫ ⋘ ⋙ ≬

**Equality, Identity, Equivalence, Approx, Congruence**

equality ≝ ≞ ≟ ≠ ∹ ≎ ≏ ⪮ ≐ ≑ ≒ ≓ ≔ ≕ ≖ ≗ ≘ ≙ ≚ ≛ ≜
Identity ≡ ≢ 
Equivalence ≍ ≭ ≣ 
Approx/almost/asymptotic equality ≁ ≂ ≃ ≄ ⋍ ≅ ≆ ≇ ≈ ≉ ≊ ≋ ≌ ⩯ ⩰
Misc equality ∻
Misc relations ⊏ ⊐ ⊑ ⊒ ⋢ ⋣ ⋤ ⋥

**Logic**

Logic ∀ ∁ ∃ ∄ ∴ ∵
Logic binary ∧ ∨ ¬  

**Geometry**

Ratio, proportion ∝ ∶ ∷ ∺
Parallel, perpendicular ∥ ∦ 
Angles ∠ ∡ ∟ ⊾ ⊿

**Operators**

Integrals ∫ ∬ ∭ ∮ ∯ ∰ ∱ ∲ ∳

Derivative ∂ ′ ″ ‴ ∆

**Vector** 

⨯ ∇

Tilde Operators ∼ ∽

n-nary sum ∑ 
n-nary product ∏


## Misc symbols
 
± ∓ Δ ▽ Ψ⌁ ϵ ϶ ⍙ ⍫ ◇ ⨯ ∀ Ɐ ⎊ ⍜ ⍉ ⌘ ‼ ¿ ǂ ʊ Ұ θ ≡  
↻ ↺ ‡ ⍜ ⍛ ⍶ ⍙ ⍚ ¦ Ɐ ♇ ◻ ◯ ◬ ⍭ ⌽ ↹ ↯ ⁉ ⁈ ⁇ ‼ ‡ † ւ ǂ ǁ ǀ ÷ ¿ ⸮ ? ¬ 


Line: Low line _ Overlain: ‾ Vertical | double ̿ ‖ ‗  

 
**Missing**
Some subscript/superscript characters are missing.
I found this proposal: http://unicode.org/L2/L2011/11208-n4068.pdf

* Euler number, base of natural log ℯ, ⅇ (Missing)

**Alternative Historical Research**
There was once upon a time a language called APL.

https://en.wikipedia.org/wiki/APL_(programming_language)

