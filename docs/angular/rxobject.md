# Using `RxObject`

> Written by Ajay Gandecha for the CSXL Web Application and for COMP 423: Foundations of Software Engineering.<br>_Last Updated: 11/21/2023_

## Preface

Throughout COMP 423, you have been learning how to effectively load data from your APIs into your frontend. Since fetching data from an API is not instantaneous (we need to submit an HTTP request across the internet), we do not receive a response from our APIs *immediately*. There is a slight amount of latency between your HTTP *request* and *response!* To deal with this latency, you have learned how to utilize RxJS `Observable` objects. Observables are a common *design pattern* used across programming languages and something you were introduced to in COMP 301. In COMP 423, you learned how to ***subscribe*** to observables to access the data within them.

To recap, take a look at the following example. Say that we are trying to call an API that returns all of the organizations within the `organization` database table in the backend. We can do this in our `OrganizationService` like so:

**In `OrganizationService`**:

```ts
  /** Returns all organization entries from the backend database table using the backend HTTP get request.
   * @returns {Observable<Organization[]>}
   */
  getOrganizations(): Observable<Organization[]> {
    return this.http.get<Organization[]>('/api/organizations');
  }
```

As you can see, we use the `.get()` method on our injected `HttpClient` to run a GET HTTP request to the API at the route `/api/organizations`! You will also notice that the result of this method is **NOT** `Organization[]`, or a list of organizations. Instead, the result of this method is `Observable<Organization[]>`.

In order for us to access the data within our observable in our `OrganizationComponent` TypeScript class, we would need to do the following:

**In `OrganizationComponent`**:
> **NOTE**: Assume that `OrganizationService` is *injected* into the component and given the name `organizationService`.

```ts
organizationService.getOrganizations().subscribe((organizations) => {
  // Access organizations here!
  console.log(organizations);
})
```

This is great, and the concept is extremely powerful! But, what happens if we wanted to update the data? Let's say that we *post* a new organization, *edit* an organization, or *delete* an organization. ***How would we refresh the data within our page?***

*You will find that the answer to this question is actually a bit tricky.* You may be able to programmatically reload your page, which also reloads your data, however this will cause your screen to flash and is not a good approach. You can also technically re-call your APIs, replace your observables, subscribe to the result, and refresh the data on your page, which is not ideal either. Lastly, you can update the data on your page manually to reflect the changes made using these API calls, however this is redundant and introduces changes for data to become out of sync.

We need a way to manage this so that we can update data dynamically without having to do any of the steps above. This is incredibly important on pages with dynamic data or where information needs to refresh constantly.

This lesson aims to teach you how to use the `RxObject` class, a custom construction in the CSXL Web Application that actually enables this dynamic data reloading functionality! The `RxObject` class and its usage is actually quite simple, however the combination of features and its inner workings makes it extremely powerful and handy.

## Review of the Observable Design Pattern

In order to understand how the `RxObject` class works, it is first important to have a good understanding of the Observable design pattern.

If you recall from COMP 301, in the Observable design pattern, there is one object called a **subject** ***or*** **observable** which can change state or value. Many other objects called **observers** are dependent on the value of the *subject* to complete certain tasks. These objects are called observers because they *observe* or *watch* the value of the *subject*. Whenever the subject's state or value changes, the subject ***notifies*** all of the objects that are observing it with the new value.

This relationship can be seen in the diagram below:

![Observable Design Pattern]()

We can also apply this design pattern to an analogy. Say that we are watching the score of a UNC vs. Duke basketball game. In this example, the game's score would be the **subject**, since it is a single item whose value changes. Then, we the viewers would be the **observables** that *observe* and keep note of the game's score. When UNC inevitably scores over Duke, the game's score then changes. The score is then broadcast on your phone or television, ***notifying*** all of the viewers (observables) of the new score.

If we were to ground the Observable design pattern back to the CSXL web application and retreiving organizations using the example from the Preface, `organizationService.getOrganizations()` returns an ***observable***, or *subject*. Remember, these terms are interchangeable in the context of the design pattern! In this case, the `OrganizationComponent` itself is the ***observer*** that watches the subject's value. When the observer *subscribes* to the subject, we then wait to be *notified* of the next value.

```ts
organizationService.getOrganizations().subscribe((organizations) => {
  // Access organizations here!
  console.log(organizations);
})
```

As you can see in the arrow function from above, the *subject* ***notifies*** us of the subject's value within the `organizations` variable. We can then access that data (the state or value of the subject) and use it within our application.

## Connecting the Observable Design Pattern to RxJS

### The `Observable<T>` Class

