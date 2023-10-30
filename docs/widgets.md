# Crash Course on Angular Widgets

> Written by Ajay Gandecha for the CSXL Web Application and for COMP 423: Foundations of Software Engineering.<br>
> *Last Updated: 10/19/2023*

## Introduction

If you have begun to explore the frontend of the CSXL web application, you may have noticed a new frontend convention being used that you probably have not seen before - widgets! Widgets are an extremely useful convention that makes your Angular frontend more *versatile* and *modular*.

In Angular, **widgets are *individual*, *resuable* user interface elements that can be easily integrated into the UI of your Angular components!** Widgets essentially abstract frontend UI elements to simplify Angular compponents, enhance user experience, and make the development process in Angular less painful.

Take the following example:
![organization page](https://github.com/unc-csxl/csxl.unc.edu/blob/main/docs/images/org-page.png)

Above is the *Organization component* of the CSXL site ([view live here](https://csxl.unc.edu/organizations)). As you can see, the page contains a lot of elements - namely a *search bar* and also individual *organization cards* that display relevant information about CS Department-affiliated student organizations.

Say we wanted to look at the HTML structure of the organization page. You would likely expect it to look something like the sample code below:

```html
<div class="container">

  <!-- Search Bar -->
  <div class="search-bar-container">
    <mat-form-field class="search-bar" appearance="outline" color="accent">
      <mat-label>Search</mat-label>
      <input matInput type="text" [(ngModel)]='searchBarQuery' (ngModelChange)="onTextChanged()">
      <!-- HIDDEN : Search icon code not shown -->
    </mat-form-field>
  </div>

  <!-- Organizations -->
  <div class="organization-grid">
    <mat-card class="organization-card" *ngFor="let organization of organizations">
      <!-- HIDDEN: Organization Header Section not shown -->
      <!-- HIDDEN: Organization Description Section not shown -->
      <!-- Social Media Icons -->
      <!-- Email -->
      <a href={{href}} target="_blank">
          <button mat-icon-button color="basic">
            <mat-icon fontIcon="email" svgIcon="email"></mat-icon>
          </button>
      </a>
      <!-- HIDDEN: Instagram, Link, LinkedIn Icons not shown -->
    </mat-card>
  </div>
</div>
```

As you can see, this HTML structure is quite complex! Not only is there a lot of code here, but actually most of the code has been hidden from you in the example above. This makes parsing the HTML of the Organizations Component extremely difficult.

In addition, you may be begin to notice a few problems - namely with certain elements such as the search bar and social media icons. These components are actually repeated on many different pages. For example, the search bar component is also used on the events page ([view live here](https://csxl.unc.edu/events)), and social media icons are used on the organization detail pages ([view live here](https://csxl.unc.edu/organizations/cads)).

This means that all of these components would then need to to have duplicate HTML, styles (CSS), and even functionality (TS) to share these common elements across pages. Worse yet, if you wanted to change one of these elements, you then need to update them on every single page, which is far less than optimal. ***This is where widgets come in***.

We can convert commonly-shared elements into widgets and *abstract them out* of our component! For example, say we created a `<search-bar>` widget and a `<social-media-icon>` widget. Our HTML would then shorten to look like:

```html
<div class="container">

  <!-- Search Bar -->
  <!-- NOTE: Widget parameters not shown -->
  <search-bar />

  <!-- Organizations -->
  <div class="organization-grid">
    <mat-card class="organization-card" *ngFor="let organization of organizations">
      <!-- HIDDEN: Organization Header Section not shown -->
      <!-- HIDDEN: Organization Description Section not shown -->
      <!-- Social Media Icons -->
      <!-- Email -->
      <social-media-icon icon="email">
      <!-- HIDDEN: Instagram, Link, LinkedIn Icons not shown -->
    </mat-card>
  </div>
</div>
```

We can even create a widget called `<organization-card>` that abstracts out the code for each organiztaion card! Look at the resulting code:

```html
<div class="container">

  <!-- Search Bar -->
  <!-- NOTE: Widget parameters not shown -->
  <search-bar />

  <!-- Organizations -->
  <div class="organization-grid">
    <organization-card *ngFor="let organization of organizations" [organization]="organization" />
  </div>
</div>
```

Look how much cleaner that is! It is now a lot more clear how our organization component is structured, and it becomes *a lot easier* for us to select certain elements that we want to edit. In addition, we can now reuse the `<search-bar>` widget, for example, across many parts of the application!

In summary, the wireframe for our Organization would look as follows:

![wireframe](https://github.com/unc-csxl/csxl.unc.edu/blob/main/docs/images/wireframe.jpeg)


## Widgets in the Module

Before we take a look at how these widgets are created, we need to first become aware of how these widgets are actually loaded and where they are located within the Angular App Module. To be able to understand this fully, we need to go over a quick review of Angular Modules.

**Angular Modules *define the application's structure* and help to manage dependencies in an Angular application.** The module organizes and encapsulate components, services, and other code related to a specific feature or functionality.

Throughout all of your projects in COMP 423 so far, your project has only included the singular `App Module` located in `app.module.ts` in the root directory of your project. The App Module then contains all of your *components*, *services*, *models*, and other code. 

**However, this is not necessarily the best approach.** Consider what actually happens when you load your application on the browser. The application loads the entire module and all of its declarations. This is not optimal on large projects, such as the CSXL web application (and of course larger projects than this). Having all of your code and all of your features in one module means longer load times and more resources to download for your users.

Instead, **it is better to encapsulate your features into separate modules**. For example, the CSXL Web Application has the `Organization Module` (defined in `organization.module.ts`) and the `Event Module` (`event.module.ts`) to encapsulate their respective features into standalone bundles. When the user navigates to the Organization page, only the `Organization Module` and what is necessary for that to run will be loaded. The app still has the `App Module` to ultimately ensapculate the application.

Why do we care about this? Well, we emphasized that widgets are meant to be *reusable across the application*. If we separate our code into separate modules, then where do we put widgets? **We can only declare widgets in one place, so we need to choose which module to use.**

Take the example above. We defined *three different widgets* - `<search-bar>`, `<organization-card>`, and `<social-media-icon>`. Let's think about the use cases for each of these widgets:

- `<search-bar>`: Defines a search bar item to be *used throughout the application.*
- `<organization-card>`: Defines a card to show organization data *on organization pages.*
- `<social-media-icon>`: Defines social media icon buttons to be *used throughout the application.*

As you can see, we can separate these into two different categories:

| Used Locally | Used Globally |
| ----------- | ----------- |
| `<organization-card>`| `<seach-bar>` |
|  | `<social-media-icon>`   |

So, which modules should we declare these widgets in?

It may be much more obvious for the `<organization-card>` widget! We said this widget will only be used for the organization pages, therefore it can be stored in the `Organization Module`.

But, what about the other two components? Well, you would likely immediately think of the global `App Module` as a good place to put it. However, the problem with this solution. *In order for components in other modules to access widgets in the App Module, the module has to import the App Module.* This actually completely defeats the purpose of having separate modules, because now you are ultimately importing the App Module and loading everything inside anyway.

The solution to this problem is to have a new `Shared Module` (defined in `shared.module.ts`) that **just contains Angular widgets** and other Angular Material components. Then, modules that use global widgets just have to import the Shared Module and will then have access to the widgets ***without*** importing everything in App Module.

Ultimately, this relationship looks like:

![widgets in modules](https://github.com/unc-csxl/csxl.unc.edu/blob/main/docs/images/widget-modules.jpeg)

## How Widgets Work

### Creating a Widget

Now that you have been introduced into Angular Widgets and hopefully understand how widgets are declared in modules conceptually, let's get into actually creating widgets.

There is no command in Angular to generate widgets in the same way there is with components (using `ng generate component`). Instead, we have to do this step manually. However, the setup is extremely easy. 

First, it is important to note that, like components, widgets require **three files** to be declared:
- HTML File: Defines the structure of the widget
- CSS File - Defines the style of the widget
- TS File - Defines the functionality of the widget

In either the `/widgets` folder in a module folder (like `/organizations/widgets`) or in the `/shared` folder for the shared module, you want to create a folder to contain all of your widget files. It should have this structure:
```
widget-name
  |- wiget-name.widget.css
  |- widget-name.widget.html
  |- widge-name.widget.ts
```

Then, *open the TS file you created.*

Just like with Angular components, the TS file actually ultimately defines and creates your widget. You can use the template below to quickly create your widget:

**Angular Widget Template For TypeScript**

```ts
@Component({
    selector: 'widget-name',
    templateUrl: './widget-name.widget.html',
    styleUrls: ['./widget-name.widget.css']
})
export class WidgetName {

  /** Inputs and outputs go here */

  /** Constructor */
  constructor() { }
}
```

There are a few things to note with this template. First is the `selector` property passed into the `@Component` decorator. Note that this is what you will use to refer to your widget in HTML! So, in a component's HTML, you would call this widget using `<widget-name />`. 

Second, once you create the template, ***you must declare it in a module!!*** Follow the steps in the previous part to determine whether your widget will be globally or locally used. Then, in the correct Modules file, add it to the list for the `declarations` property in the `@NgModule` decorator.


### Pass Data into Widgets Using Inputs

The great thing about Angular Widgets is that we can *pass data* into them! For example, in the example above with `<organization-card>`, we want to be able to pass in the *organization* to show in the card as a parameter. Setting up inputs are extremely easy in Angular widgets. 

We use the `@Input` decorator in class fields to accomplish this. See the example below:

```ts
@Component({
    selector: 'organization-card',
    templateUrl: './organization-card.widget.html',
    styleUrls: ['./organization-card.widget.css']
})
export class OrganizationCard {

  /** Organization to show */
  @Input() organization!: Organization

  /** Constructor */
  constructor() { }
}
```

> *Note the usage of the `!` unwrap operator in the code block above! Including this ensures to TypeScript that the organization field is required and will be passed into it upon construction. Failure to provide an input will cause an error.*

Now, in the `organization-card.widget.html` file, we can use the `{{organization}}` variable in the same way you would in the HTML for a component!

How would be use this in a component? We can pass inputs in directly to the HTML, like so:

```html
<organization-card [organization]="organization" />
```

**Note that the `[ ]` syntax denotes an INPUT in Angular!**

We can also expand this and combine it with `*ngFor`, assuming `organizations` is a list of `Organization`s:

```html
<organization-card [organization]="organization" *ngFor="let organization of organizations" />
```

This is the exact implementation used for the organization page! See for yourself in the `organization-page.component.html` file.

### Event Binding to Send Data From Widgets to Components

There is a problem here with widgets that you may have already been thinking ahead about. *What about button actions?* For example, say we had a "join organization" button on each `organization-card` widget. *How can we get this button to trigger a function in the parent component?*

For this, we can use the `@Output` decorator! While slightly more complicated than inputs, outputs for widgets are extremely powerful and useful to connect widgets to their parent components.

**The big idea here is that we need a way to *pass data* from widgets back to components** - the reverse of what we were doing with `@Input()`. That way, the parent component can run functions *using the output of the widget*.

Let's recall a normal Angular button. You would define an action like so:

```html
<button (click)="myAction()">Click me</button>
```

**Note that the `( )` syntax denotes an Event Binding in Angular!**

What is actually happening here? In this example, whenever the button is pressed, the function passed into `(click)` is run. The `(click)` event and the `myAction()` function are being bound together.

This will not make too much sense without a relevant example.

Say that in the Organization Component, we define a function `joinOrganization(org: Organization)` that we want to run whever we press the join button for a specific organization. 

Recall that the Organization Component still has many Organization cards as before, and the "Join Org" button would be on each *widget* rather than in the component directly. So, we need to define some way that the Organization Component knows which organization to join when one of these buttons is pressed.

In our ***widget***, we want to define an output field.

**organization-card.widget.ts**
```ts
@Component({
    selector: 'organization-card',
    templateUrl: './organization-card.widget.html',
    styleUrls: ['./organization-card.widget.css']
})
export class OrganizationCard {

  /** Organization to show */
  @Input() organization!: Organization

  /** Handler for when the join button is pressed */
  @Output() joinButtonPressed = new EventEmitter<Organization>()

  /** Constructor */
  constructor() { }
}
```

There is a decent amount to unpack here - first, the use of `EventEmitter`. You can see that it takes a generic type of `Organization` in a similar way that `Observables` do. ***We want to set this up so that when the join button is pressed, this event emitter will emit some data to the component.***

Before we do that step, let's look at what this would look like in the component's HTML now:

**organization-page.component.html**
```html
<organization-card
  [organization]="organization"
  (joinButtonPressed)="/* SOMETHING HERE */"
  *ngFor="let organization of organizations"
  />
```

We can see that we now have access to this `(joinButtonPressed)` output! Looks like `<button>`'s `(click)`, right? You would probably want to put the component's `joinOrganization(org: Organization)` in here now, which is the correct idea!

```html
<organization-card
  [organization]="organization"
  (joinButtonPressed)="joinOrganization(org: /* What goes here??? */)"
  *ngFor="let organization of organizations"
  />
```

But, what would our organization input be?

Again, go back to the widget's HTML. Like we said before, *we want to set this up so that when the join button is pressed. this event emitter will emit some data to the component.*

We can actually connect the button's `(click)` handler to emit this data.

**organization-card.widget.ts**
```html
<mat-card>
  <!-- Implmentation not shown -->
  <button (click)="joinButtonPressed.emit(organization)">Join Org</button>
</mat-card>
```

Now, the *button is pressed*, the organization clicked on will be *emitted* out to the component!

In our main component, we can now access this emitted variable using `$event`, like so:

**organization-page.component.html**
```html
<organization-card
  [organization]="organization"
  (joinButtonPressed)="joinOrganiation($event)"
  *ngFor="let organization of organizations"
  />
```

This is perfect! Now, when the button in the *widget* is pressed, it *emits* the organization out of the widget into this variable called `$event`, which is then used as the parameter for `joinOrganization` in the component! We just sent data from our widget to the component that contains it.

## Conclusion - Widgets vs. Components

Congratulations! You have made it to the end of the widgets crash course! While it is optional to use widgets in your final project, they would be **extremely useful** to implement and would be considered a best practice to properly organize and encapsulate your code.

The one thing that is important to take away from these notes is the difference between *widgets* and *components* in Angular. The differences can be summarized below:

|  | Widgets | Components |
| ----------- | ----------- | ----------- |
| **Purpose** | Widgets are indiviual UI elements that can be reused. | Components are entire pages in the Angular application, containing many elements and widgets. |
| **Reusability** | Widgets can be used *numerous times* within the same component and throughout the application. | Components are used **only once** in your application and represent a page. |
| **Declaration** | Wigets can either be declared in *feature* modules or the *shared* module depending on use case. | Components are usually declared in *feature* modules or the *app* module, but never the *shared* module. |
| **Routing** | Since widgets are individual elements and not pages, they do not have a route and do not connect to any routing modules. | Since components are pages, they do have routes (URLs) and are connected to their respective routing modules. |


## Further Reading
- Official Angular Documentation - [Using `@Input` and `@Output`](https://angular.io/guide/inputs-outputs)
- Official Angular Documentation - [Event Bindings](https://angular.io/guide/event-binding)
- Official Angular Documentation - [Angular Modules](https://angular.io/guide/architecture-modules)
