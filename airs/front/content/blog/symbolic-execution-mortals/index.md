---
slug: symbolic-execution-mortals/
title: Symbolic Execution for Mortals
date: 2017-05-04
category: attacks
subtitle: What it is and how it works
tags: cybersecurity, security-testing, software
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620331105/blog/symbolic-execution-mortals/cover_wgcfrh.webp
alt: Photo by Agence Olloweb on Unsplash
description: In this article, we intend to explain an approach to symbolic execution, which is very useful when dealing with software assessment.
keywords: Symbolic, Execution, Security, Software, Test, Assessment, Ethical Hacking, Pentesting
author: Juan Aguirre
writer: juanes
name: Juan Esteban Aguirre González
about1: Computer Engineer
about2: Netflix and hack.
source: https://unsplash.com/photos/d9ILr-dbEdg
---

In 2003 the Defense Advanced Research Projects Agency, `DARPA`,
announced the Cyber Grand Challenge, a two-year competition seeking to
create automatic systems for vulnerability detection, exploitation, and
patching in near real-time which brought quite a big and complex task to
the table. With this task symbolic execution techniques, which have been
around since the mid `'70s`, came to the attention of a bigger and
broader audience. Difficulty is intriguing for hackers and security
researchers, it makes things interesting but when we are just learning
about something complicated it can be overwhelming and we need to take a
step back and tackle it from a different angle.

This article is meant to give you a different view or angle from which
to tackle this topic, to help you understand the basic concepts of
symbolic execution and how it works in order to enable you to do some
more in depth research on the topic. Common problems and how to solve
them will not be covered here but once you are finished with this
article you should have all the concepts to be able to understand the
why to the problems behind symbolic execution.

## Symbolic Execution

Symbolic execution is a popular program analysis technique introduced in
the mid `’70s` in the context of software testing to check whether a
certain property can be violated by a program. Today it conserves the
same principles and there is no doubt that it has played a big role in
the detection of security vulnerabilities in modern software (Baldoni et
al, 2016).

Symbolic execution can simultaneously explore multiple paths that a
program could take under different inputs that don’t necessarily have to
be defined. The analysis is done at either a source or binary code
level. You might wonder how a program can be executed with different
inputs without actually knowing the exact value of that input. Well,
think of it as a mathematical expression, if you don’t know the exact
value to plug into the expression, you just put `x` or `y` which is just
a variable or better yet a symbol to represent some unknown value. Same
thing here, if we give a program symbolic, rather than concrete input
values it can run with those values and give me an expression at the
end.

<div>
<cta-banner
buttontxt="Read more"
link="/solutions/security-testing/"
title="Get started with Fluid Attacks' Security Testing solution right now"
/>
</div>

### How it works

The execution of all possible paths is done by a symbolic execution
engine. To keep track of all executions, the engine always maintains a
state (`stmt`, `σ`, `π`).

- `stmt`: Statement. The next statement to evaluate.

- `σ` : Symbolic Store. Maps program variables to concrete values or
  symbols `αi`.

- `π` : Path Constraints. A set of all conditions the symbols must
  meet in order to reach the stmt in the execution branch. Always true
  at the beginning.

To better understand how symbolic execution works we are going to look
at an example that illustrates the steps taken by the symbolic execution
engine.

Consider the following code:

**simexec.c.**

``` c
void myFunct(int a, int b){
  int x = 1, y = 0;
  if (a != 5){
    y = 3 * x;
  if (b == 1){
    x = 5 * (a + b);
  }
  }
  assert(x - y != 0);
}
```

Let’s try to find the values that make the assert fail.

<div class="imgblock">

![symbolic](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331103/blog/symbolic-execution-mortals/image1_a56odm.webp)

<div class="title">

Figure 1. Symbolic execution tree of function myFunct()

</div>

</div>

The symbolic execution tree in the image represents the states the
symbolic execution engine goes through during the analysis of the
program, in this case during the analysis of `myFunct()`.

1. The function receives two parameters, `a` and `b`. The symbolic
    execution engine assigns symbols for each parameter: `a → αa` , `b →
    αb`. Since the program hasn’t really began executing, we don’t yet
    have any paths and therefore no constraints, thus `π` is always true
    at the beginning. The next statement to execute is `int x = 1, y
    = 0;` leaving our engine in state `A: σ = {a → αa , b→ αb} π =
    true`.

2. The next statement is executed and two values are assigned. This
    adds `x →1`, `y → 0` to our `σ`. No conditions have been established
    so `π` is still `true`. The next statement to execute is `if (a
    != 5)` leaving our engine in state `B: σ = {a → αa , b → αb, x = 1,
    y = 0} π = true`.

3. Here a decision is made based on the value of the first parameter,
    `a`. Since symbolic execution doesn’t assign concrete values to
    input the initial symbols remain and a will still be equal to `αa`.
    Symbolic execution analyses multiple paths, so the execution tree
    must continue whether the condition is met or not. The symbolic
    execution engine can take two states. If the condition is met,
    `αa!= 5`, that implies a constraint which is added to `π` leaving
    our engine in state `C: σ = {a → αa , b → αb, x = 1, y = 0} π = αa
    != 5` where the next statement to execute would be `y = 3 * x`. If
    the condition is not met, `αa = 5`, that also implies a constraint
    and it must also be added to our `π` leaving our engine in state `D:
    σ = {a → αa , b → αb, x= 1, y = 0} π = αa = 5` and the next
    statement to execute would be the assert which when executed would
    pass all checks meaning the end of that branch.

4. The value of `y` is assigned to be three times that of `x`. The only
    thing this changes is the value of `y` in our `σ` and the next
    statement to execute is a condition leaving our engine in state `E:
    σ = {a → αa , b →αb, x = 1, y = 3} π = αa != 5`.

5. A decision is made based on the value of the second parameter, `b`.
    Both possibilities are evaluated. If the condition is met, `αb = 1`,
    that is another constraint and it is added to our `π`. The next
    statement to execute would be ``x= 5 * a ` b;+
    leaving our engine in state
    `F: σ = {a → αa , b → αb, x = 1, y= 3} π = αa != 5 ∧ αb = 1``. If
    the condition is not met, `αb != 1`, that constraint must also be
    added to our `π` leaving our engine in state `G: σ = {a → αa , b →
    αb, x = 1, y = 3} π = αa!= 5 ∧ αb != 1` where the next statement to
    execute would be the assert which when executed would pass all
    checks meaning the end of that branch.

6. The value of `x` is assigned to be five times the sum of `a` and
    `b`. The only thing this changes is the value of `x` in our `σ`
    leaving our engine in state ``H: σ = {a → αa , b → αb, x = 5(αa `
    αb), y = 3} π = αa != 5 ∧ αb = 1+
    where the next statement to execute would be the assert.
    When the assert, `x -y != 0`` is evaluated the values are replaced
    for what our engine has. ``5(αa `αb) - 3 = 0 ∧ αa != 5 ∧ αb = 1+
    this is the expression that tells me what values will make my assert
    fail.
    To satisfy the previous expression `αa`` has to be equal to `0.6`
    and `αb` has to be `1`.

There it is, we found a property that can be violated and the conditions
that must be met in order to violate it.

## References

1. [A Survey of Symbolic Execution Techniques. Retrieved
    May 4, 2017](https://arxiv.org/pdf/1610.00502.pdf)
