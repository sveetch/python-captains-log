import click

@click.command()
@click.option('--category', '-c', default='global', help='category name')
@click.argument('message', required=True)
@click.pass_context
def add_entry_command(ctx, category, message):
    """
    To add a new log entry
    """
    click.echo('Adding entry for: {0}'.format(category))
    click.echo('    {0}'.format(message))
