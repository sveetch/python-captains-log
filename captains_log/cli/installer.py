import os, shutil
import click

from captains_log.backend.init import init_database
from captains_log.backend.models import CaptainsLogDatabase, Category, Entry

def install_app(settings):
    """
    Common method to install app's stuff
    """
    if not os.path.exists(settings['config_dir']):
        click.echo("* Creating the dedicated directory to: {0}".format(settings['config_dir']))
        os.makedirs(settings['config_dir'])
    else:
        click.echo("* Fascinating, the dedicated directory allready exists at: {0}".format(settings['config_dir']))
    
    if not os.path.exists(settings['database_filepath']):
        click.echo("* We need to create the database to: {0}".format(settings['database_filepath']))
        init_database(settings, naive=True)
        CaptainsLogDatabase.create_tables([Category, Entry])
    else:
        click.echo("* It is illogical, the database allready exists at: {0}".format(settings['database_filepath']))


@click.command()
@click.option('--force', default=False, help="Don't prompt user to ask for install")
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
@click.pass_context
def reset_command(context):
    """
    To restart from a new install
    
    Just remove app's directory and relaunch an install
    """
    settings = context.obj['settings']
    
    click.confirm('Captain, this will reset your install and erase all your logs, are you sure ?', abort=True)
    click.echo("Setting Phasers on kill!")
    
    if os.path.exists(settings['config_dir']):
        shutil.rmtree(settings['config_dir'])

    install_app(settings)
    