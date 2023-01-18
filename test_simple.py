"""
Run tests for a single Python version.
"""

import anyio
import dagger
from rich.console import Console

console = Console()


async def test(repo_url: str):
    with console.status("Connecting engine...") as status:
        async with dagger.Connection() as client:
            status.update("Running tests...")

            repo = client.git(repo_url).branch("master").tree()

            python = (
                client.container()
                .from_("python:3.11-slim-buster")

                # mount cloned repository into image
                .with_mounted_directory("/src", repo)

                # set current working directory for next commands
                .with_workdir("/src")

                # install test dependencies
                .with_exec(["pip", "install", "-e", ".[test]"])

                # run tests
                .with_exec(["pytest", "tests"])
            )

            # execute
            await python.exit_code()

    console.print("Tests succeeded ✓", style="bold green")


# Using the popular FastAPI library as an example
anyio.run(test, "https://github.com/tiangolo/fastapi")
