"""
Initialize database for peewee connector
"""
import click, os
from captains_log.backend.models import CaptainsLogDatabase

from captains_log.conf import settings

def init_database(naive=False):
    """
    Given the user settings, initialize the database
    
    Raise a click exception UsageError if the database filepath does not exists in settings
    
    ``naive`` argument is used to say if the method should validate that database file exists.
    """
    # Validate than database filepath exists
    if not naive and not os.path.exists(settings.DATABASE_FILEPATH):
        raise click.UsageError(
            "\n\n".join([
                "Unable to find the database, from: {0}".format(settings.DATABASE_FILEPATH),
                "If this is your first \"Captain's log\" usage you must use the 'install' command before."
            ])
        )
    
    # Gives database access/config to peewee
    CaptainsLogDatabase.init(settings.DATABASE_FILEPATH)
        
    return CaptainsLogDatabase