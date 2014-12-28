import click

def validate_entry_id(ctx, param, value):
    try:
        foo = int(value)
        return foo
    except ValueError:
        if value != 'last':
            raise click.BadParameter('value must be a valid integer or at least the keyword "last" (that means the last entry)')
        else:
            return value

@click.command()
@click.argument('entry_id', callback=validate_entry_id, required=True)
@click.pass_context
def remove_entry_command(ctx, entry_id):
    """
    To remove an existing log entry from its given ID or the last entry in date if given ID is a string equal to "last"
    """
    click.echo('Remove entry id: {0}'.format(entry_id))
