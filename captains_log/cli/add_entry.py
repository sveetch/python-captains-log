import click

from captains_log.backend.init import init_database

@click.command()
@click.option('--category', '-c', default=None, help='Category name')
@click.argument('message', default='')
@click.pass_context
def add_entry_command(ctx, category, message):
    """
    To add a new log entry
    """
    init_database(ctx.obj['settings'])
    
    # Validate that both category and message are not empty
    if not category and not message:
        raise click.UsageError("Sorry captain, you can't create a log with both empty category and message.")
    
    click.echo('Adding entry for: {0}'.format(category))
    click.echo('    {0}'.format(message))
