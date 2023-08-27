import click

from src.commands import add_borders


@click.group()
def stickers_utils():
    pass


@stickers_utils.command()
@click.argument("path")
def add_border(path):
    add_borders.run(path)
