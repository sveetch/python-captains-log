# -*- coding: utf-8 -*-
import os, shutil
import click

from captains_log.conf.install import install_app
from captains_log.backend.init import init_database
from captains_log.backend.models import CaptainsLogDatabase, Category, Entry

from captains_log.conf import settings

@click.command()
@click.option('--force/--no-force', default=False, help="Don't prompt user to ask for install")
@click.pass_context
def install_command(context, force=False):
    """
    Install the required config
    """
    if not force:
        click.confirm('Do you want to continue for installing my needed stuff?', default=True, abort=True)
    click.echo("Make it so!")
    
    install_app()

    click.echo("Captain, it seems we've finished. Engage!")


@click.command()
@click.option('--force/--no-force', default=False, help="Don't prompt user to ask for reset")
@click.pass_context
def reset_command(context, force):
    """
    Restart with a new install
    """
    if not force:
        click.confirm('Captain, this will reset your install and erase all your logs, are you sure ?', abort=True)
    click.echo("Setting Phasers on kill!")
    
    # Remove previous config
    if os.path.exists(settings.CONFIG_DIR):
        shutil.rmtree(settings.CONFIG_DIR)
    
    # Then redo install
    install_app()
    