"""
We need to check that __version__ is a valid version string, and that it
matches the version in pyproject.toml and the version in the Dockerfile.

We should also ensure that there is a section in the CHANGELOG for the new version.
"""
import re
import subprocess
from pathlib import Path

from packaging import version

from gpyt_eventbus import __version__


def test_poetry_version():
    poetry_version = subprocess.run(
        ["poetry", "version"], stdout=subprocess.PIPE, check=True
    ).stdout.decode("utf-8")
    poetry_version = poetry_version.strip()
    assert re.match(r"^gpyt-eventbus \d+\.\d+\.\d+$", poetry_version)


def test_imported_version():
    assert isinstance(version.parse(__version__), version.Version)


def test_version_in_dockerfile():
    dockerfile = Path(__file__).parent.parent.parent / "Dockerfile"
    with open(dockerfile) as f:
        dockerfile_contents = f.read()
    assert f"ARG VERSION={__version__}" in dockerfile_contents


def test_version_in_pyproject_toml():
    pyproject_toml = Path(__file__).parent.parent.parent / "pyproject.toml"
    with open(pyproject_toml) as f:
        pyproject_toml_contents = f.read()
    assert f'version = "{__version__}"' in pyproject_toml_contents


def test_version_in_init():
    init = Path(__file__).parent.parent.parent / "gpyt_eventbus" / "__init__.py"
    with open(init) as f:
        init_contents = f.read()
    assert f'__version__ = "{__version__}"' in init_contents


def test_changelog():
    changelog = Path(__file__).parent.parent.parent / "CHANGELOG.md"
    with open(changelog) as f:
        changelog_contents = f.read()
    assert f"## {__version__}" in changelog_contents
