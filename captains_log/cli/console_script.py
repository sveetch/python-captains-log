# -*- coding: utf-8 -*-
import os
import click
import peewee
import locale

## Uncomment this to see executed SQL queries
#import logging
#logging.basicConfig(
    #format='[%(asctime)-15s] [%(name)s] %(levelname)s]: %(message)s',
    #level=logging.DEBUG
#)

from captains_log.conf import settings

@click.group()
#@click.argument('location', default=DEFAULT_DIR_LOCATION, required=True)
@click.option('--config-dir', default=None, metavar='PATH', help='Path to the directory where the app config resides')
#@click.option('--database', '-d', default='captains-log.sqlite3', help='Path to the sqlite3 database to use')
@click.pass_context
def cli_frontend(ctx, config_dir):#, database):
    """
    Captain's log is a command line to write simple log messages
    
    Take care to quote your texts when they contains spaces. Also, note that some characters like "!" will be processed by Bash as some special characters and results to unwanted behaviors, avoid them if you don't know how to escape them.
    """
    # Init the default context that will be passed to commands
    # Not really used since settings is imported from its module
    ctx.obj = {}
    
    # Override config directory from given option if any
    if config_dir:
        settings.set_setting('CONFIG_DIR', config_dir)
    
    # Active system locale so we have dates in the right user language
    if settings.LANGUAGE_CODE is not None:
        lang_code = settings.LANGUAGE_CODE
        # LANGUAGE_CODE can be an empty string that means 
        # "get the user system locale" but it a real code is defined we have 
        # to parse into a tuple
        if lang_code:
            # On most recent system, language code is composed of "code.encoding"
            lang_code = settings.LANGUAGE_CODE.split('.')
            if len(lang_code)<2:
                lang_code.append("")
        try:
            locale.setlocale(locale.LC_ALL, lang_code)
        except Exception as e:
            click.echo(click.style(
                "\n\n".join([
                    "Unvalid locale code '{0}': {1}".format(settings.LANGUAGE_CODE, e),
                    "Default settings will be used instead, you should resolve this problem to avoid this message."
                ]),
                fg='yellow'
            ))



from captains_log.cli.add_entry import add_entry_command
from captains_log.cli.remove_entry import remove_entry_command
from captains_log.cli.entries_history import entries_history_command
from captains_log.cli.installer import install_command, reset_command
from captains_log.cli.devdebug import foo_command

# Attach commands methods to the main grouper
cli_frontend.add_command(add_entry_command, name="add")
cli_frontend.add_command(remove_entry_command, name="del")
cli_frontend.add_command(entries_history_command, name="history")
cli_frontend.add_command(install_command, name="install")
cli_frontend.add_command(reset_command, name="reset")
#cli_frontend.add_command(foo_command, name="foo")
# TODO: a "settings" command to see effectives settings used
