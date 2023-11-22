# Error Handling in the Middleware

> Written by Ajay Gandecha for the CSXL Web Application and for COMP 423: Foundations of Software Engineering.<br>_Last Updated: 11/20/2023_

## Preface

In the final project, you been creating and implementing rather complex logic in your Python services and APIs to fetch, modify, and delete data in your database! Of course, these operations can often in exceptions that must be ultimately sent over back to your frontend in the form of an HTTP response code.

When working on exercises and your final project, you have been implementing this logic throughout. Let's take a look at a relevant example. Below, you will see the backend service function and the API for **retrieving organizations** from the database using an ID.

---

**In the `OrganizationService`:**

```py
class OrganizationService:
    ...
    def get_from_id(self, id: int) -> Organization:
        """
        Get the organization from an id

        Parameters:
            id (int): Unique organization ID
        Returns:
            Organization: Object with corresponding ID
        """

        # Query the organization with matching id
        organization = self._session.query(OrganizationEntity).get(id)

        # Check if result is not null
        if organization:
            return organization.to_model()
        else:
            raise Exception(f"No organization found with ID: {id}")
```

---

Pay attention to what happens if the search for an organization _fails_ (i.e., the result `organization` is `None`). In this case, we throw an `Exception` with a custom description alerting us that no organization was found for the given ID.

This service function is then used in the organization API! Here is the code for this `GET` API:

---

**In the Organization API:**

```py
@api.get("/{id}", tags=['Organization'])
def get_organization_from_id(id: int, organization_service: OrganizationService = Depends()) -> Organization:
    """
    Get organization with matching id

    Returns:
        Organization: Organization with matching id
    """

    # Try to get organization with matching id
    try:
        return organization_service.get_from_id(id)
    except Exception as e:
        # Raise 404 exception if search fails
        raise HTTPException(status_code=404, detail=str(e))

```

---

Notice that in the API, we use `try`/`except` to _handle_ any exceptions thrown by the service function! So, what happens when our search fails?

Recall that the service function _raises an `Exception`_. This exception is then caught in the API function, and an `HTTPException` is then thrown as the HTTP response. In this case, we ensure that a `404` HTTP response is sent to the frontend if this search fails.

We can show this error handling with the diagram below:

