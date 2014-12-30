import os
import click
import peewee

## Uncomment this to see executed SQL queries
#import logging
#logging.basicConfig(
    #format='[%(asctime)-15s] [%(name)s] %(levelname)s]: %(message)s',
    #level=logging.DEBUG
#)

from captains_log.cli.add_entry import add_entry_command
from captains_log.cli.remove_entry import remove_entry_command
from captains_log.cli.entries_history import entries_history_command
from captains_log.cli.installer import install_command, reset_command

from captains_log.conf import merge_settings

@click.group()
#@click.argument('location', default=DEFAULT_DIR_LOCATION, required=True)
#@click.option('--database', '-d', default='captains-log.sqlite3', help='Path to the sqlite3 database to use')
@click.pass_context
def cli_frontend(ctx):#, database):
    """
    Captain's log is a command line to write simple log messages
    
    Take care to quote your texts when they contains spaces. Also, note that some characters like "!" will be processed by Bash as some special characters and results to unwanted behaviors, avoid them if you don't know how to escape them.
    """
    # Init the default context that will be passed to commands
    ctx.obj = {
        'settings': merge_settings(**{}),
    }


# Attach commands methods to the main grouper
cli_frontend.add_command(add_entry_command, name="add")
cli_frontend.add_command(remove_entry_command, name="del")
cli_frontend.add_command(entries_history_command, name="history")
cli_frontend.add_command(install_command, name="install")
cli_frontend.add_command(reset_command, name="reset")
