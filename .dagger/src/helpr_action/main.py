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
    def container_echo(self, string_arg: str) -> dagger.Container:
        """Return a container that echoes whatever string argument is provided."""
        return dag.container().from_("alpine:latest").with_exec(["echo", string_arg])

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
