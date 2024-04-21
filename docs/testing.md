# Testing

## Backend

### Organization

Tests for `backend` code use [Pytest](https://doc.pytest.org/) and are organized in the `backend/test` directory
with subdirectories that mirror the package structure.

The file `backend/test/conftest.py` defines fixtures for automatically setting up and tearing down a test database for backend services to use.

At present, we do not have automated front-end testing instrumented; this remains a goal.

### Loading Test Data and Fixtures

To ensure that tests pre-load all test data (defined in `_data.py` files in the test folder) into the database, test files must import `setup_insert_data_fixture` from `core_data.py`.

This `setup_insert_data_fixture` function is a _fixture_ - functions that, once you start running the tests, automatically run before the body of each test function runs.

When a test is run the following process occurs in order:

1. The `test_engine` fixture from `conftest.py` runs, which deletes the existing database (if it exists) and re-creates the database, adding all necessary tables. This fixture also creates the database engine.

2. Using the database engine created above, the `session` fixture from `conftest.py` creates the SQLAlchemy session that all of the Pytests will use when interacting with the PostgreSQL database.

3. The `setup_insert_data_fixture` fixture from `core_data.py` runs, which populates the newly-created empty database with all of the test data.

4. Fixtures creating injectable backend services are created from the `fixture.py` file, which enable Pytests to call and test the service functions they are supposed to.

5. Test cases now run, after the database has been pre-populated with data and all services have been provided via fixtures!

### Pytest CLI

The `pytest` command-line program will run all tests in the command-line.

To see `print` output, run Pytest with the special extra output flag `pytest -rP`.

To limit the scope of your tests to a specific file, include the path to the file following the command, eg:

`pytest backend/test/services/user_test.py`

To run a specific test within a test suite, use the [`-k` option of `pytest`](https://docs.pytest.org/en/latest/example/markers.html#using-k-expr-to-select-tests-based-on-their-name) to match all or part of the filtered test name(s):

`pytest backend/test/services/user_test.py -k test_get`

### Pytest VSCode with Debugger

VSCode's Python plugin has great support for testing. Click the test tube icon, configure VSCode to use Pytest and select the workspace.

When you refresh, you will see tests you can run individually, or in the debugger and with breakpoints. When you encounter a bug or failing test and having a difficult time pinning down exactly why it is failing, developing the instinct to run the test in the VSCode debugger, setting a break point, and stepping through is encouraged.

For more, see the [official documentation](https://code.visualstudio.com/docs/python/testing).

### Code Coverage

We expect 100% test coverage of backend services code and as much coverage for other code in the backend.

To generate a test coverage report, run the following command in your development container:

`pytest --cov-report html:coverage --cov=backend/services backend/test/services`

This command generates a directory with an HTML report. To view it, on your _host machine_, open the `coverage` directory's `index.html` file. Click on the service file you are working on to see the lines not covered by test cases if you are below 100%. After adding test cases that cover the missing lines, rerun the coverage command to generate a new report and confirm your progress.
