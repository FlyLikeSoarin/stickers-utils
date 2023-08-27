import subprocess

import click


@click.group()
def utils():
    pass


@utils.command()
def lint():
    routines = (
        subprocess.run(["isort", "--check", "src"]),
        subprocess.run(["black", "--quiet", "--check", "--diff", "src"]),
        subprocess.run(["flake8"]),
        subprocess.run(["mypy", "--no-error-summary", "src"]),
    )

    if all(routine.returncode == 0 for routine in routines):
        print("All linters passed")
        exit(0)

    exit(1)


@utils.command()
def format():
    subprocess.run(["isort", "src"])
    subprocess.run(["black", "src"])


if __name__ == "__main__":
    utils()
