---
id: philosophy
title: Philosophy
sidebar_label: Philosophy
slug: /development/philosophy
---

At Fluid Attacks we strongly believe
in constantly reviewing the way we do things
to make sure they are as smooth as possible.

Instead of adapting our processes
to a given set of tools,
we constantly seek for new solutions
that improve the way we do things.
It is because of this that
we are always reviewing
the hottest stack and comparing
it against what we currently have.

Throughout the years we have learned
that there are some properties
we envision to have in our technological
stack.

## Open source by default

We strongly believe in open source
as a powerful way
of making the technology ecosystem evolve.
It is thanks to open source projects
that most modern solutions
can do what they do.

Open source projects
also offer other benefits like

- transparency, as anyone can audit the source code;
- flexibility, as most open source licenses allow repurposing the software;
- the capacity of seamlessly working with those who make the solutions;
- being usually free;
- even sometimes being better than commercial competitors.

It is because all of these reasons
that Fluid Attacks is open source by default.
This means we make every product open source
unless there is a valid reason to do otherwise.
Such reasons are typically competitive advantage,
sensitive information disclosure
or architectural limitations.

Similarly, we also prefer using open source stack.

## SaaS by default

We try to outsource as much as possible
in order to keep our operations simple.
Tools that do not require
infrastructure maintenance
are usually preferred.

One clear example of this
is the fact that since 2013
we do not have any on-premise servers.
All our infrastructure exists on the cloud.

We also apply this approach on our own products.
Some of the main advantages
of delivering our products as services are

- we can easily ship updates constantly using CI/CD;
- users can focus on using the tool rather than maintaining it.

## The simpler, the better

We believe the best technological stacks
are those that get things done
in the simplest and less-blocking way possible.

We prefer asynchronous work and automation
over having tons of meetings and blocking sequential steps.
Taking this approach makes us heavily rely on CI/CD,
but also allows us to have a deployment frequency
of over 50 deployments to production every day.

## Deploy, deploy and deploy

Deployment frequency to production
is the most important metric for us,
as it allows us to know how often we're
adding value to our clients.

By having processes completely aligned with this metric,
we ensure that developers
are constantly shipping small changes
to the environment where they will actually add value.
That is production.

Constantly shipping small changes to production
also offers other huge advantages like

- changes are easy to understand and debug;
- peer reviewing becomes simple and fun;
- developers feel empowered as they see how their work has real impact;
- reverting a bug or a failed deployment becomes much easier;
- deploying is a lot less scary.

## Test everything, fail, improve constantly

We think CI/CD is an integral component of the organization.
Everything we do
should be both tested deployed by the CI/CD.

We also think of failure
as the best way of finding
what needs to be improved.
This is why every time something fails,
we look for ways of adding a new test
to our CI/CD so it does not happen again.

This approach makes us have very big CI/CD pipelines
and spend considerable amounts of time optimizing
our CI/CD times and costs,
but it also allows us to constantly improve our software,
reduce risk without blocking deployments,
and keep the knowledge we acquire throughout the path
within the organization.

## Everything as code

We want our [monorepo](https://gitlab.com/fluidattacks/universe)
to be the single source of truth for the organization.
Not only functional source code should exist there,
but also [infrastructure](/development/stack/aws),
[identity management](/development/stack/okta)
and even [secrets](/development/stack/sops).

By making the repository the point
where everything happens,
we get immense benefits like

- a single point of work for everyone;
- complete traceability with git as any change must be made via a Merge Request;
- having the capacity of testing anything using CI/CD;
- complete reproducibility by constantly deploying changes using CI/CD.

## Functional programming

We envision products with

- over 90% of testing coverage;
- state isolation for easier understanding;
- high scalability;
- as few bugs as possible.

This is why all our products
are made using [functional programming](https://fluidattacks.com/blog/why-we-go-functional/).

This is ensured by running strict CI/CD linters.

## Static over dynamic typing

When building large scale software,
implicit typing in programming languages
tends to make source code harder to understand
due to the complexity
developers have to deal with.

We believe in static typing
as it increases the clarity of the source code
and allows CI/CD linters and compilers
to point at those hard-to-catch errors
that otherwise would be very hard to find.
