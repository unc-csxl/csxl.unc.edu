# Testing

## Backend

Tests for `backend` code use [Pytest](https://doc.pytest.org/) and are organized in the `test` directory
with subdirectories that mirror the package structure.

To run the tests, simply run `pytest`.

To see `print` output, run Pytest with the special extra output flag `pytest -rP`.

VSCode's Python plugin has great support for testing. Click the test tube icon, configure VSCode to use Pytest and select the workspace. When you refresh, you will see tests you can run individually, or in the debugger and with breakpoints. For more, see the [official documentation](https://code.visualstudio.com/docs/python/testing).

The file `backend/test/conftest.py` defines fixtures for automatically setting up and tearing down a test database for backend services to use.