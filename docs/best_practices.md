# Best Practices

This is an internal document that specifies the **best practices** for working on frontend code. This includes writing documentation, structuring code, and organizing frontend components.

## Python Documentation

We need to adhere to the following best practices in regards to documenting our backend Python code. This includes the use of pydocing as well as describing the importance of certain lines of code.

### Class Documentation

Here is an example Python class with proper documentation.

```
class SampleClass:
  """
  Include a description of the class and what it represents here. Feel free to include important use cases and funcionality here.
  """

  # Explain what fields represent here 
  sample_field: int | None = None

  def sampleFunctionOne(param: int) -> int:
    """
    Explain the purpose of the function here.

    Parameters:
        param (int): Description of the parameter.
    Returns:
        int: Description of the return value.
    Throws (OPTIONAL):
        SomeException: Description of why a value throws
    """
```

## TypeScript Documentation and Best Practices

We must document all *classes*, *fields*, and *functions*. The TypeScript language website provides [great information here](https://www.typescriptlang.org/docs/handbook/jsdoc-supported-types.html) about how to properly add documentation.

In addition, **all TypeScript functions should be converted to arrow functions.** This is the more modern, standard convention.