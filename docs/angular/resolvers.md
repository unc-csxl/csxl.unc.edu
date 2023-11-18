# Angular Resolvers

> Written by Ajay Gandecha for the CSXL Web Application and for COMP 423: Foundations of Software Engineering.<br>_Last Updated: 11/18/2023_

## Preface

Throughout COMP 423 so far, you have learned about subscribing to `Observable`s to load the data results from your API calls. Your Angular Service functions are responsible to calling the APIs you expose in your backend - and these service functions return `Observable` objects. Then, your Components can *subscribe* to these `Observable`s to access the actual data they hold.

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
  /** Route information to be used in the Routing Module */
  public static Route = {
    path: '',
    title: 'CS Organizations',
    component: OrganizationPageComponent
  };

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

By convention standards, Angular Resolvers exist in their own TypeScript files with the name `feature.resolver.ts` - often bundled together in the same folder of the feature you are working on. For example, all of the resolvers for the "organizations" feature are in the `organizations/` directory and in the file `organization.resolver.ts`.

Once in your file, you can begin to add Resolvers! Resolvers defined by the `ResolveFn` class. The `ResolveFn` object is defined in Angular as the following:

```ts
export declare type ResolveFn<T> = (route: ActivatedRouteSnapshot, state: RouterStateSnapshot) => Observable<T> | Promise<T> | T;
```

> **NOTE:** You can actually find this declaration as well! Simply right click on `ResolveFn` in your project and select "Go to Definition".

As you can see, resolvers are simply _functions_ with the following properties.

Resolvers take in two arguments:

- `route`: The active route that the component is currently loaded at (i.e., the URL and related information).
- `state`: Object that contains various pieces of information related to the route and navigation. For most purposes in the CSXL application, this parameter remains unused.

Resolvers return some data of type `T` back to the frontend, either in format of `Observable`, `Promise`, or just the data type `T` itself!

So, we can define a basic Resolver using the convention below:

```ts
export const resolver: ResolveFn<T> = (route, state) => {
  // Return something here of type Observable<T>, Promise<T>, or T
};
```

> **NOTE:** Notice the keyword `export`! This keyword enables other files, such as our component files, to be able to access this constant.

Of course, `T` is a generic type. So, if we wanted to create a Resolver to get all organization data, we could create a resolver with the following structure:

```ts
/** This resolver injects the list of organizations into the organization component. */
export const organizationResolver: ResolveFn<Organization[] | undefined> = (route, state) => {
  // Do something here!
};
```

Notice that we use `Organization[] | undefined` as our generic type `T` in case no data is loaded.

From here, we can **call our service function** to return the data we are expecting! We can do this using the following:

```ts
/** This resolver injects the list of organizations into the organization component. */
export const organizationResolver: ResolveFn<Organization[] | undefined> = (route, state) => {
  return inject(OrganizationService).getOrganizations();
};
```

Notice the use of `inject()`! We are _injecting_ the `OrganizationService` into the Resolver so that we can run its methods. From there, we return `.getOrganizations()`.

That is all that is needed to set up a basic Angular Resolver!

## Using Resolver Data in Components

Now that you have created a Resolver, it is time to actually use it inside of an Angular Component!

Recall the structure of of our component:

```ts
@Component({
  selector: "organization-page",
  templateUrl: "./organization-page.component.html",
  styleUrls: ["./organization-page.component.css"],
})
export class OrganizationPageComponent {

  /** Route information to be used in the Routing Module */
  public static Route = {
    path: '',
    title: 'CS Organizations',
    component: OrganizationPageComponent
  };

  /** Store unwrapped list of Organizations */
  public organizations: Organization[] = [];

  /** Initializer for the component */
  constructor(private route: ActivatedRoute) {}
}
```

Resolvers help us *load data into our components **before** construction*. So, to actually pass in a resolver, we can modify the organization page's `Route`! The route contains all of the information needed to the *router* to load a component. Since we want to load the data of a Resolver *before* the component loads, we want to add these resolver functions to the `Route` static property so that the router can run these first.

We can add the `resolve` field to the `Route` object like so:

```ts
/** Route information to be used in the Routing Module */
public static Route = {
  path: '',
  title: 'CS Organizations',
  component: OrganizationPageComponent
  resolve: {
    organization: organizationResolver // NEW
  }
};
```

We are passing in an *object shape* into the `resolve` parameter, where we assign a field name `organization` to the `organizationResolver`! Now, when the page loads, an object with the same shape will be available from the route with the data we want assigned to its `organization` field! Specifically, this object will be accessible using `route.snapshot.data` in the constructor, where `route` is the injected `ActivatedRoute`.

So, in the component's *constructor*, let's load our pre-loaded data.

```ts
  /** Initializer for the component */
  constructor(private route: ActivatedRoute) {

    // STEP 1: Load the data passed from the resolver to the route.
    const data = route.snapshot.data as {
      organization: Organization[];
    }

    // STEP 2: Access our data!
    this.organizations = data.organization;
}
```

First, we use `route.snapshot.data` to retrieve the data object exposed by our route based on the data we retrieved from the Resolver! Then, we want to *cast* this data (using the `as` operator) to an object *matching the exact shape as what we provided in `resolve` in the `Route` field above!) So, we need to cast this to an object with a field named `organization` that takes in the data type we are expecting from our Resolver - a list of organizations!

From there, now the `data` constant is saved to an oject with a single field named `organization`, and this field has been **successfully populated** with the results of `OrganizationService.getOrganizations()` - *no observables or subscriptions needed!*

So lastly, in order to access our data, we can simply call `data.organization` and save it to a field of the Component!