RxJS enables us to easily work with the Observable design pattern within our TypeScript code and provides us with numerous helper classes to achieve this. The one that you are the most used to seeing is likely `Observable<T>`. The `Observable<T>` class represents the *subject / observable* within our Observable design pattern structure, where `T` is a generic type representing the type of data the object is storing. Observers can then can use the `.subscribe()` method of `Observable` to be notified of the subject's next value.

In RxJS however, `Observable` is the superclass to many other related classes that can also be used to represent the *subject / observable* in the design pattern - most notably, the `Subject<T>` class.

### The `Subject<T>` Class

RxJS contains the `Subject<T>` class, which is a subclass of `Observable<T>`. `Subject<T>` extends the functionality as `Observable<T>`, enabling it to "multicast" values to *multiple* observers rather than just one.

When you have a regular observable, each subscription to that observable will trigger a *separate and independent* execution of the observable's logic. Each subscriber gets its own, isolated stream of data. However, what if we wanted to multiple observers to subscribe and share the same stream of data?

That is where this "multicasting" feature comes in. In this context, "multicasted" refers to the ability of a subject to *share a single data stream* from the subject among multiple subscribers. Values emitted from the subject using ***notify*** are then multicast (shared) to all subscribers.

This distinction is extremely important for the purposes of our project. We want to use subjects so that multiple components can view the same stream of data!

There are three different kinds of `Subject<T>`s that we can choose from. All of these three specific types *extend* `Subject<T>` adding new functionality:

- `BehaviorSubject<T>`: A variant of `Subject<T>` that *requires an initial value* and *emits its current value whenever it is subscribed to*.
- `ReplaySubject<T>`: A variant of `Subject<T>` that *"replays" old values* to new subscribers *by emitting them when they first subscribe*.
- `AsyncSubject<T>`: A variant of `Subject<T>` that only emits a value when it completes.

For the purposes of being able to update our data dynamically and share it across components, we are going to take a closer look at the `ReplaySubject<T>` class.

### The `ReplaySubject<T>` Class

As noted in the section above, the `ReplaySubject<T>` re-emits the latest value that is has to *new subscribers*. This is extremely useful. Imagine that we loaded all organization data on the main organization page, and then navigate to a new page that uses the same data. By re-subscribing to the `ReplaySubject<T>`, we can essentially get access to the most recently-loaded data so that we do not have to re-fetch all of our data again!

We can create a `ReplaySubject<T>` object using the code below:

```ts
let subject: Subject<string> = new ReplaySubject(1);
```

> **NOTE:** The subject created above stores *strings* as its value. However, you can replace this data type with any data type you like.

It is important to note that the `ReplaySubject()` constructor takes a *parameter*. This parameter is the ***buffer size***, or the amount of past data that it should store! In this case, we only want to keep the latest (most up-to-date) data in our subject, so we can keep our buffer size as `1`.

Once we created the `ReplaySubject` object, we can then *feed data into it* (set its value) using the `.next()` method. This method also ***notifies*** all observers pointing to the subject.

```ts
let subject: Subject<string> = new ReplaySubject(1);
subject.next("COMP 423 rocks!!");
```

The `.next()` method is how we update data within our subject!

It is also important to note that we can *convert subjects back to observers*. For example, given the same subject we created before, we can create a typical `Observable<T>` object out of it using the following:

```ts
let subject: Subject<string> = new ReplaySubject(1);
let value$: Observable<string> = subject.asObservable();

// Access latest data from the subject
value$.subscribe((stringValue) => {
  console.log(stringValue);
})
```

As you can see, the code above creates an `Observable` from the `ReplaySubject` which we can subscribe to!

Now that you have reviewed the basics of RxJS and its classes, we can now begin to bundle these classes together to create `RxObject` - a unified way for us to dynamically update our data.

## Introduction to the `RxObject` Class

The motivation of the `RxObject` class is to allow for the updating of data within observables such that your Angular Components can dynamically update with the new data. The `RxObject` class is not part of RxJS; rather, it is custom to the CSXL Web Application and serves as a helper that bundles together RxJS functionality in a concise and simple way. The class already exists in the CSXL repository at `frontend/src/app/rx-object.ts`. However in this section, we are going to rebuild this class from scratch so that you gain a fundamental understanding of how it works.

First, we know that `RxObject` must be flexible enough to handle various types of data, in the same way that `Observable` and `ReplaySubject` do. To enable this functionality, we will specify that `RxObject` takes a *generic type* `T`. We can do this in the class's header:

```ts
export abstract class RxObject<T> {
  // Implementation here
}
```

> **NOTE:** We use the keyword `export` on this class so that other TypeScript classes in our file can access this.

