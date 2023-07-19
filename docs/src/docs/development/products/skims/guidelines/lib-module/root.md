---
id: root
title: Root module
sidebar_label: ROOT
slug: /development/products/skims/guidelines/lib-module/root
---

The root module searches vulnerabilities in complex code files.

The following procedure is used:

1. Parse the file into a graph object using the tree-sitter libraries
1. Optimize the original graph to extract only relevant information
1. Search vulnerabilities by traversing the optimized graph
1. Generate the vulnerabilities report with each location

For skims developers, the following sections explain in more detail this
process.

## 1. Code parsing (AST graph)

First, the code file is parsed and converted into a graph object,
called the AST (Abstract Syntax Tree).

This process is made using the OS libraries recommended by
[tree-sitter](https://tree-sitter.github.io/tree-sitter/)

In order to support a new language, the tree sitter library repository must
be included in the code dependencies. You can follow this
[commit](https://gitlab.com/fluidattacks/universe/-/commit/1f14d6470c8cce608cfd901cd8c50312b3eacf00)
as reference of the adjustments that have to be made.

The graph object is made up of interconnected nodes that represent each
declaration of the code. Each of these nodes is identified with a unique ID
and other attributes.

Although, a skims' developer does not need to know
the intricacies of the underlying parsing libraries, there is a very important
part of each library's code that should always be verified for the next step.
This file contains the parser's rules and relationships between the nodes,
they are usually stored in a JSON object usually called "node-types",
included in the library source code.
For instance, JavaScript grammar can be found in this
[file](https://github.com/tree-sitter/tree-sitter-javascript/blob/master/src/node-types.json)

This file lists all the node types included in the language, and it includes
all the possible attributes and children nodes of each type. This information
is crucial for the next step.

For example, a function declaration is parsed as a node with a
label_type of "method_declaration". This node is connected to several children,
for example a node for its arguments list, another one for the execution block
and any modifiers or annotations that are unique to each language.
The node can also include attributes that reference some of its children,
in order to make the relationship clearer and make it easier to traverse the
graph.

The AST graphs are generally very good representations of the code, however,
we have found that they have major problems:

- They do not implicitly represent the execution flow of the code,
  that is, they do not include all the possible paths that can be taken
  to reach every code statement within a file.
- The node label types change between languages, which makes it harder
  to program methods to search vulnerabilities. For example, in java, a
  function invocation node is identified as `method_invocation`, whereas in
  JavaScript, they are identified as `call_expression`.
- The nodes in the AST usually contain a lot of unnecessary information,
  such as child nodes for code syntax symbols, such as {};[] and others,
  which makes search algorithms computationally more expensive
  and inefficient.

In order to solve these deficiencies, the AST graph goes through a
re-parsing in the following step.

## 2. Graph optimization

The AST graph is converted into an optimized graph called the
**syntax graph**.

As mentioned above, the purpose of this step is two-fold:

- Reduce the complexity and size of the parsed code.
- Generate a standard graph, using common terminology to represent coding
  concepts that are similar between languages.

This is done by running the AST through a recursive algorithm
and then generating additional connections between nodes in order to accurately
represent the execution flow of the code.

These connections or edges, as they are called, are an important tool in order
to search complex vulnerabilities that depend on many conditions in the code
while ensuring that no false positives are reported.

Each step is explained in more detail in the following subsections.

### 2.1 Syntax graph

The syntax graph is created by filtering only the relevant
information (nodes) of the AST graph, and converting each node type label
into the relevant concept that it represents.

1. Starting at the root node of the AST, a general function
   (called `generic`) is in charge of dispatching the node
   to a relevant `reader` function, which depends on the language
   and label type of the node.

1. This `reader` function extracts only the relevant
   information needed of the node and its important children.
   All this information is then sent to a function called a
   `builder` which depends only on the type of the node (The concept that it
   represents, e.g. A method declaration) and is common between all languages.

1. The `builder` function, as the name implies, creates the node
   for the syntax graph and adds all of its relevant characteristics. It also
   generates the recursion algorithm, by calling the initial `generic` function
   for each of the children nodes.

1. This process runs until all the nodes of the AST graph have been traversed.

After all the nodes have been parsed, the syntax graph goes through another
process that generates the **control flow** connections
between the major declaration nodes.

When making adjustments or adding functionalities to this module,
the node_types file (Mentioned in the first step) from the parser library
of each language must always be verified, to ensure the code is covering
all the possible cases from the language and to avoid any code execution
errors on client files.

### 2.2 Syntax CFG

In order to be able to identify vulnerabilities in code
that depend on several conditions, it is crucial to generate connections
between the nodes of the graph that represent the execution order of the code.

This is why the syntax graph goes through this step, called the syntax CFG,
which stands for control flow graph.

Simply explained, and as the name implies, this step is what generates the CFG
edges of the graph, which connect major nodes that are related to code
execution and scope.

The following procedure is used:

1. As before, a recursive function, called `generic` dispatches each node
   of the graph and, depending on its type, it calls a `dispatcher` function

1. This `dispatcher` function is in charge of adding the edges to the relevant
   nodes that follow in the code execution order. This is done by adding
   a "CFG" label to the edge connecting the nodes.

To best understand this process, run a simple code in the language
of your preference. For example, use the following JS code:

```js
let my_var1 = 2;
let my_var2 = 3;
sum_vars(my_var1, my_var2);
```

Using this snippet, you can see what types of nodes are created
when you declare a variable and invoke a method.

More importantly, from this example you can see how the CFG edges are added
to represent the flow of the code. That is, how the `my_var1` is connected
to `my_var2` and this in turn is finally connected to the `sum_vars`
method invocation.

After that, you can try to add control structures like conditionals,
loops, or switch statements to see how the nodes are connected
by different paths of execution. For example:

```js
let my_var1;
if (some_var == 2){
   my_var1 = 3;
} else {
   my_var1 = 4;
}
let my_var2 = my_var1 + 10;
```

In the previous snippet, the variable `my_var2` can be reached by two different
paths of execution (One when the if condition is true, and another when it is
false). This generates two paths by connecting the `my_var2` node with each
block of the conditional statement.

Before moving on to develop any methods using the syntax graph (Specially
methods that use the symbolic evaluation), it is recommended that you
familiarize yourself with the node types and the concept of the CFG edges,
to see how each part of the code is parsed and be able to debug the
entire process in case any errors arise.

## 3. Vulnerability search

The last step of the process is programming the methods that search for
vulnerabilities in the code, which is generally made by filtering and
searching the syntax graph for vulnerable declarations or invocations.

This last step can be classified according to two basic types
of vulnerabilities.

### 3.1 Direct vulnerabilities

When a vulnerability is a direct consequence of an unsafe object or
function, all the logic is stored in the root module.

This logic uses the syntax graph to filter a certain type of node and
search for the vulnerable name or symbol that identifies the vulnerability.

See the following pseudocode example:

```js
let vuln_var = new danger_object();
```

In this case, the vulnerability can be detected by filtering the syntax graph
and searching for any declarations of the `danger_object`.

Before moving on to the next type of vulnerabilities, it is recommended
that you try to understand and debug one of several methods in root
that only use the syntax graph to search for direct vulnerabilities.

### 3.2 Compound Vulnerabilities

Some vulnerabilities cannot be checked directly by only filtering
a certain dangerous declaration, because they depend on one or several
additional conditions that have to be met simultaneously.

See the following pseudocode example:

```js
let dangerous_var = "danger";

let vuln_method = potential_danger("danger");
let vuln_method1 = potential_danger(dangerous_var);

let safe_method = potential_danger("safe_var");
```

In this case, the method called `potential_danger` is only a vulnerability
when the parameter `danger` is used.

In order for the method to deliver value to the clients, it needs to be able
to distinguish that the third invocation of the method is safe,
and to report both of the first two occurrences of the vulnerability.

This is the purpose of the **symbolic evaluation** algorithm.

#### 3.2.1 Symbolic evaluation

This is a semi-recursive algorithm that follows the following procedure:

1. As with direct vulnerabilities, in the root module,
   the node that could potentially generate the vulnerability is searched
   by filtering the syntax graph.

1. After the potential danger has been found, the node that may generate the
   danger is then filtered (In the example above, it was the parameter of the
   `potential_danger` method invocation)

1. Using this node and the CFG edges of the graph, all the paths in the
   execution order of the code are generated. Each path is simply a list of
   all the nodes that have to be executed for the code to reach the
   analyzed node.

1. The node and its execution paths are sent to the general
   `generic` dispatcher function in the symbolic evaluation module.

1. Depending on the label_type of the node, the `dispatchers` calls a
   `evaluator` function and sends the node and all the arguments of the
   evaluation.

1. Each node type has its own evaluator function that searches and propagates
   the algorithm to other nodes that are somehow related to it.

   For example, the `SymbolLookup` node type evaluator searches in the graph
   for where that symbol is defined or used. If this search finds any nodes,
   the evaluator then propagates the algorithm by calling the `generic`
   function again with each of the found nodes as parameters.

   Another example, a `VariableDeclaration` node type evaluator simply forks
   the algorithm to the `generic` function to the value node of the variable.

1. This process is repeated until it reaches a node type in which the
   `evaluator` has its own specific evaluator condition for the method
   that is being searched.

   Depending on what the vulnerability is, each method can have one or several
   specific `evaluator` conditions, which finally check if the node is
   dangerous according to the vulnerability requirements.

   (In the example above, there would be a specific evaluator for the node type
   "Literal" which would check if the value of the node is equal to "danger")

   If so, this specific `evaluator` functions mark the node as dangerous.

1. The algorithm finishes once all possible paths have been evaluated using this
   same process, and returns two values:

   - A boolean value called danger.
   - A set of string values called the `triggers` (Maybe empty when not needed)

1. If the algorithm returns the boolean value danger as true, the vulnerability
   is marked.

Before moving on to understanding and using the `triggers`, it is
recommended that you understand methods that only use the danger
value to evaluate a vulnerability.

#### 3.2.2 Symbolic evaluation Triggers

Sometimes, a boolean value is not enough to check for a vulnerability,
because it requires several conditions to be met at the same time.

See the following pseudocode example:

```js
let dangerous_var = "danger";

let transformed_val = danger_transformation(dangerous_var);
let vulnerability = potential_danger(transformed_val);

let safe_method = potential_danger(dangerous_var);
```

In this case, the `danger` variable, needs to go through a
`danger_transformation` method before being used in the `potential_danger`
to cause a true vulnerability.

Ensuring this double condition would not be possible only with the use
of a boolean value. This is the main use of the triggers.

The symbolic evaluation works the same way as explained above, only this time,
at the specific evaluator for the method, a value would get added
to the triggers to represent the additional vulnerable condition.

It is recommended that you use the triggers object only when you
fully understand its implications and use cases.
As guidelines, try to debug one of several existing methods that use them.

## 4. Debugging

To see the parsed graphs (Both the AST and the syntax graph),
you can run skims using the --debug flag.

This will generate the two SVG files in the ~.skims folder of your home directory.

You can run the debugger of your IDE in order to see how each step is executed.
The `generic` function found in each module is the origin point of each
step of the algorithm, so it is the most helpful to follow.
