import os, shutil
import click

from captains_log.conf.install import install_app
from captains_log.backend.init import init_database
from captains_log.backend.models import CaptainsLogDatabase, Category, Entry

@click.command()
@click.option('--force/--no-force', default=False, help="Don't prompt user to ask for install")
@click.pass_context
def install_command(context, force=False):
    """
    To install the required script config
    """
    settings = context.obj['settings']
    
    if not force:
        click.confirm('Do you want to continue for installing my needed stuff?', default=True, abort=True)
    click.echo("Make it so!")
    
    install_app(settings)

    click.echo("Captain, it seems we've finished. Engage!")


@click.command()
@click.option('--force/--no-force', default=False, help="Don't prompt user to ask for reset")
@click.pass_context
def reset_command(context, force):
    """
    To restart with a new install
    """
    settings = context.obj['settings']
    
    if not force:
        click.confirm('Captain, this will reset your install and erase all your logs, are you sure ?', abort=True)
    click.echo("Setting Phasers on kill!")
    
    # Remove previous config
    if os.path.exists(settings['config_dir']):
        shutil.rmtree(settings['config_dir'])
    
    # Then redo install
    install_app(settings)
    