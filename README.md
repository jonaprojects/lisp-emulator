# **Lisp Emulator - Version 1.0.2**

## **Intro**
Lisp is a **functional** programming language, first introduced in the late 1950s by John McCarthy, a renowned computer scientist. Since then, many dialects of Lisp have been developed, with Common Lisp and Scheme being the main dialects nowadays.

Lisp is written in a prefix notation, and the code is always inside parenthesis.
It is also not case sensitive, however feel free to follow the
<a href="https://lisp-lang.org/style-guide/"> most updated conventions </a>.

The project focuses on emulating a basic environment resembling Common Lisp syntax and other compatible older versions. All of the code is written in Python.

## **Installation**

You can install the project from pip via the following the command:
``` 
pip install lisp-emulator
```

## **Usage** 

### **Arithmetic Operators**
  The most fundamental operations are addition (`+`), subtraction (`-`), multiplication(`*`) and division (`/`).
Those operators are of course supported and can receive an unlimited number of parameters.

Pay attention that those are not **binary** operations as we're used to in math and other programming languages. This is because in Lisp we use a **prefix notation**.

Here are some examples of basic calculations:
```lisp
    (+ 5 6 8)   ; 19
    (- 8 2 1)   ; 5
    (+ 6 4 (- 5 2))   ; 13
    (* 7 3)   ; 21
    (/ 6 2)   ; 3
```



### **Output**

You can use the `PRINT` or `WRITE` commands. For example:

```lisp
( print "hello" )
"HELLO"
```


### **Predicates**

Predicates return a boolean-like value - T (for true), and NIL (the equivalent of false).

- `ZEROP` - evaluates to T if the number is 0, else to NIL
- `EVENP` - evaluates to T if the number is odd, else to NIL
- `ODDP` - evaluates to T if the number is even, else to NIL
- `LESSP` - evaluates to T if the first value is smaller than the other
- `GREATERP` - evaluates to T if the first value is bigger than the other
- `NUMBERP` - evaluates to T if the value is a number, else to NIL
- `STRINGP` - evaluates to T if the value is a string (by the double quotation ".." mark), else to NIL

### **Equality Operation**

Equality can be performed via the = operator that can receive
an indefinite number of parameters or the EQ method that receives only 2 parameters.
Those methods return T if all the expressions are equal, else NIL.

### **Mathematical Operations And Constants**

PI Constant - PI is a global constant, and represents
approximately 3.1415926535.
E Constant - E is a global constant, and represents approximately
2.71828182846.

### **Trigonometric operations**

All of the trignonometric operations are handled in *radians*, rather than degrees.
Here is a full list of the supported trigonometric functions;

- `SIN` - receives a parameter and returns its sine.
- `COS` - receives a parameter and returns its cosine
- `TAN`- receives a parameter and returns its tangent
- `ASIN` - The reverse operation of SIN.
receives a parameter within range of -1 and 1 and
returns the angle that its sine equals to the parameter (in radians)
- `ACOS` - The reverse operation of COS.
receives a parameter within range of -1 and 1 and
returns the angle that its cosine equals to the parameter (in radians)
- `ATAN`- The reverse operation of TAN.
receives a parameter within range of -1 and 1 and
returns the angle that the result of its tangent operation equals to the parameter (in radians)
- `SINH` - Hyperbolic sine
- `COSH` - Hyperbolic cosine
- `TANH` - Hyperbolic tangent
- `ASINH` - The reverse operation of SINH
- `ACOSH` - The reverse operation of COSH
- `ATANH` - The reverse operation of TANH

For instance:

```lisp
( sin ( / PI 2 ) ) ; 1.0
```

### **Other mathematical operations**
- `SQRT` - receives a parameter and returns its square root
- `EXPT` - receives two parameters and returns the power of the first
parameter by the second.
- `EXP` - receives one parameter and returns the
power of E ( 2.71828182846 ) by that number.
- `MAX` - receives N parameters and return the value of the biggest.
- `MIN` - receives N parameters and return the value of the smallest.
- `GCD` - receives N parameters and returns their Greatest Common
Denominator Operation.
- `ABS` - receives a parameter, and returns its absolute value.

## Creating Variables
You can define new variables via the `SET` and `SETQ` methods
( `defvar`, `defparameter` keywords are not implemented yet )

For example:

```lisp
( setq number 5 ) ; 5
( + 3 number 4 ) ; 12
```

### **Conditionals**

Conditions are created via IF expressions

### **String Operations**
Concatenate - receives N strings and evaluates to their concatenation.
For example,

### **Data Types**
There are currently only 3 supported datatypes in the project: strings, integers and decimals.
`str` - strings. A sequence of characters, sorrounded by double quotes. For example: "hello" , "world".
`int` - integers. For example: 6, -3 ,2.
`dec` - decimal numbers. For instance, 6.1, 2.23, etc...

### **Predicates**
Predicates return a boolean-like value - T (for true)
, and NIL (the equivalent of false).

- `ZEROP` - evaluates to `T` if the number is `0`, else to `NIL`
- `EVENP` - evaluates to `T` if the number is odd, else to `NIL`
- `ODDP` - evaluates to `T` if the number is even, else to `NIL`
- `LESSP` - evaluates to `T` if the first value is smaller than the other
- `GREATERP` - evaluates to `T` if the first value is bigger than the other
- `NUMBERP` - evaluates to `T` if the value is a number, else to `NIL`
- `STRINGP` - evaluates to `T` if the value is string (by the double quotation ".." mark)
else, to NIL

### **Equality Operation**

Equality can be performed via the = operator that can receive
an indefinite number of parameters or the EQ method that receives only 2 parameters.
Those methods return T if all the expressions are equal, else NIL.

### **Constants**

You can use these global constants anywhere in your program.

- `PI` Constant - PI is a global constant, and represents
approximately 3.1415926535.
- `E `Constant - E is a global constant, and represents approximately 2.71828182846.
