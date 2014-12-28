import click

@click.command()
@click.pass_context
def entries_history_command(ctx):
    """
    To display log entries
    """
    click.echo('History')
