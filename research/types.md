Impressive article:

Rust Traits

https://blog.rust-lang.org/2015/05/11/traits.html


## Native Types

Native types are defined using one small letter followed by a number.

| Type | Sign      |Bytes|Description
|------|-----------|-----|------------------------------------------------------------
| u8   | unsigned  | 1   |Unsigned 8  bit, max: 255
| u16  | unsigned  | 2   |Unsigned 16 bit, max: 64535
| u32  | unsigned  | 4   |Unsigned 32 bit, max: 4294967295
| u64  | unsigned  | 8   |Unsigned large positive integer [0..+*]
| i8   | signed    | 1   |Signed half   integer 8  bit  [-128..127]    
| i16  | signed    | 2   |Signed short  integer 16 bit  [-32768..+32767]
| i32  | signed    | 4   |Signed binary integer 32 bit  [-..+*]
| i64  | signed    | 8   |Signed large  integer 64 bit  [-..+*]
| f32  | signed    | 4   |Double precision float (0..+*)
| f64  | signed    | 8   |Double precision float (-*..+*)
