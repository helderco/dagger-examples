"""
Run tests using concurrency
"""

import anyio
import dagger
from rich.console import Console

console = Console()


async def test(repo_url: str):
    versions = ["3.7", "3.8", "3.9", "3.10", "3.11"]

    with console.status("Connecting to engine...") as status:
        async with dagger.Connection() as client:
            status.update("Running tests...")

            repo = client.git(repo_url).branch("master").tree()

            async def test_version(version: str):
                console.log(f"Starting tests for Python {version}")

                python = (
                    client.container()
                    .from_(f"python:{version}-slim-buster")
                    .with_mounted_directory("/src", repo)
                    .with_workdir("/src")
                    .with_exec(["pip", "install", "-e", ".[test]"])
                    .with_exec(["pytest", "tests"])
                )

                await python.exit_code()

                console.log(f"Tests for Python {version} succeeded")

            # when this block exits, all tasks will be awaited (i.e., executed)
            async with anyio.create_task_group() as tg:
                for version in versions:
                    tg.start_soon(test_version, version)

    console.print("All tests succeeded ✓", style="bold green")


# Using the popular FastAPI library as an example
anyio.run(test, "https://github.com/tiangolo/fastapi")
