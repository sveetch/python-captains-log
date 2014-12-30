import click, peewee

from captains_log.backend.init import init_database
from captains_log.backend.models import CaptainsLogDatabase, Category, Entry
from captains_log.renderer.history import BasicHistoryRenderer, TabulatedHistoryRenderer


@click.command()
#@click.option('--year', '-y', default=None, type=int, help='Year filter (ex:2014)')
#@click.option('--month', '-m', default=None, type=int, help='Month filter (ex:12)')
#@click.option('--day', '-d', default=None, type=int, help='Day filter (ex:25)')
@click.pass_context
def entries_history_command(ctx):#, year, month, day):
    """
    To display log entries
    """
    init_database(ctx.obj['settings'])
    
    title = 'History'
    title = "\n".join(["="*len(title), title, "="*len(title)])
    click.echo(title)
    
    queryset = Entry.select(Entry, Category).join(Category, peewee.JOIN_LEFT_OUTER).order_by(Entry.created.asc()).aggregate_rows()
    
    #click.echo(BasicHistoryRenderer(queryset).render())
    
    click.echo(TabulatedHistoryRenderer(queryset).render())
        