import click

from captains_log.cli.add_entry import add_entry_command
from captains_log.cli.remove_entry import remove_entry_command
from captains_log.cli.entries_history import entries_history_command

@click.group()
@click.pass_context
def cli_frontend(ctx):
    """
    Main command grouper to expose all commands
    """
    ctx.obj = {
        'debug': "yes indeed",
    }


cli_frontend.add_command(add_entry_command, name="add")
cli_frontend.add_command(remove_entry_command, name="del")
cli_frontend.add_command(entries_history_command, name="history")

if __name__ == '__main__':
    print "FOOOOOOOOOOOOOOOOOO"
    cli_frontend(obj={})
