"""
Simple example using cowsay.

Try with::

    $ python say.py "Simple is better than complex"
"""

import sys

import anyio
import dagger

from rich.console import Console

console = Console()

async def main(args: list[str]):
    with console.status("Hold on..."):
        async with dagger.Connection() as client:
            # build container with cowsay entrypoint
            # note: this is reusable, no request is made to the server
            ctr = (
                client.container()
                .from_("python:alpine")
                .exec(["pip", "install", "cowsay"])
                .with_entrypoint(["cowsay"])
            )

            # run cowsay with requested message
            # note: queries are executed only on coroutines
            result = await ctr.exec(args).stdout()

    print(result)


if __name__ == "__main__":
    anyio.run(main, sys.argv[1:])
