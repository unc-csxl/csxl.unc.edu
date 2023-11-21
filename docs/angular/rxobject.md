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

## Introduction to the `RxObject` Class

The `RxObject` class nun
