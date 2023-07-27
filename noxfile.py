import nox
import toml

nox.options.stop_on_first_error = False
nox.options.reuse_existing_virtualenvs = True

with open("./pyproject.toml") as pyproj_toml:
    parsed_toml = toml.load(pyproj_toml)
    project_name = parsed_toml["tool"]["poetry"]["name"].replace("-", "_")


@nox.session(python=False)
def poetry(session):
    session.run("poetry", "install", external=True)


@nox.session(python=False)
def isort(session):
    session.run("isort", ".", external=True)


@nox.session(python=False)
def black(session):
    session.run("black", ".", external=True)


@nox.session(python=False)
def tests(session):
    session.run("pytest", "-rap", "-p", "no:faulthandler", "tests/", external=True)


@nox.session(python=False)
def coverage(session):
    session.run(
        "coverage",
        "run",
        f"--source={project_name}",
        "-m",
        "pytest",
        "-p",
        "no:faulthandler",
        "./tests/",
        external=True,
    )
    session.run("coverage", "report", "--fail-under=80", "-m", external=True)


@nox.session(python=False)
def flake8(session):
    session.run("flake8", project_name, external=True)


@nox.session(python=False)
def pylint(session):
    session.run("pylint", project_name, external=True)


@nox.session(python=False)
def mypy(session):
    session.run(
        "mypy",
        "--show-error-codes",
        project_name,
        "tests",
        external=True,
    )


@nox.session(python=False)
def bandit(session):
    session.run("bandit", "-r", "-v", project_name, external=True)


@nox.session(python=False)
def build(session):
    session.run("poetry", "build", external=True)
