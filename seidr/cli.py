from io import BytesIO
import os
from urllib.request import urlopen
from zipfile import ZipFile
import click

REPO_URL = (
    "https://github.com/dttctcs/seidr-skeleton/archive/master.zip"
)


@click.group()
def cli():
    pass


@cli.command()
def hello():
    click.echo("Hello World")


@cli.command("create-app")
@click.option(
    "--name",
    prompt="Your new app name",
    help="Your application name, directory will have this name",
)
def create_app(name):
    """
        Create a Skeleton application (needs internet connection to github)
    """
    try:
        url = urlopen(REPO_URL)
        dirname = "seidr-test"
        zipfile = ZipFile(BytesIO(url.read()))
        zipfile.extractall()
        os.rename(dirname, name)
        click.echo(click.style("Downloaded the skeleton app, good coding!", fg="green"))
        return True
    except Exception as e:
        click.echo(click.style("Something went wrong {0}".format(e), fg="red"))
        return False