Notice that we also make this class **`abstract`**. The core motivation behind in the `RxObject<T>` class is that we *do not instantiate it directly*. Instead, we want to have *subclasses* ***extend*** this base class for related usecases. For example, if we wanted to dynamically store data for organizations, we may want to create a subclass `RxOrganizationsList` that *extends* `RxObject<Organization[]>`. We will utilize this in the future, but for now, we are just working on the conceptual `abstract` class.

From here, we know we need to successfully implement the Observer design pattern. We know that the Angular Components are going to be the *observers*, which means the only thing missing here is the *subject*. We want our `RxObject<T>` class to contain our subject.

You can recall that, after examining the various options for our RxJS subject object, we decided that `ReplaySubject<T>` is the best for our use case. This is because the `ReplaySubject<T>` re-emits the latest value that is has to *new subscribers*. We will use a `ReplaySubject<T>` object to serve as the main *subject* to satisfy the requirements of the Observer design pattern.

So, we need to add a `ReplaySubject<T>` to our `RxObject<T>` class. We want our `RxObject<T>` class to *abstract* away this functionality from the Components that use it, so we can make our `ReplaySubject<T>` a **private** field. We do not want to directly expose this subject to Components - rather, the subject will be used internally within the `RxObject<T>` object to manage the data stream. Let's add it to the class:

```ts
export abstract class RxObject<T> {

  /**
  * The Subject provides a "multicast" mechanism for publishing changes to observers.
  * We choose a ReplaySubject with a value of 1 such that every new observer is guaranteed
  * to receive the latest value immediately upon observation, once an initial value has
  * been set.
  */
  private subject: Subject<T> = new ReplaySubject(1);

}
```

As you can see, we *initialize* our `subject` field using a new `ReplaySubject` with a buffer size of `1` so that it stores just the most up-to-date value.

So, if this field is private, then how do we want our Components to interact with our object? We want the Components to interact with the object by *subscribing to a simple `Observable<T>`*. The motivation behind this is so that `subject` manages the data stream and ensures that everything is working correctly behind the scenes, and that our Components do not need to worry about this concern and can work with the more general `Observable` type everywhere else. In addition, it enables the use of the `| async` pipe in HTML. Since we want our Components to access this field, we can make it public. Let's add the observable, made from our `subject`, into our object:

```ts
export abstract class RxObject<T> {

  /**
  * The Subject provides a "multicast" mechanism for publishing changes to observers.
  * We choose a ReplaySubject with a value of 1 such that every new observer is guaranteed
  * to receive the latest value immediately upon observation, once an initial value has
  * been set.
  */
  private subject: Subject<T> = new ReplaySubject(1);

  /**
  * This exposed Observable is what all Components and Services dependent on the RxObject
  * are expected to subscribe to for updates and changes of state to the object.
  */
  public value$: Observable<T> = this.subject.asObservable();

}
```

As you are likely already aware, it is convention to put a `$` after the names of `Observable`s in RxJS / TypeScript so that it is easy to differentiate what is a `Observable<T>` and the actual data itself of type `T`.

Lastly, for internal purposes, we also simply want to include a field that simply contains the value (of type `T`) that is the *latest value* of our subject! We make this *protected* so that only `RxObject<T>` and its subclasses can access it, but not other files (like Components). We want other files to use the public `value$` observable and subscribe to that. We can add this final field below:


```ts
export abstract class RxObject<T> {

  /**
  * The last/most recent value of the RxObject.
  */
  protected value!: T;

  /**
  * The Subject provides a "multicast" mechanism for publishing changes to observers.
  * We choose a ReplaySubject with a value of 1 such that every new observer is guaranteed
  * to receive the latest value immediately upon observation, once an initial value has
  * been set.
  */
  private subject: Subject<T> = new ReplaySubject(1);

  /**
  * This exposed Observable is what all Components and Services dependent on the RxObject
  * are expected to subscribe to for updates and changes of state to the object.
  */
  public value$: Observable<T> = this.subject.asObservable();

}
```

Those are all of the fields of `RxObject`! Now, we simply need a method to actually ***update the data*** within our object! Let's call this method `set()` and have it take in a parameter of type `T`, which will be the new value. This method should perform two steps:
1. Update the internal `value` field.
2. Notify all *observers* of a change in our internal value.

Let's add this method to our `RxObject<T>` implementation:

```ts
  /**
  * Replace the last value of the RxObject with a new value and notify observers.
  *
  * @param value The new value of the RxObject.
  */
  set(value: T): void {
    this.value = value;
    this.notify();  // NOTE: NOT IMPLEMENTED YET
  }
```

As you can see, the `set()` method above completes both steps! We can abstract the internal *notify* logic into a protected method called `notify()`. How would be implement this method?

Recall how we notify the observers of a `ReplaySubject<T>` object. We use the `.next()` method! In this case, we simply want to pass in our newly updated `value` field into `.next()`.

