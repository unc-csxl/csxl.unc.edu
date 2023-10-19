# Angular Widgets

> Written by Ajay Gandecha for the CSXL Web Application and for COMP 423: Foundations of Software Engineering.<br>
> *Last Updated: 10/19/2023*

## Introduction

If you have begun to explore the frontend of the CSXL web application, you may have noticed a new frontend convention being used that you probably have not seen before - widgets! Widgets are an extremely useful convention that makes your Angular frontend more *versatile* and *modular*.

### What is a Widget?

In Angular, **widgets are *individual*, *resuable* user interface elements that can be easily integrated into the UI of your Angular components!** Widgets essentially abstract frontend UI elements to simplify Angular compponents, enhance user experience, and make the development process in Angular less painful.

Take the following example:

[[ IMAGE HERE ]]

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

[[ IMAGE HERE ]]

## Widgets in the Module

Before we take a look at how these widgets are created, we need to first become aware of how these widgets are actually loaded and located within the Angular App Module. To be able to understand this fully, we need to go over a quick review of Angular Modules.

**Angular Modules *define the application's structure* and help to manage dependencies in an Angular application.** The module organizes and encapsulate components, services, and other code related to a specific feature or functionality.

Throughout all of your projects in COMP 423 so far, your project has only included the singular `App Module` located in `app.module.ts` in the root directory of your project. The App Module then contains all of your *components*, *services*, *models*, and other code. 

**However, this is not necessarily the best approach.** Consider what actually happens when you load your application on the browser. The application loads the entire module all all of its declarations. This is not optimal on large projects, such as the CSXL web application (and of course larger projects than this). Having all of your code and all of your features in one module means longer load times and more resources to download for your users.

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

But, what about the other two components? Well, you would likely immediately think of the global `App Module` as a good place to put it. However, the problem with this solution is that if declare this widget in the App Module, *in order for components in other modules to access widgets in App Module, the module has to import App Module.* This actually completely defeats the purpose of having separate modules, because now you are ultimately importing the App Module and loading everything regardless.

The solution to this problem is to have a new `Shared Module` (defined in `shared.module.ts`) that **just contains Angular widgets** and other Angular Material components. Then, modules that use global widgets just have to import the Shared Module and will then have access to the widgets ***without*** importing everything in App Module.

Ultimately, this relationship looks like:

[[ IMAGE HERE ]]


## How Widgets Work

### Pass Data into Widgets Using Inputs


### Outputting Data From Widgets


## Conventions For Creating a Widget

## Widgets vs. Components

It is important to diffe

## Further Reading