Let's take a look at the final code:

```ts
@Component({
  selector: "organization-page",
  templateUrl: "./organization-page.component.html",
  styleUrls: ["./organization-page.component.css"],
})
export class OrganizationPageComponent {

  /** Route information to be used in the Routing Module */
  public static Route = {
    path: '',
    title: 'CS Organizations',
    component: OrganizationPageComponent,
    resolve: {
      organization: organizationResolver // NEW
    }
  };

  /** Store list of Organizations */
  public organizations: Organization[];

  /** Initializer for the component */
  constructor(private route: ActivatedRoute) {

    // STEP 1: Load the data passed from the resolver to the route.
    const data = route.snapshot.data as {
      organization: Organization[];
    }

    // STEP 2: Access our data!
    this.organizations = data.organization;
}
}
```

That is essentially all you need to set up Resolvers and connect Resolvers to Angular Components in your code!

## Access Route Parameters in the Resolver

The setup above is great for querying all data! However, what if you wanted to query *specific* data? For example, the `OrganizationService` has a `.getOrganization(slug: string)` function that takes in a specific slug to find an organization matching that slug. This call would be used on the *organization detail page* \([link here](https://csxl.unc.edu/organizations/cads)\) to display information about one specific organization.

Look at the *route*, or URL, of this sample organization detail page for CADS: `https://csxl.unc.edu/organizations/cads`. As you can see, the route contains the *slug* for the organization! 

Recall that the *Resolver* takes in a **`route`** parameter! This parameter allows us to have access to the current route that the user is navigating to.

Before, in our *components*, we could access parameters in our routes, such as slugs, using the following:

**The constructor of a Component File:**
```ts
constructor(private route: ActivatedRoute, private organizationService: OrganizationsService) {
  let slug = route.paramMap.get('slug')!
  this.organization$ = organizationService.getOrganization(slug);
}
```

We could do this when `route` was injected into our component. Well, we have access to our *route* in our Resolver too!

Recall the final setup for the `organizationResolver` we defined earlier:

**In `organization.resolver.ts`**

```ts
/** This resolver injects the list of organizations into the organization component. */
export const organizationResolver: ResolveFn<Organization[] | undefined> = (route, state) => {
  return inject(OrganizationService).getOrganizations();
};
```

We can use the *route* parameter in the same way as we would in the component! So, let's create a new resolver called `organizationDetailResolver` that loads the data for just one organization:

**In `organization.resolver.ts`**

```ts
/** This resolver injects an organization into the organization detail component. */
export const organizationDetailResolver: ResolveFn<Organization | undefined> = (route, state) => {
  let slug = route.paramMap.get('slug')!
  return inject(OrganizationService).getOrganization(slug);
};
```

That is all that is needed! You can then pass this Resolver back into a component's static `Route` property and access the data as we did before.

## Error Handling with Resolvers

What happens if there are errors when we attempt to load our data using Resolvers? If you recall, if we were to use the traditional method of *subcscribing* to an `Observable`, we could include error handling using the following:

```ts
this.organization$.subscribe({
  next: (organization) => {
    // Do something on success here.
  },
  error: (err) => {
    // Handle and errors here.
  }
});
```

How would we handle errors using our Resolvers if we are never explicitly subscribing to an `Observable` in code?

We can use RxJS's `catchError()` function to handle errors in our Resolver!

First, we need to use the `.pipe()` function to *pass the injected `Observable`* into the `catchError()` function. Look at the example below:

**In `organization.resolver.ts`**

```ts
/** This resolver injects an organization into the organization detail component. */
export const organizationDetailResolver: ResolveFn<Organization | undefined> = (route, state) => {
  let slug = route.paramMap.get('slug')!
  return inject(OrganizationService).getOrganization(slug)
    .pipe(
      catchError(err) => {
        // Handle error here!
        // Let's log the error, and then instead of crashing the program, we can just
        // return `undefined` for our `Organization` output.
        console.log(err);
        return of(undefined);
      }
    )
};
```

With this convention, we can handle any errors that occur when we attempt to retrieve the organization! Notice the usage of RxJS's `of()` operator in the return type.

In RxJS, the **`of()`** operator is a function that *creates an Observable* from a value! Since the return type of this Resolver is to return an `Observable<Organization | undefined>` directly, we cannot just return `undefined`! We need to return an *Observable* holding the value `undefined`. So, we return `of(undefined)`.

You can add a lot more nuance to your error handling here depending on the specific use cases you have in your final project.

## Conclusion

Angular Resolvers are a great tool to be aware of and to utilize in your project. They simplify loading data to your Components, guaranteeing that data is pre-populated before the Component's construction without the complicated nature of manually managing subscriptions! It is also especially useful if you need to load data from multiple API calls at once as well. I encourage you to take a look at the [`organization-detail.component.ts`](https://github.com/unc-csxl/csxl.unc.edu/blob/main/frontend/src/app/organization/organization-details/organization-details.component.ts) file! This component loads data from *three different resolvers* at once. 

You want to be cautious about using Resolvers for *everything*, though. In situations where your page needs to dynamically update, for example, using Resolvers is not the best idea (because Resolvers load your data *once*). Instead, using a convention such as the CSXL's custom `RxObject` class may be a better idea (docs page on this coming soon). 

Here are some extra resources to explore if you want to learn more about Angular Resolvers:
- [Angular Documentation for `ResolveFn`](https://angular.io/api/router/ResolveFn)
- [RxJS Documentation](https://rxjs.dev/guide/operators)
- [Data Stored in `ActivatedRoute`](https://angular.io/api/router/ActivatedRoute)
