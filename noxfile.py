import os

import nox

source_files = (
    "hstspreload/",
    "test_hstspreload.py",
    "build.py",
    "setup.py",
    "noxfile.py",
)


@nox.session(reuse_venv=True)
def lint(session):
    session.install("autoflake", "black", "flake8", "isort", "seed-isort-config")

    session.run("autoflake", "--in-place", "--recursive", *source_files)
    session.run("seed-isort-config", "--application-directories=hstspreload")
    session.run(
        "isort",
        "--project=hstspreload",
        "--multi-line=3",
        "--trailing-comma",
        "--force-grid-wrap=0",
        "--combine-as",
        "--line-width=88",
        "--recursive",
        "--apply",
        *source_files,
    )
    session.run("black", "--target-version=py36", *source_files)

    check(session)


@nox.session(reuse_venv=True)
def check(session):
    session.install("black", "flake8")

    session.run("black", "--check", "--target-version=py36", *source_files)
    session.run("flake8", "--max-line-length=88", "--ignore=W503,E203", *source_files)


@nox.session(reuse_venv=True)
def build(session):
    session.install("httpx")

    session.run("python", "build.py")


@nox.session(reuse_venv=True)
def test(session):
    session.install("httpx", "pytest")
    session.install(".")

    session.run("python", "-m", "pytest", "-q", "test_hstspreload.py")


@nox.session(reuse_venv=True)
def deploy(session):
    build(session)

    session.install("twine")

    if os.path.isdir("dist"):
        session.run("rm", "-rf", "dist/*")

    session.run("python", "setup.py", "build", "sdist")
    session.run(
        "python",
        "-m",
        "twine",
        "upload",
        "--skip-existing",
        "dist/*",
        "--username",
        os.environ["PYPI_USERNAME"],
        "--password",
        os.environ["PYPI_PASSWORD"],
    )
