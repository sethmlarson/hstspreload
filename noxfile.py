import os

import nox

source_files = (
    "hstspreload/",
    "test_hstspreload.py",
    "build-hstspreload.py",
    "setup.py",
    "noxfile.py",
)


@nox.session(reuse_venv=True)
def format(session):
    session.install("-rrequirements/lint.txt")

    session.run("autoflake", "--in-place", "--recursive", *source_files)
    session.run(
        "isort",
        "--profile=black",
        *source_files,
    )
    session.run("black", "--target-version=py39", *source_files)

    lint(session)


@nox.session(reuse_venv=True)
def lint(session):
    session.install("-rrequirements/lint.txt")

    session.run("black", "--check", "--target-version=py39", *source_files)
    session.run("flake8", "--max-line-length=88", "--ignore=W503,E203", *source_files)


@nox.session(reuse_venv=True)
def build(session):
    session.install("-rrequirements/test.txt")

    session.run("python", "build-hstspreload.py")


@nox.session(reuse_venv=True)
def test(session):
    session.install("-rrequirements/test.txt")
    session.install(".")

    session.run("python", "-m", "pytest", "-q", "test_hstspreload.py")


@nox.session(reuse_venv=True)
def deploy(session):
    session.install("-rrequirements/deploy.txt")

    if os.path.isdir("dist"):
        session.run("rm", "-rf", "dist/*")

    session.run("python", "-m", "build")

    if os.getenv("PYPI_TOKEN"):
        username = "__token__"
        password = os.getenv("PYPI_TOKEN")
    else:
        username = os.environ["PYPI_USERNAME"]
        password = os.environ["PYPI_PASSWORD"]

    session.run(
        "python",
        "-m",
        "twine",
        "upload",
        "--skip-existing",
        "dist/*",
        f"--username={username}",
        f"--password={password}",
        success_codes=[0, 1],
    )
