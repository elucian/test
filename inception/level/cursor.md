## Cursor section

A cursor is special section that is based on one single select statement. 
Cursor can return a structure that is a record or a table row_type. 
A cursor is equivalent to a generator. It yields one record at a time on demand using fetch.

**Syntax:**
```
cursor <name>(<params>) : <record_type> is
  <select_statement>
end cursor;
```

## Using a cursor
A cursor can be open, fetch and closed. This can be done also using _for_ loop. 
We can fetch row by row or in bulk for several rows or all rows. This may be too much if the data set is very large. 

**Syntax:**

**using fetch...**
```
<cursor_name>.open(<arguments>);
fetch <cursor_name> to <record_variable>;
fetch <cursor_name> to <list_of_records> [limit N];
<cursor_name>.close;
```
**using for loop...**
```
for <record_name> in <cursor_name> loop
  with <record_name> do
     ... --use record fields
  end do;
loop;
```

**Examples:**
* [data_demo.lev](https://github.com/elucian/level/blob/master/example/data_demo.lev)
* [data_fetch.lev](https://github.com/elucian/level/blob/master/example/data_fetch.lev)

**Read next:**
[table](table.md),
[select](select.md)