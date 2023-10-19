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



### Widgets vs. Components

### Using Widgets in Components


## Widgets in the Module


## How Widgets Work

### Pass Data into Widgets Using Inputs


### Outputting Data From Widgets


## Conventions For Creating a Widget


## Further Reading


