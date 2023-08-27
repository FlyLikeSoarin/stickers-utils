import click

from src.commands import add_borders as add_borders_command
from src.commands import download_stickerset as download_stickerset_command
from src.commands import upload_stickerset as upload_stickerset_command


@click.group()
def stickers_utils():
    pass


@stickers_utils.command()
@click.argument("path")
def add_borders(path: str):
    add_borders_command.run(path)


@stickers_utils.command()
@click.argument("stickerset_name")
def download_stickerset(stickerset_name: str):
    download_stickerset_command.run(stickerset_name)


@stickers_utils.command()
@click.argument("stickerset_folder")
def upload_stickerset(stickerset_folder: str):
    upload_stickerset_command.run(stickerset_folder)
