import nox

nox.options.sessions = ["lint", "test"]


@nox.session
def lint(session: nox.Session):
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files", "--show-diff-on-failure")


@nox.session(python=["3.6", "3.7", "3.8", "3.9", "3.10"])
def test(session: nox.Session):
    session.install("-e", ".", "pytest", "pytest-cov")
    session.run(
        "pytest", "--cov=asymmetric_matchers", "--cov-report=xml", *session.posargs
    )
