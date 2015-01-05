import click, copy, os, json

from captains_log.backend.init import init_database
from captains_log.backend.models import CaptainsLogDatabase, Category, Entry

from captains_log.conf import settings

def install_app():
    """
    Common method to install app's stuff
    """
    if not os.path.exists(settings.CONFIG_DIR):
        click.echo("* Creating the dedicated directory to: {0}".format(settings.CONFIG_DIR))
        os.makedirs(settings.CONFIG_DIR)
    else:
        click.echo("* Fascinating, the dedicated directory allready exists at: {0}".format(settings.CONFIG_DIR))
    
    if not os.path.exists(settings.DATABASE_FILEPATH):
        click.echo("* We need to create the database to: {0}".format(settings.DATABASE_FILEPATH))
        init_database(naive=True)
        CaptainsLogDatabase.create_tables([Category, Entry])
    else:
        click.echo("* It is illogical, the database allready exists at: {0}".format(settings.DATABASE_FILEPATH))

    # Save the config file
    with open(settings.SETTINGS_FILEPATH, 'w') as fp:
        json.dump(settings.as_dict(), fp, indent=4)
    