![Traditional Error Handling Diagram](https://github.com/unc-csxl/csxl.unc.edu/blob/docs/middleware/docs/images/backend/no_middleware.jpeg)

However, this is not necessarily the best way to handle errors. First, this method is **not that concise** and a bit _redundant_. Imagine we have 5 different `GET` APIs. Throughout all these APIs, we need to re-implement this logic to catch exceptions and throw them as a `404` HTTP exception.

In addition, what if we want to handle many different errors? For example, imagine we have a `GET` API to _retrieve the members of an organization_. We may define this at the endpoint `/api/organization/members/:slug`, where `slug` is the identifier of the organization. There are many different HTTP responses that we may want to send here:

1. `403 : Forbidden` - for when a user who is not in charge of the organization attempts to acces this list.
1. `404 : Resource Not Found` - for when the organization for a given slug does not exist.
1. `422 : Unprocessable Entity` - for when an ID is passed in the HTTP Request instead of a valid slug.

If we want to handle different types of errors, how we throw and handle exceptions becomes a bit more complicated. We would need to throw custom `Exception`s in the services and then include more complex logic in your API's `try`/`except` blocks.

So, *there is a better way* for us to handle errors in your backend code. For this, we are going to make use of **middleware**. 

In the CSXL Application, we define the **middleware** as functions that run during the transfer of data across the HTTP abstraction barrier between the backend and the frontend. We can utilize the middleware to simplify how we handle exceptions and throw HTTP responses to the backend.

## Using the Middleware to Handle Exceptions

We can define middleware functions in the `backend/main.py` file! The `main.py` file is the entrypoint for your backend application. Therefore, when the backend loads, all of the functions here are loaded first.

If you take a look at this file, you can see that it accomplishes a few things. First, it *configures FastAPI* by providing metadata and all of the APIs defined in the `backend/api` directory.

Below this, you will notice the following code:

```py
# Add application-wide exception handling middleware for commonly encountered API Exceptions
@app.exception_handler(UserPermissionException)
def permission_exception_handler(request: Request, e: UserPermissionException):
    return JSONResponse(status_code=403, content={"message": str(e)})
```

This is our first error-handling *middleware* function!

You can see that this function is marked with the `@app.exception_handler(Exception)` decorator. Note that `app` is referring to the current `FastAPI` application. This decorator essentially makes it so that the function it is attached to *runs whenever an uncaught exception of the type specified is thrown*. For the example above, can conclude that, based on the decorator, that `permission_exception_handler()` will run whenever `UserPermissionException` is thrown!

Each of our *exception handler* middleware functions takes in two parameters: `request` which models the HTTP request made, and `e` which injects the specific uncaught error.

Within our exception handler function, we can then return a `JSONResponse` with the correct status code for the exception we are throwing, as well as a stringified version of the error `e` as the message!

In order for us to be able to catch errors using these middleware functions, we need to create **custom Exception classes!** In the example above, `UserPermissionException` is a *custom exception* that we will throw whenever there are permission errors or when the user is not authenticated. The code for `UserPermissionException` is shown below:

```py
class UserPermissionException(Exception):
    """UserPermissionException is raised when a user attempts to perform an action they are not authorized to perform."""

    def __init__(self, action: str, resource: str):
        super().__init__(f"Not authorized to perform `{action}` on `{resource}`")
```

As you can see, the `UserPermissionException` *extends* the `Exception` class - this is very important! Your custom exceptions must extend `Exception`.

In addition, we create a custom constructor for our exception that takes in two values, and we use `super()` to access the superclass's constructor and pass in a custom string as the exception message.

Now, `UserPermissionException`s pair well with `403: Forbidden` errors, since it indicates a user permission issue.

Another custom exception we can create is `ResourceNotFoundException`! This would match up to our `404: Not Found` errors. We can create this exception below:

```py
class ResourceNotFoundException(Exception):
    """ResourceNotFoundException is raised when a user attempts to access a resource that does not exist."""
    ...
```

As you can see, this custom exception class *also* extends `Exception`. There is nothing special here and no custom constructor - everything is inherited from the superclass `Exception`.

**NOTE:** All of these custom exceptions are defined in the `backend/services/exceptions.py` file! Feel free to check it out for yourself in the CSXL repository.

So, how would we modify our **OrganizationService** and **organization** API function from our first example to use middleware error handling?

Well first, ***in the service***, we will simply just throw our new custom error!

---

**In the `OrganizationService`:**

```py
class OrganizationService:
    ...
    def get_from_id(self, id: int) -> Organization:
        """
        Get the organization from an id

        Parameters:
            id (int): Unique organization ID
        Returns:
            Organization: Object with corresponding ID
        """

        # Query the organization with matching id
        organization = self._session.query(OrganizationEntity).get(id)

        # Check if result is not null
        if organization:
            return organization.to_model()
        else:
            raise ResourceNotFoundException(f"No organization found with ID: {id}") # Updated
```
---

As you can see, now we are using our custom exception.

Now in the API, ***we no longer need the `try` / `except` block***! This is because we will let the middleware functions deal with this error. Now, instead of the APIs handling errors from the service directly, we will let the errors bubble up one more layer. The middleware will then take care of this for us! The new error handling flow is shown below:

![New Error Handling](https://github.com/unc-csxl/csxl.unc.edu/blob/docs/middleware/docs/images/backend/middleware.jpeg)

So, we can easily simplify our API to remove our manual error handling.

---

**In the Organization API:**

```py
@api.get("/{id}", tags=['Organization'])
def get_organization_from_id(id: int, organization_service: OrganizationService = Depends()) -> Organization:
    """
    Get organization with matching id

    Returns:
        Organization: Organization with matching id
    """

    # Try to get organization with matching id
    return organization_service.get_from_id(id) # Notice all error handling removed.
```

---

Now, it is up to our error exception handler functions in the middleware to catch this error! We can ensure that we have a middleware exception handler function to catch and deal with `ResourceNotFoundException`s:

---

**In `main.py`:**

```py
@app.exception_handler(ResourceNotFoundException)
def resource_not_found_exception_handler(request: Request, e: ResourceNotFoundException):
    return JSONResponse(status_code=404, content={"message": str(e)})
```

---

Now, our *middleware* handles throwing this exception as a 404 response!

## Conclusion

As mentioned nearlier in the reading, using middleware exception handlers paired with custom `Exception` classes is extremely useful and helps to significantly reduce redundancy in error handling across all of the various API functions in your application. In addition, this convention is scalable and extendable. As you scale your application and add more custom `Exception` classes, the way exceptions are handled also remains consistent across the application and all API routes.

There are still certain cases where you may need custom error handling by throwing `HTTPException`s in your API functions. However, for most cases, it is better to try and use the middleware to handle exceptions. You are encouraged to look at some of the various HTTP response codes to determine some of the potential custom `Exception` classes you need to make, as well as some of the existing exceptions in `backend/services/exceptions.py` and how they are handled!
