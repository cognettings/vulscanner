---
id: graphql-api
title: GraphQL API
sidebar_label: GraphQL API
slug: /development/products/integrates/backend/graphql-api
---

## What is GraphQL

> "GraphQL is a query language for APIs
> and a runtime for fulfilling those queries
> with your existing data.
> GraphQL provides a complete
> and understandable description
> of the data in your API,
> gives clients the power to ask for exactly what they need
> and nothing more,
> makes it easier to evolve APIs over time,
> and enables powerful developer tools."

— graphql.org

## Integrates GraphQL implementation

From late 2018 to mid-2019 we gradually migrated
from a `REST`-like `API` to `GraphQL`,
first using
[Graphene](https://graphene-python.org/),
but since it didn't support ASGI
and async execution,
in early 2020 we replaced it for [Ariadne](https://ariadnegraphql.org/).

Integrates currently uses the
[Ariadne](https://ariadnegraphql.org/) library,
developed by [Mirumee Labs](https://github.com/mirumee).

All `GraphQL` queries are directed to a
single endpoint,
which is exposed at [/api](https://app.fluidattacks.com/api) thanks to
[Starlette routing configuration](https://gitlab.com/fluidattacks/universe/-/blob/a5e81adb1e55ba8cfc8b931104313e56391e82b9/integrates/back/src/app/app.py).

The `API` layer was inspired by
[GitLab's GraphQL API](https://gitlab.com/gitlab-org/gitlab/tree/master/app/graphql)
and is structured in the following way:

```markup
api
+-- enums
|   +-- __init__.py         <- Index for all enum bindings
|   +-- enums.graphql       <- Available enums schema
+-- interfaces
|   +-- name.graphql        <- Interface type definition
+-- mutations
|   +-- mutation_name.py    <- Mutation implementation
|   +-- schema.graphql      <- Available mutations schema
|   +-- inputs
|   |   +-- schema.graphql  <- Available input types schema
|   +-- payloads
|   |   +-- schema.graphql  <- DTOs and payloads schema
+-- resolvers
|   +-- entity_name
|   |   +-- field_name.py   <- Resolver implementation
+-- scalars
|   +-- __init__.py         <- Index for all scalar bindings
|   +-- scalar_name.py      <- Scalar implementation
|   +-- scalars.graphql     <- Available scalars schema
+-- unions
|   +-- __init__.py         <- Type bindings
|   +-- root.graphql        <- Available union types schema
+-- validations
|   +-- validator_name.py   <- Validators at the schema level
```

### GraphQL Playground

The GraphQL Playground is a tool
that allows to perform queries
against the API
or to explore the schema definitions
in a graphic and interactive way.
You can access it on:

- https://app.fluidattacks.com/api,
  which is production.
- `https://youruseratfluid.app.fluidattacks.com/api`,
  which are the ephemerals
  (where `youruseratfluid` is assigned depending on the name of your git branch).
- https://localhost:8081/api,
  which is local.

### Types

Integrates GraphQL types can be found on Documentation Explorer section at the
[Fluid Attacks API Playground](https://app.fluidattacks.com/api) or you can
[go to the code](https://gitlab.com/fluidattacks/universe/-/tree/a5e81adb1e55ba8cfc8b931104313e56391e82b9/integrates/back/src/api/resolvers).

There are two approaches
to defining a `GraphQL` schema:

1. Code-first
1. Schema-first

We use the latter,
which implies defining the structure using `GraphQL SDL`
(Schema definition language)
and binding it to python functions.

e.g:

api/resolvers/user/schema.graphql

```graphql
type User {
  "User email"
  email: String!
}
```

api/resolvers/user/schema.py

```py
from ariadne import ObjectType

USER = ObjectType('User')
```

Further reading:

- [GraphQL docs - Schemas and Types](https://graphql.github.io/learn/schema/)
- [Mirumee blog - Schema-First GraphQL: The Road Less Travelled](https://blog.mirumee.com/schema-first-graphql-the-road-less-travelled-cf0e50d5ccff)

### Enums

Integrates GraphQL enums can be found on Documentation Explorer section at the
[Fluid Attacks API Playground](https://app.fluidattacks.com/api) or you can
[go to the code](https://gitlab.com/fluidattacks/universe/-/tree/a5e81adb1e55ba8cfc8b931104313e56391e82b9/integrates/back/src/api/enums).

api/enums/enums.graphql

```graphql
...
enum AuthProvider {
  "Bitbucket auth"
  BITBUCKET
  "Google auth"
  GOOGLE
  "Microsoft auth"
  MICROSOFT
}
...
```

> **_NOTE:_**
> By default,
> enum values passed to resolver functions
> will match their name

To map the value to something else,
you can specify it
in the enums binding index,
e.g:

api/enums/\_\_init\_\_\.py

```py
from ariadne import EnumType

ENUMS: Tuple[EnumType, ...] = (
    ...,
    EnumType(
        'AuthProvider',
        {
            'BITBUCKET': 'bitbucket-oauth2',
            'GOOGLE': 'google-oauth2',
            'MICROSOFT': 'azuread-tenant-oauth2'
        }
    ),
    ...
)
```

### Scalars

Integrates GraphQL scalars can be found on Documentation Explorer section at the
[Fluid Attacks API Playground](https://app.fluidattacks.com/api) or you can
[go to the code](https://gitlab.com/fluidattacks/universe/-/tree/a5e81adb1e55ba8cfc8b931104313e56391e82b9/integrates/back/src/api/scalars).

GraphQL provides some primitive scalars,
such as String,
Int and Boolean,
but in some cases,
it is required to define custom ones
that aren't included by default
due to not (yet) being
part of the spec,
like Datetime, JSON and Upload.

Further reading:

- [Ariadne docs - Custom scalars](https://ariadnegraphql.org/docs/scalars)

### Resolvers

Integrates GraphQL resolvers can be found on GraphiQL Explorer section at the
[Fluid Attacks API Playground](https://app.fluidattacks.com/api) or you can
[go to the code](https://gitlab.com/fluidattacks/universe/-/tree/a5e81adb1e55ba8cfc8b931104313e56391e82b9/integrates/back/src/api/resolvers).

A resolver is a function
that receives two arguments:

- **Parent:**
  The value returned by the parent resolver,
  usually a dictionary.
  If it's a root resolver
  this argument will be None
- **Info:**
  An object whose attributes
  provide details about the execution AST
  and the HTTP request.

It will also receive keyword arguments
if the GraphQL field defines any.

api/resolvers/user/email.py

```py
from graphql.type.definition import GraphQLResolveInfo

def resolve(parent: Any, info: GraphQLResolveInfo, **kwargs: Dict[str, Any]):
    return 'test@fluidattacks.com'
```

The function must return a value
whose structure matches the type
defined in the GraphQL schema

> **_IMPORTANT:_**
> Avoid reusing the resolver function.
> Other than the binding,
> it should never be called
> in other parts of the code

Further reading:

- [Ariadne docs - resolvers](https://ariadnegraphql.org/docs/resolvers)

### Mutations

Integrates GraphQL mutations can be found on GraphiQL Explorer section at the
[Fluid Attacks API Playground](https://app.fluidattacks.com/api) or you can
[go to the code](https://gitlab.com/fluidattacks/universe/-/tree/a5e81adb1e55ba8cfc8b931104313e56391e82b9/integrates/back/src/api/mutations).

Mutations are a kind of GraphQL operation
explicitly meant to change data.

> **_NOTE:_**
> Mutations are also resolvers,
> just named differently
> for the sake of separating concerns,
> and just like a resolver function,
> they receive the parent argument
> (always None),
> the info object and their defined arguments

Most mutations only return `{'success': bool}`
also known as "SimplePayload",
but they aren't limited to that.
If you need your mutation to return other data,
just look for it or define a new type in
`api/mutations/payloads/schema.graphql` and use it.

api/mutations/schema.graphql

```graphql
type Mutation {
  ...
  "Create a new user"
  createUser(
    "User email"
    email: String!
  ): SimplePayload!
  ...
}
```

api/mutations/create_user.py

```py
from graphql.type.definition import GraphQLResolveInfo

def mutate(parent: None, info: GraphQLResolveInfo, **kwargs: Dict[str, Any]):
    user_domain.create(kwargs['email'])
    return {'success': True}
```

### Errors

All exceptions raised,
handled or unhandled will be reported
in the "errors" field of the response.

Raising exceptions can be useful
to enforce business rules
and report back to the client
in cases the operation
could not be completed successfully.

Further reading:

- https://spec.graphql.org/June2018/#sec-Errors

### Authentication

The Integrates API enforces authentication
by checking for the presence
and validity of a JWT
in the request cookies or headers.

For resolvers or mutations
that require authenticated users,
decorate the function with the
`@require_login` from `decorators`.

## Authorization

The Integrates API enforces authorization
implementing an ABAC model with a simple grouping
for defining roles. You can find
[the model here](https://gitlab.com/fluidattacks/universe/-/tree/a5e81adb1e55ba8cfc8b931104313e56391e82b9/integrates/back/src/authz).

### Levels and roles

An user can have one role for each one
of the three levels of authorization:

- User
- Organization
- Group

Each role is associated with [a set of permissions](https://gitlab.com/fluidattacks/universe/-/tree/a5e81adb1e55ba8cfc8b931104313e56391e82b9/integrates/back/src/authz/model/roles).

Also, Service level exists and it checks
the covered features according to group plan
like [Squad or Machine](https://fluidattacks.com/plans/).

### Enforcer

An enforcer is an authorization function that
checks if the user can perform
an action on the context.

We define
[enforcers for each authorization level](https://gitlab.com/fluidattacks/universe/-/blob/a5e81adb1e55ba8cfc8b931104313e56391e82b9/integrates/back/src/authz/enforcer.py).
Read the description for understanding
how to use them.

### Boundary

The general methods for listing and
getting the user permissions (and
the permissions that user can grant) are
in [boundary](https://gitlab.com/fluidattacks/universe/-/blob/a5e81adb1e55ba8cfc8b931104313e56391e82b9/integrates/back/src/authz/boundary.py).

The whole application must use this
methods for implementing controls.

### Policy

The general methods for get user role,
grant permissions or revoke them, are in
[policy](https://gitlab.com/fluidattacks/universe/-/blob/a5e81adb1e55ba8cfc8b931104313e56391e82b9/integrates/back/src/authz/policy.py).

### Decorators

For resolvers or mutations
that require authorized users,
decorate the function
with the appropriate decorator
from `decorators`

- @enforce_user_level_auth_async
- @enforce_organization_level_auth_async
- @enforce_group_level_auth_async

## Performance optimizations

In order to make the API more performant,
we are moving towards a fully async backend.
For better comprehension
on how it's done in python,
here's an article
that provides a good explanation:
[Multitasking](/development/products/integrates/backend/multitasking)

### Implementing and using dataloaders

Work in progress,
please check back later

### Caching resolvers

Work in progress,
please check back later

## Guides

### Adding new fields or mutations

Work in progress,
please check back later

1. Declare the field or mutation in the schema using SDL
1. Write the resolver or mutation function
1. Bind the resolver or mutation function to the schema

### Editing and removing fields or mutations

When dealing with fields or mutations
that are already being used by clients,
we need to ensure backwards compatibility.

That is,
we need to let API users know
which fields or mutations will be edited/deleted in the future
so they have time to adapt to such changes.

We use field and mutation deprecation for this.
Our current policy mandates removal
**6 months** after marking fields and mutations
as deprecated.

#### Deprecating fields

To mark fields or mutations as deprecated,
use the
[`@deprecated` directive](https://spec.graphql.org/June2018/#sec-Field-Deprecation),
e.g:

```graphql
type ExampleType {
  oldField: String @deprecated(reason: "reason text")
}
```

The reason should follow
something similar to:

```markup
This {field|mutation} is deprecated and will be removed after {date}.
```

If it was replaced or there is an alternative,
it should include:

```markup
Use the {alternative} {field|mutation} instead.
```

Dates follow the `AAAA/MM/DD` convention.

#### Removing fields or mutations

When deprecating fields or mutations for removal,
these are the common steps to follow:

1. Mark the field or mutation as deprecated.
1. Wait six months
   so clients have a considerable window
   to stop using the field or mutation.
1. Delete the field or mutation.

e.g:

Let's remove the `color` field from type `Car`:

1. Mark the `color` field as deprecated:

   ```graphql
   type Car {
     color: String
       @deprecated(
         reason: "This field is deprecated and will be removed after 2022/11/13."
       )
   }
   ```

1. Wait until one day after given deprecation date and Remove the field:

   ```graphql
   type Car {}
   ```

#### Editing fields or mutations

When renaming fields, mutations or already-existing types within the API,
these are the common steps to follow:

1. Mark the field or mutation you want to rename as deprecated.
1. Add a new field or mutation using the new name you want.
1. Wait until one day after given deprecation date.
1. Remove the field or mutation that was marked as deprecated.

e.g:

Let's make the `color` field from type `Car`
to return a `Color` instead of a `String`:

1. create a `newColor` field that returns the `Color` type:

   ```graphql
   type Car {
     color: String
     newColor: Color
   }
   ```

1. Mark the `color` field as deprecated and set `newColor` as the alternative:

   ```graphql
   type Car {
     color: String
       @deprecated(
         reason: "This field is deprecated and will be removed after 2022/11/13. Use the newColor field instead."
       )
     newColor: Color
   }
   ```

1. Wait until one day after given deprecation date and remove the `color` field:

   ```graphql
   type Car {
     newColor: Color
   }
   ```

1. Add a new `color` field that uses the `Color` type:

   ```graphql
   type Car {
     color: Color
     newColor: Color
   }
   ```

1. Mark the `newColor` field as deprecated and set `color` as the alternative:

   ```graphql
   type Car {
     color: Color
     newColor: Color
       @deprecated(
         reason: "This field is deprecated and will be removed after 2022/11/13. Use the color field instead."
       )
   }
   ```

1. Wait until one day after given deprecation date and remove the `newColor` field:

   ```graphql
   type Car {
     color: Color
   }
   ```

> **_NOTE:_**
> These steps may change
> depending on what you want to do,
> just keep in mind that
> keeping backwards compatibility
> is what really matters.

### Testing

Work in progress,
please check back later
