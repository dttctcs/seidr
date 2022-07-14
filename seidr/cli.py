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

        shutil.move(os.path.join(".", 'app', 'init_api.py'), os.path.join(".", 'app', '__init__.py'))        
        os.remove(os.path.join(".", 'app', 'init_app.py'))
        os.chmod('docker-entrypoint.sh', 0o0755)
        click.echo(click.style(
            f"Installed skeletton app from {branch}. Happy coding!", fg="green"))
        return True
    except Exception as e:
        click.echo(click.style("Something went wrong {0}".format(e), fg="red"))
        return False


@cli.command("install-studio")
def install_studio():
    """
        Installed seidr studio and updates index.html + __init__.py
    """
    try:
        branch = "main"
        with tempfile.TemporaryDirectory() as tmpdirname:
            studio_zipfile = get_zip(component="-studio", branch=branch)
            for file in studio_zipfile.namelist():
                if 'build' in file:
                    studio_zipfile.extract(file, tmpdirname)

            # templates and static folder
            studio_name = f"seidr-studio-{branch}"
            build_path = os.path.join(tmpdirname, studio_name, 'build')
            static_src_path = os.path.join(
                tmpdirname, studio_name, 'build')
            templates_path = os.path.join('.', 'app', 'templates')
            static_path = os.path.join('.', 'app', 'static')

            if not os.path.exists(templates_path):
                os.mkdir(templates_path)
            index_dst = os.path.join(templates_path, 'index.html')          
            if os.path.exists(index_dst):
                os.remove(index_dst)
            shutil.move(os.path.join(build_path, 'index.html'), index_dst)
            if not os.path.exists(static_path):
                os.mkdir(static_path)
            for file in os.listdir(static_src_path):
                file_path = os.path.join(static_src_path, file)
                dst_file = os.path.join(static_path, file)
                if os.path.exists(dst_file):
                    os.remove(dst_file)
                if 'static' not in file_path:
                    shutil.move(file_path, static_path)
                else:
                    for f in os.listdir(file_path):
                        sub_path = os.path.join(file_path, f)
                        dst_path = os.path.join(static_path, f)
                        if os.path.exists(dst_file) and os.path.isdir(s)(dst_file):
                            continue
                        shutil.move(sub_path, dst_path)                                                
                                    
            

        skeleton_zipfile = get_zip(branch=branch)

        with tempfile.TemporaryDirectory() as tmpdirname:
            for file in skeleton_zipfile.namelist():
                if 'init_app.py' in file:
                    skeleton_zipfile.extract(file, tmpdirname)
                    break
            
            skeleton_path = f"seidr-skeleton-{branch}"
            

            init_app_path = os.path.join(tmpdirname, skeleton_path, 'app', 'init_app.py')
            init_path = os.path.join("./", 'app', '__init__.py')
            if os.path.exists(init_path):
                os.remove(init_path)
            shutil.move(init_app_path, init_path)
            

        click.echo(click.style(
            f"Installed studio webapp from {branch}. Happy coding!", fg="green"))
        return True
    except Exception as e:
        click.echo(click.style("Something went wrong {0}".format(e), fg="red"))
        return False
