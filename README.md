# Examples for the Dagger Python SDK

This is collection of examples for running [Dagger](https://dagger.io/) pipelines using Python.

## Requirements

- Python 3.10+
- [Poetry](https://python-poetry.org/docs/)
- [Docker](https://docs.docker.com/engine/install/)

## Feedback wanted

The Python SDK is in **technical preview**. The Dagger team appreciates any feedback
to help make it better. So hack away at these examples or try different things.

You can create issues in GitHub, or come join us on our community server.

Thank you!

## Learn more

- [How does it work?](https://docs.dagger.io/#how-does-it-work)
- [Getting started](https://docs.dagger.io/#getting-started)
- [Join the Dagger community server](https://discord.gg/ufnyBtc8uY)
- [Follow us on Twitter](https://twitter.com/dagger_io)

## Tips

These tips may be helpful to understand:

- The underlying API is the same as with the Go SDK, so if you understand the few differences you can easily port from one to another and reuse some of that documentation as well;
- The Go SDK [no longer needs to pass IDs around](https://github.com/dagger/dagger/issues/3558) but in Python you still do for now;
- The `dagger.Client` is a typed query builder. Some methods are just building the query and not executing anything. Only on [scalar values](https://graphql.org/learn/schema/#scalar-types) (`str`, `int`...) a [coroutine](https://docs.python.org/3/library/asyncio-task.html#coroutines) is returned, in which case you need to `await` to execute it;
- Only _async_ is supported at the moment. I suggest this simple primer for those who aren't familiar with it: [First Steps with AnyIO](https://asyncer.tiangolo.com/tutorial/first-steps/);
- Notice that when you use an `.id()` field, it'll execute a query but nothing will actually be run (it's lazy, see issue in second bullet);
- Notice the type hints in the IDE, they help document what you can do.
