import tomllib
from pathlib import Path
from typing import Annotated

import dagger
from dagger import BuildArg, Doc, dag, function, object_type


def get_image_tag(github_ref: str) -> list[str]:
    """Return the image tag to use for publishing."""
    if github_ref.startswith("refs/tags/"):
        return [github_ref.removeprefix("refs/tags/"), "latest"]
    if github_ref.startswith("refs/heads/"):
        branch_name: str = github_ref.removeprefix("refs/heads/")
        return [branch_name.replace("/", "-")]
    if github_ref.startswith("refs/pull/"):
        pr_number: str = github_ref.removeprefix("refs/pull/").split("/")[0]
        return [f"pr-{int(pr_number)}"]
    msg: str = f"Unsupported GitHub ref: {github_ref}"
    raise ValueError(msg)


@object_type
class HelprAction:
    """Dagger object type for HelprAction."""

    @function
    def base(self) -> dagger.Container:
        """Return a base container."""
        return dag.wolfi().container()

    @function
    async def build_and_publish(
        self,
        src: Annotated[dagger.Directory, Doc("location of directory containing Dockerfile")],
        build_args: list[BuildArg],
        image_registry: Annotated[str, Doc("registry of the image to publish")],
        image_name: Annotated[str, Doc("image name of the image to publish")],
        github_ref: Annotated[str, Doc("GitHub ref to determine image tag")],
    ) -> list[str]:
        """Build and publish image from existing Dockerfile."""
        image_tags: list[str] = get_image_tag(github_ref)
        return [
            await src.docker_build(build_args=build_args).publish(f"{image_registry}/{image_name}:{image_tag}")
            for image_tag in image_tags
        ]

    @function
    def get_python_version(self) -> str:
        """Return the Python version used in pyproject.toml."""
        pyproject_path = Path("pyproject.toml")
        if not pyproject_path.exists():
            msg = "pyproject.toml not found"
            raise FileNotFoundError(msg)
        with pyproject_path.open("rb") as f:
            pyproject_data = tomllib.load(f)
        requires_python = pyproject_data["project"]["requires-python"]
        requires_python = requires_python.removeprefix(">=")
        if "," in requires_python:
            requires_python = requires_python.split(",")[0].strip()
        return requires_python
