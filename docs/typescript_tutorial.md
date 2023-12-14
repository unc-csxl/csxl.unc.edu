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
names[2] = "Kris"
# Access a value
felipe = names[0]




```

</td>
 <td>

  ```java
// Initialize
List<String> names = new ArrayList<>();
names.add("Felipe");
names.add("Sarah");
// Add values
names.add("Jordan");
// Replace a value
names.set("Kris", 2);
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
names[3] = "Kris";
// Access a value 
let felipe: string = names[0];




```
 
</td>
</tr>
</table>

Just like in Python lists and traditional Java arrays (but unlike Java's `List`), we can select values of TypeScript arrays using the `[]` syntax.

### Conditionals

Java and TypeScript have similar syntax for creating *conditional statements* and *if-statements*. 

TypeScript uses the same **boolean operators** that Java does. This means that `&&` represents *AND*, `||` represents *OR*, and `!` represents *NOT*. TypeScript and Java both use the lowercased `true` and `false` for boolean values.

If-statements have the ***same syntax and usage*** as they do in Java!

<table>
<tr><th width="520">Java</th><th width="520">TypeScript</th></tr>
<tr>
<td>
 
```java
if (conditionA || conditionB) {
 // Some code here!
}
else {
 // Some code here.
}
```

</td>
 <td>
  
```java
if (conditionA || conditionB) {
 // Some code here!
}
else {
 // Some code here.
}
```

</td>
</tr>
</table>

> **NOTE:** Both Java and TypeScript require the use of parenthesis `( )` around the conditional statements in if-statements.

### Loops

#### The `while` Loop

Just like with if-statements, both Java and TypeScript use the same syntax for while loops! We use parenthesis around the conditional in both languages. 

<table>
<tr><th width="520">Java</th><th width="520">TypeScript</th></tr>
<tr>
<td>
 
```java
while (conditionA) {
 // Some code here!
}
```

</td>
 <td>
  
```java
while (conditionA) {
 // Some code here!
}
```

</td>
</tr>
</table>

### The `for` Loop

In both Java and TypeScript, there are two types of loops that both service distinct purposes.

The first type of loop contains a counter variable that is modified each time the the loop iterates - and, iteration stops when some provided condition evaluates to false. This type of loop exists in ***both*** Java and TypeScript. The code is *nearly* identical, but notice that in the TypeScript version, we need to use our new method of creating variables. We do not say `int i = 0;`, instead we say `let i = 0;`. We can see this here:

<table>
<tr><th width="520">Java</th><th width="520">TypeScript</th></tr>
<tr>
<td>
 
```java
for(int i = 0; i < 10; i++) {
 // Loop body here...
}
```

</td>
 <td>
  
```ts
for(let i = 0; i < 10; i++) {
 // Loop body here...
}
```

</td>
</tr>
</table>

> **NOTE:** In this example, notice how we do not include the type annotation on the conditional variable. In general, type annotations on variables in TypeScript is not necessary by default. TypeScript infers types of variables when there is no explicit type annotation provided. However, including them it is ***strongly encouraged***. In this case, for conciseness in the for loop header body and the the fact that the variable's type is guaranteed to be `number`, it can be omitted here.

The second type of loop in Java allows you to *iterate over a collection*, where a variable is updated with a value corresponding to the current iteration. This is often the most widely-used loop. There are syntactical differences here between Java and TypeScript, both in the *keywords used* and the variable creation convention.

<table>
<tr><th width="520">Java</th><th width="520">TypeScript</th></tr>
<tr>
<td>
 
```java
for(String name : names) {
 // Loop body here...
}
```

</td>
 <td>
  
```ts
for(let name of names) {
 // Loop body here...
}
```

</td>
</tr>
</table>

As you can see, like in previous examples, TypeScript uses the `let` keyword. In addition, Java uses `:`, while TypeScript uses `of`.

### Defining Functions

Functions is the most fundamental abstraction technique we use all the time in software engineering. It is important to note that in Java, we create *methods*, which are functions that are members of a *class*. In TypeScript, we also mainly work in the context of classes, but we are not necessarily required to. So, if you are hearing the term "functions" and "methods" passed around, it is useful to remember this distinction.

There are many fundamental differences in the syntax for creating functions in Java and TypeScript. Let's take a look at an example of a function that takes in a user's name and returns a string that greets the user.

<table>
<tr><th width="520">Java</th><th width="520">TypeScript</th></tr>
<tr>
<td>
 
```java
String greet(String name) {
 return "Welcome, " + name + "!";
}
```

</td>
 <td>
  
```ts
function greet(name: string): string {
 return "Welcome, " + name + "!";
}
```

</td>
</tr>
</table>

There are a few noticeable differences. First, TypeScript uses the `function` keyword at the front rather than specifying a return type first. Also, the *type annotation* is at the end of the function header (and before the body). The placement of type annotations for the *function parameters* also changes here.

In the case that a function returns nothing, note that in Java, we specify the return type to be `void`. We can do this in TypeScript too, however it is optional. Both including `: void` or not is valid. For example:

<table>
<tr><th width="520">Java</th><th width="520">TypeScript</th></tr>
<tr>
<td>
 
```java
void doSomething() {
 // Implementation Not Shown
}








```

</td>
 <td>
  
```ts
function doSomething() {
 // Implementation Not Shown
}

// OR

function doSomething(): void {
 // Implementation Not Shown
}
```

</td>
</tr>
</table>

### Arrow Functions

TypeScript also has a tremendously useful feature called **arrow functions**. Arrow functions are a more compact and concise method of defining traditional functions. Let's take a look at a function from above as a *traditional function* and one as an *arrow function*.

<table>
<tr><th width="520">Traditional Function</th><th width="520">Arrow Function</th></tr>
<tr>
<td>
 
```ts
function greet(name: string): string {
 return "Welcome, " + name + "!";
}
```

</td>
 <td>
  
```ts
let greet = (name: string): string => {
 return "Welcome, " + name + "!";
}
```

</td>
</tr>
</table>

There are a few things to unpack here. First, it looks like we are ultimately assigning *"something"* to a *variable.* We use the `let` keyword and we provide a variable name! On the right, we have a weird structure that would go in the *value* spot of our variable formula.

In fact, this is exactly what we are doing. We are saving a *function* to a variable and giving it a name that we can use to call it. In the `( )`, we provide the parameters to the function. We provide a return type in the type annotation as well. Then, we use `=>` to connect these parameters to a *function body*.

We can then call our function in the same way we would normally, like so:
```ts
greet("Kris");
```

While this seems like just a syntactic change, the implications of this are ***massive*** and opens the door to an entire new world of programming called **functional programming**, as we can pass around functions as values. This is something that we will be covering *extensively* throughout this course, however it is super important to become familiar with the arrow function syntax now so it is less suprising later!

To conclude this section, provide two important caveats must be emphasized:
* Arrow functions don't have their own bindings and therefore should not be used as methods.
* Arrow functions cannot be used as constructors. Calling them with new throws a `TypeError`.

These caveats are important to note because traditional functions and arrow functions are not *exactly* the same, and there are some semantic differences.

### Class and Interface Construction

### Extra TypeScript Features
 - Comments
 - Printing
 - Enums
 - Type aliases
 - Ternary operator

## Exercises
