from io import BytesIO
import os
import shutil
from urllib.request import urlopen
from zipfile import ZipFile

import click

SEIDR_SKELETON_URL = (
    "https://github.com/dttctcs/seidr-skeleton/archive/master.zip"
)
SEIDR_STUDIO_URL = (
    "https://github.com/dttctcs/seidr-studio/archive/master.zip"
)


@click.group()
def cli():
    pass


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
        # seidr skeleton
        url = urlopen(SEIDR_SKELETON_URL)
        skeleton_dirname = "seidr-skeleton-main"
        skeleton_zipfile = ZipFile(BytesIO(url.read()))
        skeleton_zipfile.extractall()
        os.rename(skeleton_dirname, name)

        # seidr studio
        url = urlopen(SEIDR_STUDIO_URL)
        studio_dirname = "seidr-studio-main"
        studio_zipfile = ZipFile(BytesIO(url.read()))
        for file in studio_zipfile.namelist():
            if 'build' in file:
                studio_zipfile.extract(file, name)

        # templates and static folder
        build_path = os.path.join(name, studio_dirname, 'build')
        templates_path = os.path.join(name, 'app', 'templates')
        os.mkdir(templates_path)
        shutil.move(os.path.join(build_path, 'index.html'), templates_path)

        static_path = os.path.join(name, 'app', 'static')
        os.mkdir(static_path)
        for file in os.listdir(build_path):
            file_path = os.path.join(build_path, file)
            if 'static' not in file_path:
                shutil.move(file_path, static_path)
            else:
                for f in os.listdir(file_path):
                    sub_path = os.path.join(file_path, f)
                    shutil.move(sub_path, static_path)

        shutil.rmtree(os.path.join(name, skeleton_dirname))

        click.echo(click.style("Downloaded the skeleton app. Happy coding!", fg="green"))
        return True
    except Exception as e:
        click.echo(click.style("Something went wrong {0}".format(e), fg="red"))
        return False
