# -*- coding: utf-8 -*-
import click, peewee

from captains_log.backend.init import init_database
from captains_log.backend.models import Entry

def validate_entry_id(ctx, param, value):
    """
    Validate that entry ID is either a integer or a string for a valid 
    keyword (currently only 'last')
    
    Return either an integer or a string. Raise a click exception if value 
    is not an integer or a valid keyword.
    """
    try:
        value = int(value)
        return value
    except ValueError:
        if value != 'last':
            raise click.BadParameter('value must be a valid integer or at least the keyword "last" (that means the last entry)')
        else:
            return value

@click.command(short_help='Remove an existing log entry')
@click.argument('entry_id', callback=validate_entry_id, required=True)
@click.pass_context
def remove_entry_command(ctx, entry_id):
    """
    Remove an existing log entry
    
    Either from its given ID or the last entry in date if given ID is a string equal to "last"
    """
    init_database(ctx.obj['settings'])
    
    click.echo('Remove entry id: {0}'.format(entry_id))
    if isinstance(entry_id, basestring):
        raise click.UsageError("'last' keyword usage is not implemented yet")
    elif isinstance(entry_id, int):
        try:
            entry_obj = Entry.get(Entry.id == entry_id)
        except Entry.DoesNotExist:
            raise click.UsageError("Entry with given ID does not exists: {0}".format(entry_id))
        else:
            entry_obj.delete_instance()
            click.echo("Entry has been removed")
