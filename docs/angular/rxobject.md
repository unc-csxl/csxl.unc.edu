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
organizationService.getOrganizations.subscribe((organizations) => {
  // Access organizations here!
  console.log(organizations);
})
```

This is great, and the concept is extremely powerful! But, what happens if we wanted to update the data? Let's say that we *post* a new organization, *edit* an organization, or *delete* an organization. ***How would we refresh the data within our page?***

*You will find that the answer to this question is actually a bit tricky.* You may be able to programmatically reload your page, which also reloads your data, however this will cause your screen to flash and is not a good approach. You can also technically re-call your APIs, replace your observables, subscribe to the result, and refresh the data on your page, which is not ideal either. Lastly, you can update the data on your page manually to reflect the changes made using these API calls, however this is redundant and introduces changes for data to become out of sync.

We need a way to manage this so that we can update data dynamically without having to do any of the steps above. This is incredibly important on pages with dynamic data or where information needs to refresh constantly.

This lesson aims to teach you how to use the `RxObject` class, a custom construction in the CSXL Web Application that actually enables this dynamic data reloading functionality! The `RxObject` class and its usage is actually quite simple, however the combination of features and its inner workings makes it extremely powerful and handy.

