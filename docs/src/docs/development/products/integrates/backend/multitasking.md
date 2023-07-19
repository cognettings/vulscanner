---
id: multitasking
title: Multitasking
sidebar_label: Multitasking
slug: /development/products/integrates/backend/multitasking
---

## Introduction

_It's all about doing multiple things at the same time._

After reading this page,
you will have a clearer understanding of multitasking,
and how you can use it to build software
that makes the most out of the available hardware.

## In web servers

A server typically handles one request at a time,
which means that until it finishes,
the others will be waiting.

This isn't optimal,
so it's common practice for a server
to spawn multiple [copies of itself][fork],
allowing it to handle more requests,
but still,
each copy handles no more than 1 request at a time.

Back in the early 2000s as the web was getting more popular,
software engineers had to tackle the [C10K problem][c10k],
and they found that to handle 10000 requests at the same time,
the aforementioned approach would not suffice,
so there were two options:

1. **Use some form of single-threaded asynchronous I/O**,
  relying on Operating System support to trigger I/O operations,
  and [notify later][callback] once completed,
  allowing the program to continue serving others in the meantime.

1. **Use multi-threading to serve one client per thread**,
  but take a hit in resource consumption,
  as each thread allocates a portion of memory for its stack,
  and spends some CPU cycles in [context switching][context],
  which in the hardware of that era was a matter of big concern.

Sometime later,
projects implementing the first one started to emerge
and gained popularity,
notably [NGINX][nginx],
[Node.js][node],
and [Twisted][twisted].

## Options

Let's explore the options to do multitasking in Python.

:::tip
⚙️ **CPU-bound functions**: Mathematical operations
  or iterating over large sets of data.

  ```python
  def cpu_bound_function():
    i = 0
    while i < 999_999_999:
      i += 1
    return i
  ```

🌐 **I/O-bound functions**: Reading from
  or writing to a file, network, or database.

  ```python
  def io_bound_function():
    response = requests.get("https://veryslowsite.com/")
    return response
  ```

:::

### Threads

Good for 🌐 **I/O-bound functions**

https://docs.python.org/3/library/threading.html

You can think of threads as multiple lanes on a highway,
where each lane provides an independent path for drivers
to go towards their destination.
This enables multiple drivers to move simultaneously,
without being blocked by traffic in other lanes.

Threads are the most common approach to do multitasking,
but unfortunately in Python,
it's not ideal for ⚙️ **CPU-bound functions**
due to some of its [design limitations][gil],
which makes them unable to take full advantage of multi-core processors.

```python
from threading import Thread

def get_data():
  result = database.query()
  return result

def send_mail():
  result = mailer.send()
  return result

t1 = Thread(target=get_data)
t2 = Thread(target=send_mail)

t1.start()
t2.start()

t1.join()
t2.join()
```

### Processes

Good for ⚙️ **CPU-bound functions**

https://docs.python.org/3/library/multiprocessing.html

Python provides a way to run functions in a separate process,
allowing it to bypass the aforementioned limitations,
and make use of all the available CPU cores.

```python
from multiprocessing import Process

def calculate_fibonacci():
  result = fibonacci(100)
  return result

def calculate_pi():
  result = digits_of_pi(100)
  return result

p1 = Process(target=calculate_fibonacci)
p2 = Process(target=calculate_pi)

p1.start()
p2.start()

p1.join()
p2.join()
```

### Async I/O

Good for 🌐 **I/O-bound functions**

https://docs.python.org/3/library/asyncio.html

Web applications commonly involve
reading/writing to files,
databases,
and calling external services via HTTP requests.
All of that time spent waiting for each call to complete is
time wasted not processing other stuff,
so here is where async I/O comes in handy
to improve the throughput of an application.

Unlike threads,
where the Operating System's scheduler [preemptively][preemptive] decides
when to execute and interrupt functions,
in this model functions [cooperate][cooperative] so they're executed one at a time,
but each explicitly yields control to the next one when it has completed its work
or when it is waiting for some event to occur, such as I/O completion.

```python
import aioextensions
# ^ Fluid Attacks library with asyncio utils to simplify its usage

async def get_data():
  result = await database.query()
  # ^ This will take a while. Keep going and we'll talk later
  return result

async def send_mail():
  result = await mailer.send()
  return result

# While get_data waits for its query, send_mail will be executed
# It's doing multiple things at the same time 🙌
await aioextensions.collect([
  get_data(),
  send_mail(),
])
```

So, in this way of doing things,
you get the benefits of multitasking
without worrying about issues such as [thread safety][threads],
but it also comes with its challenges.

#### Challenges

The main challenge of using cooperative multitasking
is that it requires cooperation from all functions in the application.

In cooperative multitasking,
each function is responsible for voluntarily yielding control to other functions
when it is not actively doing work,
for instance,
after it triggered a database query
and is now just waiting for the response.

