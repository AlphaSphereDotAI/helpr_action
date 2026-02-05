from typing import Annotated

from dagger import Container, Directory, Doc, dag, function, object_type


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
    def base(self) -> Container:
        """Return a base container."""
        return dag.wolfi().container()

    @function
    async def build_and_publish(
        self,
        src: Annotated[Directory, Doc("location of directory containing Dockerfile")],
        build_args: list[str],
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
    async def get_python_version(
        self,
        src: Annotated[Directory, Doc("location of directory containing Dockerfile")],
    ) -> str:
        """Return the Python version used in pyproject.toml."""
        return await dag.yq(src).get(".project.requires-python", "pyproject.toml")
