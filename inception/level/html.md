## HTML Data Type

It is a goal of Level to have HTML data type. This data type may contain text and template placeholders. 

## HTML Literals
HTML may be a text on multiple lines. The indentation may be corrected a little bit by the compiler. 
We can substract the unnecesary even indentation. 
We define a 3 double quote " separators: `"""` that will be at the beginning and at the end of the HTML text.

**Example:**

```
program test_html(s string, a,b integer, c,d real):
  my_html html;
execute
  my_html:
  """
  <--DOCTYPE html>
  <html>
    <body>
      <h1>My First Heading</h1>
      <p>My first paragraph.</p>
    </body>
  </html>
  """;
end program;
```

## Usability
Having html data type declared an IDE tool can try to parse this HTML text and search for syntax errors. 
If we define HTML literals as simple text data type then we can indeed store literals in the program 
source code but we can not use a tool to verify text syntax as HTML.
