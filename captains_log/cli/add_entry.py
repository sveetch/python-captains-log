# -*- coding: utf-8 -*-
import click, peewee

from captains_log.backend.init import init_database
from captains_log.backend.models import CaptainsLogDatabase, Category, Entry


def get_category_or_create(db, name):
    """
    Return a category for given name, create it if not exists, using 
    constraint checking
    """
    try:
        with db.transaction():
            return Category.create(name=name)
    except peewee.IntegrityError:
        return Category.get(Category.name == name)


@click.command()
@click.option('--category', '-c', default=None, help='Category name')
@click.argument('message', default='')
@click.pass_context
def add_entry_command(ctx, category, message):
    """
    Add a new log entry
    """
    init_database(ctx.obj['settings'])
    
    # Validate that both category and message are not empty
    if not category and not message:
        raise click.UsageError("Sorry captain, you cannot create a log with both empty category and message.")
    
    # Get or create category
    category_obj = category
    if category:
        category_obj = get_category_or_create(CaptainsLogDatabase, category)
    
    # Create entry
    entry_obj = Entry.create(category=category_obj, content=message)

    click.echo('Added new entry with ID: {0}'.format(entry_obj.id))