This means that if a function fails to yield control when needed,
it can lead to delays in processing other requests,
or even cause the entire application server to become unresponsive.

You can identify and mitigate these problems,
but they represent a risk inherent to this design,
and in cases where reliability takes priority over performance requirements,
this model may not be the most appropriate.

:::tip
Try running the following examples in your Python console
and spot the difference
:::

```python
import asyncio
import aioextensions

async def get_data():
  print("get_data started")
  await asyncio.sleep(5)
  print("get_data finished")

async def send_mail():
  print("send_mail started")
  await asyncio.sleep(3)
  print("send_mail finished")

aioextensions.run(
  aioextensions.collect([
    get_data(),
    send_mail(),
  ])
)
```

```python
import asyncio
import aioextensions
import time

async def get_data():
  print("get_data started")
  time.sleep(5)
  # ^ From the good old standard library, what could go wrong?
  print("get_data finished")

async def send_mail():
  print("send_mail started")
  await asyncio.sleep(3)
  print("send_mail finished")

# 😰 Oh no, get_data calls a ⌛️ blocking function
# send_mail will not even be triggered until it finishes!
aioextensions.run(
  aioextensions.collect([
    get_data(),
    send_mail(),
  ])
)
```

## FAQ

* **Why was asyncio chosen for usage in our products?**

  Cooperative multitasking is considered a good
  approach for applications with lots of 🌐 **I/O-bound functions**.

  Before 2019, all our products used classic synchronous Python,
  but it was decided to follow the trend in the ecosystem embracing asyncio,
  with the goal of enabling performance improvements.

  Some products still find threads and processes more fitting for their use case
  and that's fine.
* **What should I keep in mind when working on asyncio applications?**

  1. Do not use ⌛️ blocking functions
  1. You do not use ⌛️ blocking functions
  1. Avoid using ⌛️ blocking functions
* **For real, what are some tips to avoid breaking stuff?**

  1. Be aware of ⌛️ blocking functions
    and either look for asyncio-compatible alternatives
    or wrap calls using `in_thread` to make them non-blocking.
  1. Many functions in Python's standard library are ⌛️ blocking,
    as it pre-dates the asyncio way of doing things.
  1. If you're using a 3rd party library,
    look for `asyncio` support in the docs,
    and if it doesn't have,
    consider opening an issue to let the maintainers know.
* **So, is `in_thread` as good as native asyncio? Why don't we just use it everywhere?**

  Running code in a separate thread comes with some overhead,
  so only use it when necessary
  for specific 🌐 **I/O-bound functions** that are known to be ⌛️ blocking.
* **But what exactly is a ⌛️ blocking function?**

  Anything that takes too long before returning or yielding control (using `await`).

  Some commonly used examples include:
  * `requests`
  * `urllib.request.urlopen`
  * `time.sleep`
  * `subprocess.run`
  * `open` (including `file.read`, `file.write`, and `file.seek`).
* **Couldn't we just lint it in the CI pipeline?**

  It is tricky since as previously mentioned,
  any function can be considered ⌛️ blocking if it takes long enough.

  One approach would be to have a list of functions that are known to be ⌛️ blocking,
  and break the build if one of them is used in the code.
  At the time of writing,
  the closest thing to a linter for this case would be [flake8-async][flake8],
  which is likely better than nothing,
  but falls short in detecting some cases.
* **What happens if I use `in_process` to run 🌐 I/O-bound functions?**

  It will still work,
  but there's no point to it
  as using multiple processes only favors ⚙️ **CPU-bound functions**.
  For this use case threads are fine
  and have less overhead.
* **What happens if I declare a function as `async def` but never use await inside?**

  ```python
  async def do_something():
    return "Hello world"
  ```

  It will still run like a normal function,
  but it will have some (usually trivial) overhead
  as Python needs to generate additional code behind the scenes
  to treat it as a 'coroutine'.

## Further reading

* https://eng.paxos.com/python-3s-killer-feature-asyncio
* https://realpython.com/python-concurrency/
* https://realpython.com/async-io-python
* http://c10m.robertgraham.com/p/manifesto.html

[fork]: https://en.wikipedia.org/wiki/Fork_(system_call)
[c10k]: http://www.kegel.com/c10k.html
[callback]: https://en.wikipedia.org/wiki/Callback_(computer_programming)
[context]: https://en.wikipedia.org/wiki/Context_switch
[nginx]: https://www.nginx.com/
[node]: https://nodejs.org/
[twisted]: https://twisted.org/
[gil]: https://realpython.com/python-gil/
[preemptive]: https://en.wikipedia.org/wiki/Preemption_(computing)#PREEMPTIVE
[cooperative]: https://en.wikipedia.org/wiki/Cooperative_multitasking
[threads]: https://en.wikipedia.org/wiki/Thread_safety
[flake8]: https://github.com/cooperlees/flake8-async
