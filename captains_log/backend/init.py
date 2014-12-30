"""
Initialize database for peewee connector
"""
import click, os
from captains_log.backend.models import CaptainsLogDatabase

def init_database(settings, naive=False):
    """
    Given the user settings, initialize the database
    
    Raise a click exception UsageError if the database filepath does not exists in settings
    
    ``naive`` argument is used to say if the method should validate that database file exists.
    """
    # Validate than database filepath exists
    if not naive and not os.path.exists(settings['database_filepath']):
        raise click.UsageError("Unable to find the database, if this is your first \"Captain's log\" usage you must use the 'install' command before")
    
    # Gives database access/config to peewee
    CaptainsLogDatabase.init(settings['database_filepath'])
        
    return CaptainsLogDatabase