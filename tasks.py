from invoke import task

@task
def start(ctx):
  ctx.run("python3 src/main_game.py")

@task
def lint(ctx):
  ctx.run("pylint src", pty=True)

@task
def format(ctx):
  ctx.run("autopep8 --in-place --recursive src", pty=True)