# TypeScript For the 301 Java Developer

> Written by Ajay Gandecha for the CSXL Web Application and for COMP 423: Foundations of Software Engineering.<br>
> *Last Updated: 12/14/2023*

## Preface

### Uses of TypeScript

### TypeScript vs Java

*Nominal vs structural* 

## Syntax

The syntax for TypeScript is pretty succint and less verbose than Java! In this section, you will learn the syntax of TypeScript code with the context of the Java syntax you have worked in throughout *COMP 210* and *COMP 301*.

### Typing

The first major distinction between Java and TypeScript exists with its typing system. Recall the following:

* **Primitive types** are a set of basic data types in a programming language. All other data types and classes can be constructed from these primitive types. Using standard programming conventions, primitive types are often denoted with a *all-lowercase* name and usually do not need to be imported.
* **Reference types**, on the other hand, are all of the other types in a language. Reference types are defined as structures that contain or build upon the basic primitive types. Reference types are often defined by *interfaces*, *classes*, and *enumerations*. Reference types, like the name of all clases, often start with a capital letter (For example, `Dog` or `Cat`).

In **Java**, we have the following *primitive* types:
* `int`: Represents a number with no decimal places.
* `double`: Represents a number that can store fractions (decimal places).
* `boolean`: Represents a state that can either be `true` or `false`.

Note that in Java, `String` is a *reference* type.

In **TypeScript**, on the otherhand, we have **different** primitive types. TypeScript defines the following:
* `number`: Represents a number that can store fractions (decimal places).
* `boolean`: Represents a state that can either be `true` or `false`.
* `string`: Represents a sequence of characters.

There are two important things to note here. First, notice that there is not really a distinction between *integers* and *floats / doubles*. We use `number` in TypeScript for both. This is actually super helpful because it can prevent a lot of arithmetic errors or unexpected results.

Second, notice that `string` is a *value* type in TypeScript. This is important to remember to keep your types and capitalization consistent.

### Variable and Constant Declarations


### Conditionals


### Loops


### Defining Functions


### Arrow Functions


### Class Construction


## Exercises
