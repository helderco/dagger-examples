"""
Run tests for multiple Python versions.
"""

import anyio
import dagger


async def test(repo_url: str):
    versions = ["3.7", "3.8", "3.9", "3.10", "3.11"]

    async with dagger.Connection() as client:
        repo = client.git(repo_url)

        # get reference to the project's directory
        src_id = await repo.branch("master").tree().id()

        for version in versions:
            python = (
                client.container()
                .from_(f"python:{version}-slim-buster")

                # mount cloned repository into image
                .with_mounted_directory("/src", src_id)

                # set current working directory for next commands
                .with_workdir("/src")

                # install test dependencies
                .exec(["pip", "install", "-e", ".[test]"])

                # run tests
                .exec(["pytest", "tests"])
            )

            print(f"Starting tests for Python {version}")

            # execute
            await python.exit_code()

            print(f"Tests for Python {version} succeeded!")

        print("All tasks have finished")


if __name__ == "__main__":
    # Using the popular FastAPI library as an example
    anyio.run(test, "https://github.com/tiangolo/fastapi")