Here is our **final implementation** of the `RxObject<T>` class:

```ts
export abstract class RxObject<T> {

  /**
  * The last/most recent value of the RxObject.
  */
  protected value!: T;

  /**
  * The Subject provides a "multicast" mechanism for publishing changes to observers.
  * We choose a ReplaySubject with a value of 1 such that every new observer is guaranteed
  * to receive the latest value immediately upon observation, once an initial value has
  * been set.
  */
  private subject: Subject<T> = new ReplaySubject(1);

  /**
  * This exposed Observable is what all Components and Services dependent on the RxObject
  * are expected to subscribe to for updates and changes of state to the object.
  */
  public value$: Observable<T> = this.subject.asObservable();

  /**
  * Replace the last value of the RxObject with a new value and notify observers.
  *
  * @param value The new value of the RxObject.
  */
  set(value: T): void {
    this.value = value;
    this.notify();
  }

  /**
  * Subclasses are expected to make mutable changes to `this.value` and then call `this.notify()`
  * in order to broadcast changes to all dependent subscribers of this RxObject.
  */
  protected notify() {
    this.subject.next(this.value);
  }
}
```

This exact implementation is what is used currently in the CSXL application! 

Now that we have implemented `RxObject<T>`, it is time to *extend* the abstract class so that we can use it within our application for our specific use cases. Next, we will explore two different uses of this object.

## Update Data Using `RxObject`

If you have explored the Coworking feature of the CSXL Application, you likely know that the data on the Coworking page *updates every 5 seconds*. Say that `pollStatus()` is a function that exists *within the `CoworkingService`* that runs every 5 seconds to update the current status of the CSXL and coworking data. Let's take a look here:

**In `coworking.service.ts`:**

```ts
@Injectable({
  providedIn: 'root'
})
export class CoworkingService {

  // OTHER FUNCTIONALITY HIDDEN

  /** This method is called every 5 seconds to update the coworking data. */
  pollStatus(): void {
    this.http.get<CoworkingStatus>('/api/coworking/status').subscribe((status) => {
      console.log("FETCHED STATUS! Now what?");
    });
  }
}
```

How would we go about storing our data so that we can access this data in our component? Let's use `RxObject`!

First, as you remember, `RxObject` is an *abstract class* - therefore, it cannot be instantiated directly. We need to create a *subclass* for `RxObject` that pertains to our specific feature and the data we are trying to store. In this case, we are trying to store an object of type `CoworkingStatus`. So, let's define a new class - `RxCoworkingStatus` - that extends `RxObject`! We can define this using the code below in a new file.

**In `rx-coworking-status.ts`**

```ts
export class RxCoworkingStatus extends RxObject<CoworkingStatus> {}
```

Notice that this is a one-liner! We do not need to override or overload any methods. Notice also though that the *generic type* goes away - this is because we extend `RxObject<CoworkingStatus>`, which fills in this generic type!

Now, ***in our service***, we can create two new fields - one to store our `RxCoworkingObject` which allows us to dynamically update our data, and then one public observable for our components to use that is automatically updated with new data! The fields are shown below:

```ts
private status: RxCoworkingStatus = new RxCoworkingStatus();
public status$: Observable<CoworkingStatus> = this.status.value$;
```

Notice that `status`, which is our `RxCoworkingStatus` object, is private - this is because we want to abstract all of this functionality and keep it from our Components. Instead, the only thing accessible to the components should be the *observable* that is automatically updating with new data, `status$`! Notice that this observable is simply the public `.value$` observable from our `status` object that we defined in the previous part.

Finishing this functionality is easy! All we need to do now is call the `.set()` method on our `RxCoworkingStatus` object (remember, this was *inherited* from `RxObject` because `RxCoworkingStatus` extends `RxObject`). We can do this in `pollStatus()`, which is supposed to update our data! Look at the following final construction:

**In `coworking.service.ts`:**

```ts
@Injectable({
  providedIn: 'root'
})
export class CoworkingService {

  private status: RxCoworkingStatus = new RxCoworkingStatus();
  public status$: Observable<CoworkingStatus> = this.status.value$;

  // OTHER FUNCTIONALITY HIDDEN

  /** This method is called every 5 seconds to update the coworking data. */
  pollStatus(): void {
    this.http.get<CoworkingStatus>('/api/coworking/status').subscribe((newStatus) => {
      // Update the `RxCoworkingStatus` object, which automatically notifies
      // the observers through `status$`.
      this.status.set(newStatus);
    });
  }
}
```

This is all we need! Now in any Component that needs to access this status, we can simply **subscribe to the `status$`** observable from the `CoworkingService` in a Component or use its data in our HTML using the `| async` pipe! The data on the page will automatically update every five seconds.

