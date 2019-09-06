@Jar of Salt from Discord

So, first you're going to need a parser and lexer. I recommend using ANTLR to generate one for you and then using their run times, available for; Java, C#, C++, Go, Python and Swift (might be more now). There's a full book and online docs on how to use the Antlr language to define the parser and lexer.

Then I'm going to recommend to compile to a virtual machine, the JVM and the LLVM seem like good options currently, and both have easy APIs to do so, such as the JVMs ASM library.

You could also make a transpiler instead like I did for my language, which transpiles a Kotlin-like language to C, adding features like packages and classes.


1. Assambly
I advise before you do that learn Logic Gates, Queues and Assembly if you haven't already. DragonBook is more for optimizations in compiler technology so I wouldn't recommend that, unless you can pick up quickly.

2. Parsing
- Parsing is boring.  Skip it as much as possible.  Tools like lex/yacc/bison are heavy weight with a large learning curve, used to compile heavy-weight-syntax languages (C, C++, Java).  Instead skip to a trivial syntax; here's three choices: Forth - white-space delimited only.  Great starter language (and my first, both interpreter and compiler).  Pascal: simple recursive-descent parser; skip the heavy lex/yacc/bison and just write the trivial parser by hand.  "Mouse:" ancient bogus language just used to teach people how to write interpreters and compilers; think "Forth, but all tokens are exactly 1 character" - so parsing is really REALLY trivial.

- Relocation, linking loaders, link steps, etc... all mechanical and boring as well.  Skip 'em.  Just make code into a RAM buffer at first.  Later you can figure out all the fiddly bits with linkers & loaders (and why they exist, such as allowing the code to be relocated and still work).

- Generate the machine code yourself - don't generate something in-between (e.g. C code or Java bytecodes).  You'll learn a crap-ton more, and for a simple compiler it's not all that hard.  Crucial to the learning.

- Write the interpreter first: parse into something internal in little bits, then execute the bits.  i.e., be able to execute the input language. Crucial to the learning. Once that works, instead of "execute the bits", you "generate the code that executes the bits".  Ta-da, a compiler.  This can be really really trivial if you just puke the "execute the bits" code into memory.  If later, you write that memory buffer out to disk, it's a classic compiler.  If later, you execute that memory buffer, it's a "JIT".