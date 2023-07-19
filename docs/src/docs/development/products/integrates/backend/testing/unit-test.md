---
id: unit-tests
title: Unit tests
sidebar_label: Unit tests
slug: /development/products/integrates/backend/testing/unit-tests
---

Unit tests focuse on verifying the functionality of individual units or
components of our software. A unit would be the smallest testable part of a
software, such as a function, method or class. Unit tests in Fluid Attacks
must be:

- **Repeatable:**
  Regardless of where they are executed, the result must be the same.

- **Fast:**
  Unit tests should take little time to execute because,
  being the first level of testing,
  where you have isolated functions/methods and classes,
  the answers should be immediate.
  A unit test should take at most two (2) seconds.

- **Independent:**
  The functions or classes to be tested should be isolated,
  no secondary effect behaviors should be validated, and, if possible,
  we should avoid calls to external resources such as databases;
  for this, we use mocks.

- **Descriptive:**
  For any developer,
  it should be evident what is being tested in the unit test,
  what the result should be, and in case of an error,
  what is the source of the error.

Our unit test run in our [CI/CD pipeline](https://gitlab.com/fluidattacks/universe/-/blob/trunk/integrates/gitlab-ci.yaml),
every time a developer pushes changes to our repository. They also can be run
locally. To run locally the unit tests that do not change the mock database:

```sh
universe $ m . /integrates/back/test/unit not_changes_db
```

To run the ones that modify the mock database:

```sh
universe $ m . /integrates/back/test/unit changes_db
```

Currently, every time our unit tests run, we launch a mock stack that is
populated with the necessary data required for our tests to execute.
We utilize mocking to prevent race conditions and dependencies within the tests.

For mocking, we utilize the `mock` library from `unittest`. Throughout our
unit tests, you may come across mocks, stubs, and spies. If you are interested
in learning more about these concepts, you can refer to this [post](https://jesusvalerareales.medium.com/testing-with-test-doubles-7c3abb9eb3f2).

When writing unit tests, you can follow these steps to ensure that the test
is repeatable, fast, independent, and descriptive:

- **Test file:**
  We store our tests using the same structure
  as our repository. Inside `universe/integrates/back/test/unit/src` you can
  find our unit tests. Look for the `test_module_to_test.py` file or add it
  if missing.

- **Write the test:**
  Once the file is ready, you can start writing the test.
  Consider the purpose of the function, method, or class that you want to test.
  Think about its behavior when different inputs are provided. Also, identify
  extreme scenarios to test within the test. These will form our test cases and
  are important for writing our assertions. We use the
  [parametrize decorator](https://docs.pytest.org/en/7.1.x/how-to/parametrize.html)
  if possible to declare different test cases.

- **Mocks:**
  What do you mock? A general guideline is to look for the `await`
  statement inside the function, method or class that you want to test.
  In most cases, `await` indicates that the awaited function requires
  an external resource, such as a database. To learn more about mocks,
  you can refer to the official [documentation](https://docs.python.org/3/library/unittest.mock.html).

- **Mock data:**
  When using mocks, you need to provide the data required for
  your unit test to run. We accomplish this by using `pytest fixtures`, which
  allow us to have mock data available from `conftest.py` files.

- **Assertions:**
  Test the expected behavior. We use assertions to validate
  results, the number of function or mock calls, and the arguments used in mocks.

Once your test is ready, format your code:

```sh
universe $ m . /formatPython/default
```

And use a linter:

```sh
universe $ m . /lintPython/module/integratesBackTestUnit
```

A test where you can observe the mentioned steps in action can be found [here](https://gitlab.com/fluidattacks/universe/-/blob/trunk/integrates/back/test/unit/src/app/views/test_charts.py#L41).
