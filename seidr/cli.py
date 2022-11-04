from io import BytesIO
import os
import shutil
from urllib.request import urlopen
from zipfile import ZipFile
import tempfile
import click


def get_zip(component="-skeleton", branch="main"):
    studio_name = f"seidr{component}-{branch}"
    studio_url = f"https://github.com/dttctcs/seidr{component}/archive/refs/heads/{branch}.zip"
    url = urlopen(studio_url)
    return ZipFile(BytesIO(url.read()))


@click.group()
def cli():
    pass


@cli.command("create-app")
# @click.option(
#    "--name",
#    prompt="Your new app name",
#    help="Your application name, directory will have this name",
# )
def create_app():
    """
        Create a Skeleton application (needs internet connection to github)
    """
    branch = "main"
    try:
        skeleton_zipfile = get_zip(branch=branch)

        with tempfile.TemporaryDirectory() as tmpdirname:
            skeleton_zipfile.extractall(path=tmpdirname)
            skeleton_path = f"seidr-skeleton-{branch}"
            for file in os.listdir(os.path.join(tmpdirname, skeleton_path)):
                if file == ".gitignore":
                    continue
                src_file = os.path.join(tmpdirname, skeleton_path, file)                
                dst_path = os.path.join(".")            
                shutil.move(src_file, dst_path)

        #shutil.move(os.path.join(".", 'app', 'init_api.py'), os.path.join(".", 'app', '__init__.py'))        
        #os.remove(os.path.join(".", 'app', 'init_app.py'))
        #os.chmod('docker-entrypoint.sh', 0o0755)
        click.echo(click.style(
            f"Installed skeletton app from {branch}. Happy coding!\nStart backend with python run.py\nStart frontend in webapp/ with npm i; npm start", fg="green"))
        return True
    except Exception as e:
        click.echo(click.style("Something went wrong {0}".format(e), fg="red"))
        return False