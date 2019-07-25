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
    session.install("black")

    session.run("black", "--target-version=py36", *source_files)

    check(session)


@nox.session(reuse_venv=True)
def check(session):
    session.install("black", "flake8")

    session.run("black", "--target-version=py36", "--check", *source_files)
    session.run("flake8", "--max-line-length=88", "--ignore=E203,W503", *source_files)


@nox.session(reuse_venv=True)
def build(session):
    session.install("httpx")

    session.run("python", "build.py", success_codes=[0, 100])


@nox.session(reuse_venv=True)
def test(session):
    session.install("httpx", "pytest", "pytest-xdist")
    session.install(".")

    session.run("python", "-m", "pytest", "-q", "-n", "4", "test_hstspreload.py")


@nox.session(reuse_venv=True)
def upload(session):
    session.install("twine")

    session.run("rm", "-rf", "dist/*")
    session.run("python", "setup.py", "build", "sdist")
    session.run(
        "python",
        "-m",
        "twine",
        "upload",
        "--ignore-existing",
        "dist/*",
        "--username",
        os.environ["PYPI_USERNAME"],
        "--password",
        os.environ["PYPI_PASSWORD"],
    )
