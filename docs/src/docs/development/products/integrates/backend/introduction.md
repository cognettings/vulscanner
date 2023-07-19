---
id: introduction
title: Backend
sidebar_label: Introduction
slug: /development/products/integrates/backend
---

[![codecov](https://codecov.io/gl/fluidattacks/universe/branch/integrates/graph/badge.svg?token=V8SMWFOMG0)](https://codecov.io/gl/fluidattacks/universe)

## Introduction

Integrates' backend is an HTTP web service
written in [Python][py],
served with [Hypercorn][hypercorn]
and built with [Starlette][starlette].

## Principles

- _Functional_:
  The codebase favors functions instead of classes
  and avoids direct mutations.
- _No need to reinvent the wheel_:
  Sometimes, third-party packages have already figured it out.

## Getting started

To view the changes reflected as you edit the code, you can run:

```bash
  m . /integrates
```

## Linting

The back uses [Prospector][prospector]
and [Mypy][mypy]
to enforce compliance with a defined coding style.

To view linting issues, you can run:

```bash
  m . /lintPython/dirOfModules/integrates/name of the module
```

To view and auto-fix formatting issues, you can run:

```bash
  m . /formatPython/default
```

## Testing

The back uses [pytest][pytest] as a test runner.

To execute the unit tests on your computer, you can run:

```bash
  m . /integrates/back/test/unit 'changes_db'
  m . /integrates/back/test/unit 'not_changes_db'
```

To execute a functional test on your computer, you can run:

```bash
  m . /integrates/back/test/functional 'name of the test'
```

## Core

The backend codebase consists of several modules,
which are classified into three layers:
API, business logic, and data access.

### Web server

The back is served by [Hypercorn][hypercorn],
a program with two sides:

- 🌐 On one side it speaks the HTTP protocol,
  receiving requests
  and sending responses.
- 🐍 On the other
  it speaks Python ([ASGI][asgi]),
  passing the request data over to Python code for processing.

This is lower-level stuff
that would be difficult to build an application directly on top of,
so that's where [Starlette][starlette] comes in handy.

[Starlette][starlette] abstracts the handling of requests,
and provides us with utilities that make it simple to build a web application,
such as declaring routes,
middlewares,
working with sessions
and managing cookies.

### API layer

This layer provides an external interface for external systems or clients
to interact with our services.

It is implemented as a [GraphQL][gql] API,
of which you can learn more [here](/development/products/integrates/backend/graphql-api).

You can find it in the `back/src/api` directory.

### Business logic layer

This layer implements the core functionality of the application,
processing inputs and producing outputs,
according to the specified business requirements.

You can find it across modules in files usually named `domain.py`.

### Data access layer

This layer declares the structure of each entity used in the application
and interacts with database-specific modules
to read from and write to a data store.

It provides functions to perform [CRUD][crud] operations for each entity,
taking care of batching and caching with the use of [dataloaders][loaders],
and was designed to be agnostic so that the underlying data store can be swapped
without causing major disruptions to the upper layers.

You can find it in the `back/src/db_model`,
`back/src/dynamodb`
and `back/src/search` directories.

[py]: https://www.python.org/
[hypercorn]: https://hypercorn.readthedocs.io/
[starlette]: https://www.starlette.io/
[prospector]: https://prospector.landscape.io/
[mypy]: https://mypy-lang.org/
[pytest]: https://docs.pytest.org/
[asgi]: https://asgi.readthedocs.io/
[gql]: https://graphql.org/
[crud]: https://en.wikipedia.org/wiki/Create,_read,_update_and_delete
[loaders]: https://github.com/graphql/dataloader
