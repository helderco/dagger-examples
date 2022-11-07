"""
Run tests for a single Python version.
"""

import anyio
import dagger


async def test(repo_url: str):
    async with dagger.Connection() as client:
        repo = client.git(repo_url)

        # get reference to the project's directory
        src_id = await repo.branch("master").tree().id()

        python = (
            client.container()
            .from_("python:3.10-slim-buster")

            # mount cloned repository into image
            .with_mounted_directory("/src", src_id)

            # set current working directory for next commands
            .with_workdir("/src")

            # install test dependencies
            .exec(["pip", "install", "-e", ".[test]"])

            # run tests
            .exec(["pytest", "tests"])
        )

        # execute
        await python.exit_code()

        print("Tests succeeded!")


if __name__ == "__main__":
    # Using the popular FastAPI library as an example
    anyio.run(test, "https://github.com/tiangolo/fastapi")
