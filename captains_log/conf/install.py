import os, click

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
