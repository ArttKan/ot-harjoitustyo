from invoke import task


@task
def start(ctx):
    ctx.run("python3 src/index.py", pty=True)


@task
def test(ctx):
    ctx.run("pytest", pty=True)


@task
def coverage_report(ctx):
    ctx.run("coverage run --branch -m pytest", pty=True)
    ctx.run("coverage report -m", pty=True)


@task
def coverage_report_html(ctx):
    ctx.run("coverage html", pty=True)
    ctx.run("open htmlcov/index.html", pty=True)
