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

Now that you know a bit about the basic data types in TypeScript, let's take a look at how to define **variables**.

Let's compare a number declaration in Java and Typescript, then compare more generally.

<table>
<tr><th width="520">Java</th><th width="520">TypeScript</th></tr>
<tr>
<td>
 
```java
// Declaring a Number
int myNumber = 88;

// General Formula
type name = value;
```

</td>
 <td>
  
```ts
// Declaring a Number
let myNumber: number = 88;

// General Formula
let name: type = value;
```

</td>
</tr>
</table>

As you can see, there are a few differences. First, in Java, we specify the data type *first*. In TypeScript, we provide a **type annotation *after*** the name of the variable. We also provide the `let` keyword before variable name.

You can also notice the difference in types. In Java, we use the `int` primitive type. In TypeScript, we use `number` instead. Lastly, you can note that both Java and TypeScript use semicolons at the end of their lines.

What if we wanted to make these values *constants* instead of variables (so that we cannot change their value later)?

<table>
<tr><th width="520">Java</th><th width="520">TypeScript</th></tr>
<tr>
<td>
 
```java
// Declaring a Constant
final int myNumber = 88;

// General Formula
final type name = value;
```

</td>
 <td>
  
```ts
// Declaring a Constant
const myNumber: number = 88;

// General Formula
const name: type = value;
```

</td>
</tr>
</table>

**Java**


**TypeScript**
```ts
const myNumber: number = 88;
```
```ts
const name: type = value;
```

As you can see, in Java, we use the `final` keyword to turn a variable into a constant. The keyword is appended to the front. In TypeScript however, we just use the `const` keyword ***instead of*** the `let` keyword!

### Arrays

The way that arrays work in Java and TypeScript are a bit different, and so is the syntax to create them.

In Java, you probably remember that the length of an array cannot be changed once it is set, and that using `ArrayList<>` or any other subtype of `List` (imported from `java.utils.*`) provides this functionality!

TypeScript arrays **are more similar to the Java `List` than to the Java array**. Creating arrays in TypeScript is also very similar to creating lists in Python. To declare an array in TypeScript, we can simply add `[]` to the end of a variable's *type annotation*, and use brackets to add initial values. Compare the following:

<table>
<tr><th width="213">Python</th><th width="213">Java</th><th width="213">TypeScript</th></tr>
<tr>
<td>
 
```py
# Initialize
names = ["Felipe", "Sarah"]
# Add values
names.append("Jordan")
# Replace a value
names[3] = "Kris"
# Access a value
felipe = names[0]
```

</td>
 <td>

  ```java
// Initialize
List<String> names =
    new ArrayList<>();
names.add("Felipe");
names.add("Sarah");
// Add values
names.add("Jordan");
// Replace a value
names.set("Kris", 3);
// Access a value
String felipe = names.get(0);
```

</td>
<td>

```ts
// Initialize
let names: string[] = ["Felipe, "Sarah"]
// Add values
names.push("Jordan");
// Replace a value
names[4] = "Kris";
// Access a value 
let felipe: string = names[0];
```
 
</td>
</tr>
</table>

Just like in Python lists and traditional Java arrays (but unlike Java's `List`), we can select values of TypeScript arrays using the `[]` syntax.

### Conditionals



### Loops


### Defining Functions


### Arrow Functions


### Class and Interface Construction

### Extra TypeScript Features
 - Enums
 - Type aliases

## Exercises
