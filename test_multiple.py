"""
Run tests for multiple Python versions.
"""

import anyio
import dagger

from rich.console import Console

console = Console()


async def test(repo_url: str):
    versions = ["3.7", "3.8", "3.9", "3.10", "3.11"]

    with console.status("Connecting to engine...") as status:
        async with dagger.Connection() as client:
            repo = client.git(repo_url).branch("master").tree()

            for version in versions:
                console.log(f"Starting tests for Python {version}")

                status.update(f"Testing Python {version}")

                python = (
                    client.container()
                    .from_(f"python:{version}-slim-buster")

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

    console.print("All tests succeeded ✓", style="bold green")


# Using the popular FastAPI library as an example
anyio.run(test, "https://github.com/tiangolo/fastapi")
