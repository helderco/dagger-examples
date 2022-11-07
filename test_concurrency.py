"""
Run tests using concurrency
"""

import anyio
import dagger


async def test_version(version: str, src_id, client: dagger.Client):
    python = (
        client.container()
        .from_(f"python:{version}-slim-buster")
        .with_mounted_directory("/src", src_id)
        .with_workdir("/src")
        .exec(["pip", "install", "-e", ".[test]"])
        .exec(["pytest", "tests"])
    )

    print(f"Starting tests for Python {version}")

    await python.exit_code()

    print(f"Tests for Python {version} succeeded!")



async def test(repo_url: str):
    versions = ["3.7", "3.8", "3.9", "3.10", "3.11"]

    async with dagger.Connection() as client:
        repo = client.git(repo_url)
        src_id = await repo.branch("master").tree().id()

        # when this block exits, all tasks will be awaited (i.e., executed)
        async with anyio.create_task_group() as tg:
            for version in versions:
                tg.start_soon(test_version, version, src_id, client)

        print("All tasks have finished")


if __name__ == "__main__":
    # Using the popular FastAPI library as an example
    anyio.run(test, "https://github.com/tiangolo/fastapi")
