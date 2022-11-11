"""
Simple example using cowsay.

Try with::

    $ python say_sync.py "Simple is better than complex"
"""

import sys

import dagger

from rich.console import Console

console = Console()


def main(args: list[str]):
    with console.status("Hold on..."):
        with dagger.Connection() as client:
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
            result = ctr.exec(args).stdout().contents()

            print(result)


if __name__ == "__main__":
    main(sys.argv[1:])
