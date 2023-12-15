# TypeScript For the COMP 301 Java Developer

> Written by Ajay Gandecha for the CSXL Web Application and for COMP 423: Foundations of Software Engineering.<br>
> *Last Updated: 12/14/2023*

## Preface

**Welcome to COMP 423!** 🥳 During your career at UNC, you likely started out in COMP 110 learning the *Python* programming language. In COMP 210, you transitioned to Java and learned how to organize your code using classes and common data structures. In COMP 301, you built off of this idea and learned more about useful language features to help you gain a foundational toolbox to approach software engineering problems.

This course aims to teach you the *foundations of full-stack software engineering*. Full-stack development involves the development of a *frontend*, or an application (web, mobile, etc) that a user interacts with, as well as a *backend* running on a server that helps to support your frontend and provide data to it. 

Since this course is focused on developing full-stack *web* applications, you need to gain familiarity with the programming languages and tools needed to build high quality web apps. **JavaScript** is the *leading programming language that powers the web* and web applications. According to the **[2023 StackOverflow Developer Survey](https://survey.stackoverflow.co/2023/#technology-most-popular-technologies)**, developers ranked JavaScript as their most commonly-used programming language - an ***eleven-year long streak** and counting!*

In this course, we will use **TypeScript** to build out the frontend of our web applications. TypeScript is a *superset* of JavaScript - it adds on static typing with optional type annotations to JavaScript, meaning that writing code and keeping data types consistent is significantly easier. Because of its type safety features, it is designed for the development of large applications - it even transpiles to JavaScript!

TypeScript shares some similarities to Java - both are compiled languages, both support object-oriented programming. However, there are many key differences (including their purpose, how they are compiled, etc). You will learn more about these features throughout the course. 

This document is designed to help you become familiar with the syntax and features of TypeScript from the context of the Java experience you all have had in COMP 301. It compares the syntax between Java and TypeScript in various situations and should serve as a guide going into the first few weeks of the semester.

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

Let's compare a number declaration in Java and TypeScript, then compare more generally.

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
names = ["Aziz", "Andrew"]
# Add values
names.append("Jordan")
# Replace a value
names[2] = "Kris"
# Access a value
aziz = names[0]




```

</td>
 <td>

  ```java
// Initialize
List<String> names = new ArrayList<>();
names.add("Aziz");
names.add("Andrew");
// Add values
names.add("Jordan");
// Replace a value
names.set("Kris", 2);
// Access a value
String aziz = names.get(0);
```

</td>
<td>

```ts
// Initialize
let names: string[] = ["Aziz, "Andrew"]
// Add values
names.push("Jordan");
// Replace a value
names[3] = "Kris";
// Access a value 
let aziz: string = names[0];




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
<tr><th width="520">TypeScript - Traditional Function</th><th width="520">TypeScript - Arrow Function</th></tr>
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
greet("Jade");
```

While this seems like just a syntactic change, the implications of this are ***massive*** and opens the door to an entire new world of programming called **functional programming**, as we can pass around functions as values. This is something that we will be covering *extensively* throughout this course, however it is super important to become familiar with the arrow function syntax now so it is less suprising later!

To conclude this section, provide two important caveats must be emphasized:
* Arrow functions don't have their own bindings and therefore should not be used as methods.
* Arrow functions cannot be used as constructors. Calling them with new throws a `TypeError`.

These caveats are important to note because traditional functions and arrow functions are not *exactly* the same, and there are some semantic differences.

### Class and Interface Construction

**Classes** define data types and are the foundation of object-oriented programming. It will be critical for you to be comfortable working within TypeScript classes throughout your time in COMP 423! While there are many syntax differences between classes in Java and TypeScript, the *core idea* and motivation for using them remains the same. Below is an example of a full class in both Java and TypeScript. I recommend that you read this in its entirely and try to compare line by line! From there, we will go through each section.

<table>
<tr><th width="520">Java</th><th width="520">TypeScript</th></tr>
<tr>
<td>
 
```java
/** Represents a UNC Student. */
public class Student {

 /* Fields
 * NOTE: In COMP 301, you learned about using the
 * `private` keyword on fields to control access
 * via getter and setter methods. For this example,
 * I am making some fields public and others private.
 */

 /** Represents the name of the student */
 public String name;
 /** Represents the year of the student*/
 public int year;
 /** Represents the address of the student */
 private String address;

 /* Constructor */
 public Student(String name, int year, String adr) {
  this.name = name;
  this.year = year;
  this.address = adr;

  this.welcome();
 }

 /* Methods */

 /** Prints a welcome message to the console. */
 public void welcome() {
  System.out.println("Hello, " + this.name + "!");
 }

 /** Converts a year number to a description. */
 public static String yearToString(int year) {
  if(year == 1) {
   return "Freshman";
  }
  else if(year == 2) {
   return "Sophomore";
  }
  else if(year == 3) {
   return "Junior";
  }
  else if(year == 4) {
   return "Senior";
  }

  return "Oops...";
 }
}
```

</td>
 <td>
  
```ts
/** Represents a UNC Student. */
public class Student {

 /* Fields
 * NOTE: In COMP 301, you learned about using the
 * `private` keyword on fields to control access
 * via getter and setter methods. For this example,
 * I am making some fields public and others private.
 */

 /** Represents the name of the student */
 public name: string;
 /** Represents the year of the student*/
 public year: number;
 /** Represents the address of the student */
 private address: string;

 /* Constructor */
 constructor(name: string, year: int, adr: string) {
  this.name = name;
  this.year = year;
  this.address = adr;

  this.welcome();
 }

 /* Methods */

 /** Prints a welcome message to the console. */
 public welcome() {
  console.log("Hello, " + this.name + "!");
 }

 /** Converts a year number to a description. */
 public static yearToString(year: number): string {
  if(year == 1) {
   return "Freshman";
  }
  else if(year == 2) {
   return "Sophomore";
  }
  else if(year == 3) {
   return "Junior";
  }
  else if(year == 4) {
   return "Senior";
  }

  return "Oops...";
 }
}
```

</td>
</tr>
</table>

As you can see, there are a few similarities between classes in Java and TypeScript! First, we can look at *access modifiers*. The `public`, `private`, and `protected` keywords are the ***same*** in both Java and TypeScript.

Notice that the fields are the same conventions as well! Note however that the `let` keyword is ***not used*** when defining fields - it is only needed when defining regular variables.

The constructor also differs a bit. In TypeScript, the `constructor` keyword replaces `public ClassName` from Java! The type annotations in the parameters also follow the normal conventions of TypeScript functions.

Lastly, like fields, *methods* in TypeScript also do ***not*** use their respective keyword (`function`) to be defined. Instead, we can just provide an access modifier.

We use the `static` keyword to denote class methods the same way in both Java and TypeScript. Learn more about class fields and methods [here](https://www.tutorialsteacher.com/typescript/typescript-static).

Within a function, we also have access to the `this` keyword that references the current object.

Now, how do we ***instantiate*** objects?

We actually use the same syntax as in Java:

<table>
<tr><th width="520">Java</th><th width="520">TypeScript</th></tr>
<tr>
<td>
 
```java
Student noah = new Student("Noah", 3, "Columbia St");
```

</td>
 <td>
  
```ts
noah: Student = new Student("Noah", 3, "Columbia St");
```

</td>
</tr>
</table>

We can also define interfaces in TypeScript like we do in Java. Take a look at the following:

<table>
<tr><th width="520">Java</th><th width="520">TypeScript</th></tr>
<tr>
<td>
 
```java
public interface Person {
 String name;
}

public class Student implements Person { /* ... */ }
```

</td>
 <td>
  
```ts
public interface Person {
 name: String;
}

public class Student implements Person { /* ... */ }
```

</td>
</tr>
</table>

As you can see, the keywords remain the same between both languages with `interface` and `implements`! The only difference between the two languages are with variable creation and type annotation conventions.

There is also another interesting feature of TypeScript worth mentioning here.

TypeScript is a ***structural language***. This means that TypeScript views object as equivalent types *if they share the same structure*, NOT just the same name! On the otherhand, Java is a ***nominal language***, which means it views objects as equivalent types if they share the same name ONLY (or if there is an inheritence relationship).

So, we can *technically* directly create a value of type `Person` in TypeScript! This is not something you can directly do in Java without creating a subclass. The syntax would look like so:

<table>
<tr><th width="520">TypeScript</th></tr>
<tr>
<td>
 
```ts
person: Person = {
 name: "Charles"
}
```

</td>
</tr>
</table>

In this example, we use JSON (JavaScript object notation) to *create an object of data* that contains the *same properties* that a `Person` objct should have. Suprisingly enough, due to TypeScript being a structural language, this ***is a valid way to instantiate a `Person` object!***

This distinction is pretty cool, and it allows us to do some interesting things with TypeScript. We will explore this more throughout COMP 423.

### Extra TypeScript Features

#### Comments

The examples throughout this document have already used many comments, however we create comments in Java and TypeScript in the exact same way! This is shown below:

<table>
<tr><th width="520">Java</th><th width="520">TypeScript</th></tr>
<tr>
<td>
 
```java
// This is a single-line comment.

/*
This is an example of a
multi-line comment!
*/
```

</td>
 <td>
  
```ts
// This is a single-line comment.

/*
This is an example of a
multi-line comment!
*/
```

</td>
</tr>
</table>

#### Printing Values

In Java and TypeScript, we have statements to print out values! In TypeScript, values are printed to the *console*. We use the following convention to print values:

<table>
<tr><th width="520">Java</th><th width="520">TypeScript</th></tr>
<tr>
<td>
 
```java
String taName = "Jean";
System.out.println(taName);
// Output:
// >> Jean
```

</td>
 <td>
  
```ts
let taName = "Jean";
console.log(taName);
// Console:
// >> Jean
```

</td>
</tr>
</table>

As you can see, we use `console.log()` to print out values to the console in TypeScript.

#### Enums

Enums (enumerators) are an extremely useful language feature in many programming languages! Enums allow you to define custom, related values or states. Think of enums as implementing a multiple-choice question, where there are many options! Let's a look at an example:

<table>
<tr><th width="520">TypeScript</th></tr>
<tr>
<td>
 
```ts
enum Direction {
  Up,
  Down,
  Left,
  Right,
}
```

</td>
</tr>
</table>

Let's look at the `Direction` enum applied in a TypeScript function:

<table>
<tr><th width="520">TypeScript</th></tr>
<tr>
<td>
 
```ts
function directionToText(direction: Direction): string {
 if(direction == Direction.Up || direction == Direction.Down) {
  return "Let's go vertically!"
 }
 else if (direction == Direction.Left || direction == Direction.Right) {
  return "Let's go horizontally!"
 }
}
```

</td>
</tr>
</table>

Enumerations will be extremely useful in your final projects to model data.

#### Type Aliases

There is a nifty feature in TypeScript called the **type alias**, which essentially allows you to create another label why which you can refer to a type. This can be useful to make types more concise, or to make it more readable for your feature. Look at the following example:

<table>
<tr><th width="520">TypeScript</th></tr>
<tr>
<td>

```ts
type Rating = number;
 
let csxlRating: Rating = 10;
```

</td>
</tr>
</table>

Using the `type` keyword, we give `number` an alias as `Rating`. Now, we can use `number` and `Rating` interchangeably. Next, we create a variable called `csxlRating` of type `Rating` (which is really just type `number`), and then assign a number to it.

#### Ternary Operator

The last super useful feature of TypeScript I wanted to feature here is the **ternary operator**. The ternary operator allows you to *conditionally assign a value to a variable!* This means that if a condition is true, I can assign one value - and if false, I can assign the other.

The ternary operator uses the following syntax:
`condition ? value if true : value if false`

Let's look at an example relating to the CSXL site:

<table>
<tr><th width="520">TypeScript</th></tr>
<tr>
<td>

```ts
// Stores the hour which the CSXL opens.
// For sake of example, say the CSXL opens at 10am on weekdays and 12pm on weekends:
let csxlOpeningHour: number = isWeekday ? 10 : 12;

console.log(csxlOpeningHour);

// Output IF isWeekday = true:
// >> 10
// Output IF isWeekday = false:
// >> 12
```

</td>
</tr>
</table>

Ternary operators are *extremely useful* and are used numerous times throughout the CSXL application. I highly recommend checking out the codebase and searching for `?` / `:` to see more relevant examples!

#### Generic Types

**Generic types** are a powerful convention in Java that allows you to pass types *as a parameter* into objects. This makes objects support multiple data types.

For example, take a `LinkedList` implementation in Java. Linked lists are data structures that can store *many different types of values*. For example, look at the following in *Java*:

<table>
<tr><th width="520">Java</th></tr>
<tr>
<td>

```java
// Create a linked list that stores strings.
LinkedList<String> myStringList = new LinkedList<>();
// Create a linked list that stores students.
LinkedList<Student> myRoster = new LinkedList<>(); 
```

</td>
</tr>
</table>

The above Java syntax likely looks vaguely familiar! Here, we are creating two linked lists - one of `String` objects and the other of `Student` objects. We pass the data type of the object we want to store into the `< >` part of the type annotation.

**TypeScript also supports generic types!** This is a feature that will be used a lot throughout this course. First, let's compare the syntax for creating the hypothetical lists shown above:

<table>
<tr><th width="520">Java</th><th width="520">TypeScript</th></tr>
<tr>
<td>
 
```java
// Create a linked list that stores strings.
LinkedList<String> myStringList = new LinkedList<>();
// Create a linked list that stores students.
LinkedList<Student> myRoster = new LinkedList<>(); 
```

</td>
 <td>
  
```ts
// Create a linked list that stores strings.
let yStringList: LinkedList<String> = new LinkedList<>();
// Create a linked list that stores students.
let myRoster: LinkedList<Student> = new LinkedList<>(); 
```

</td>
</tr>
</table>

As you can see, the only thing different between both code snippets are how we declare the variable! The usage of `< >` remains the same.

Now, how would we actually *implement* the `LinkedList<T>` class? Let's compare two rudimentary implmentations in both Java and TypeScript:

<table>
<tr><th width="520">Java</th><th width="520">TypeScript</th></tr>
<tr>
<td>
 
```java
/** Represents a linked list node. */
public class LinkedList<T> {

 /** Value for the node. */
 private T value;
 /** Next node, if it exists. */
 private LinkedList<T> next;

 /** Constructor */
 public LinkedList(T value) {
  this.value = value;
 }

 /** Returns the value of the node. */
 public T getValue() {
  return this.value;
 }

/* Modifies the value of the node. */
 public void setValue(T value) {
  this.value = value;
 }

 /* Other methods not shown */
}
```

</td>
 <td>
  
```ts
/** Represents a linked list node. */
public class LinkedList<T> {

 /** Value for the node. */
 private value: T;
 /** Next node, if it exists. */
 private next: LinkedList<T>;

 /** Constructor */
 constructor(value: T) {
  this.value = value;
 }

 /** Returns the value of the node. */
 public getValue(): T {
  return this.value;
 }

/* Modifies the value of the node. */
 public setValue(value: T) {
  this.value = value;
 }

 /* Other methods not shown */
}
```

</td>
</tr>
</table>

In the header of the class, we put `<T>`, which specifies that we are adding a *type parameter*! Whenever this is then provided, like in `LinkedList<String>` or `LinkedList<Student>`, the `T` used throughout the class is then replaced by the type that is provided! So in the `LinkedList<String>` example, the field `value` becomes of type `String`. In the `LinkedList<Student>` example, the field `value` becomes of type `Student`.

If this concept is unfamiliar, we highly recommend to practice using generic types in classes, as well as experimenting on your own! Generic types are an invaluable tool to make code extendable to multiple use-cases, and is used in many of the packages we are going to use throughout the course.

## Conclusion

Congratulations! 🎉 TypeScript is an extremely powerful and useful language, and we you will have the chance to work with TypeScript code this entire semester. If you are having trouble remembering TypeScript syntax, feel free to return to this document at any time. In addition, for practice, we highly recommend you go to the official [TypeScript playground](https://www.typescriptlang.org) or open a new [Repl.it](https://replit.com) ! The TypeScript playground, as well as opening a `.ts` TypeScript file in [Visual Studio Code](https://code.visualstudio.com) and playing around with it, are some of the best ways to get more familiar and accustomed to using the language. As you have seen throughout your computer science careers so far, sometimes the best way to learn is to dive right in!

In addition, below are some additional resources that you may find useful as your work through learning TypeScript.

## Extra Resources

* [Official TypeScript Cheat Sheets](https://www.typescriptlang.org/cheatsheets)
* [Official Docs - TypeScript for the Java Programmer](https://www.typescriptlang.org/docs/handbook/typescript-in-5-minutes-oop.html)


