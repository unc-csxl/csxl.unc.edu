# Angular Resolvers

> Written by Ajay Gandecha for the CSXL Web Application and for COMP 423: Foundations of Software Engineering.
> _Last Updated: 11/17/2023_

## Preface

Imagine that we are trying to load the list of all CSXL organizations into the `OrganizationPageComponent`. To do this, we would first need to call on on the `OrganizationService` Angular service class - specifically the `.getOrganizations()` method.

Recall that your service functions return _observables_. If we examine the method signature of the `OrganizationService.getOrganizations()` method, it looks like the following:

```ts
getOrganizations(): Observable<Organization[]>
```

As you can see, our list of organizations is wrapped in an `Observable` object. So, in order to access the data from this call, we would need to subscribe to it and access its value.

Let's take a look at the following code snippet from our component:

**In `organization-page.component.ts`**

```ts
@Component({
  selector: "organization-page",
  templateUrl: "./organization-page.component.html",
  styleUrls: ["./organization-page.component.css"],
})
export class OrganizationPageComponent {
  // Route object and other fields hidden.

  /** Store Observable list of Organizations */
  public organizations$: Observable<Organization[]>;

  /** Store unwrapped list of Organizations */
  public organizations: Organization[] = [];

  /** Initializer for the component */
  constructor(private organizationService: OrganizationsService) {
    // Load the organizations observable
    this.organizations$ = this.organizationService.getOrganizations();

    // HERE:
    // Subscribe to the observable to obtain list of organizations
    this.organizations$.subscribe((organizations) => {
      // Update our field
      this.organizations = organizations;
    });
  }
}
```

You notice that in the code above, we have to _subscribe_ to `organization$`, the observable returned from the `.getOrganizations()` service function, in order to access our data. However in many cases, especially where you are reading data that is not updating constantly, where this manual tussle with `Observable`s and subscriptions does not seem to idiomatic.

What if there was a way to _pre-load_ this data so that we can access it immediatley without having to manage subscriptions?

**Enter the Angular Resolver.**

**Angular Resolvers** allow you to _preload_ data into your Angular components so that they are accessible _before_ construction. This is immensely useful, easy to set up, and more convenient than subscribing to Angular service methods. Resolvers are used throughout the CSXL application to load various pieces of data, from the currently-logged-in profile to organizations and event data.

In this lesson, you will learn how to create your own Angular Resolvers and add them to your components.

## Creating Resolvers

## Using Resolver Data in Components

## Access Route Parameters in the Resolver

## Error Handling with Resolvers

## Conclusion
