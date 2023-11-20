# Error Handling in the Middleware

> Written by Ajay Gandecha for the CSXL Web Application and for COMP 423: Foundations of Software Engineering.<br>_Last Updated: 11/20/2023_

## Preface

In the final project, you been creating and implementing rather complex logic in your Python services and APIs to fetch, modify, and delete data in your database! Of course, these operations can often in exceptions that must be ultimately sent over back to your frontend in the form of an HTTP response code.



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

![Traditional Error Handling Diagram]()

However, this is not necessarily the best way to handle errors. First, this method is **not that concise** and a bit _redundant_. Imagine we have 5 different `GET` APIs. Throughout all these APIs, we need to re-implement this logic to catch exceptions and throw them as a `404` HTTP exception.

In addition, what if we want to handle many different errors? For example, imagine we have a `GET` API to _retrieve the members of an organization_. We may define this at the endpoint `/api/organization/members/:slug`, where `slug` is the identifier of the organization. There are many different HTTP responses that we may want to send here:

1. `403 : Forbidden` - for when a user who is not in charge of the organization attempts to acces this list.
1. `404 : Resource Not Found` - for when the organization for a given slug does not exist.
1. `422 : Unprocessable Entity` - for when an ID is passed in the HTTP Request instead of a valid slug.

If we want to handle different types of errors, how we throw and handle exceptions becomes a bit more complicated. We would need to throw custom `Exception`s in the services and then include more complex logic in your API's `try`/`except` blocks.

So, *there is a better way* for us to handle errors in your backend code. For this, we are going to make use of **middleware**. 

In the CSXL Application, we define the **middleware** as functions that run during the transfer of data across the HTTP abstraction barrier between the backend and the frontend. We can utilize the middleware to simplify how we handle exceptions and throw HTTP responses to the backend.

## Using the Middleware to Handle Exceptions

