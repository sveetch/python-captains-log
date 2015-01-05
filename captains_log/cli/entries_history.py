# -*- coding: utf-8 -*-
import click, datetime, peewee

from captains_log.backend.init import init_database
from captains_log.backend.models import CaptainsLogDatabase, Category, Entry
from captains_log.renderer.history import SimpleHistoryRenderer, TabulatedHistoryRenderer, ColumnedHistoryRenderer

@click.command(short_help='Browse your logs history')
@click.argument('period', type=click.Choice(['all', 'year', 'month', 'day']), default="all", required=True, metavar='<period>')
@click.option('--search_pattern', '-s', default=None, help='Pattern to search for entries than contain it')
@click.pass_context
def entries_history_command(ctx, period, search_pattern=None):
    """
    Browse your logs history for the optionnal <period> keyword given.
    
    If given, <period> must be a valid choice, where 'year' will limit results 
    to the current year, "month" to the current month and "day" the current day.
    """
    init_database()
    
    # Start queryset defining JOIN on entry and category
    queryset = Entry.select(Entry, Category).join(Category, peewee.JOIN_LEFT_OUTER)
    
    empty_message = "There is no entries for.."
    
    if period != 'all':
        now = datetime.datetime.now()
        
        if period == 'year':
            queryset = queryset.where(Entry.created.year == now.year)
            empty_message = "There is no entries for the current year"
        elif period == 'month':
            queryset = queryset.where(
                (Entry.created.year == now.year) & 
                (Entry.created.month == now.month)
            )
            empty_message = "There is no entries for the current month"
        elif period == 'day':
            queryset = queryset.where(
                (Entry.created.year == now.year) & 
                (Entry.created.month == now.month) & 
                (Entry.created.day == now.day)
            )
            empty_message = "There is no entries for the current day"
        # TODO: use calendar to find the week start and end days so we can 
        #       limit results to the current week
    
    # Use a pattern to seach for entries that contains it
    if search_pattern:
        queryset = queryset.where(Entry.content.contains(search_pattern))
    
    # Finish with adding order and aggregating
    queryset = queryset.order_by(Entry.created.asc()).aggregate_rows()
    
    if queryset.count() > 0:
        ## Simple history columns are just joined with a space, no tabulated layout
        #click.echo(SimpleHistoryRenderer(queryset).render())
        
        ## History tabulated with "tabulate" package, should be deprecated
        #click.echo(TabulatedHistoryRenderer(queryset).render())
        
        ## History correctly tabulated
        click.echo(ColumnedHistoryRenderer(queryset).render())
    else:
        click.echo(empty_message)
    # TODO: add an option to print message about finded results ?
    #print "Period keyword:", period
    #print "Results:", len(list(queryset))
        