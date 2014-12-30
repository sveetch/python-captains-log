# -*- coding: utf-8 -*-
import click, peewee
from colorama import Fore, Back, Style

from captains_log.backend.models import Category, Entry

class BasicHistoryRenderer(object):
    entry_id_template = u"""{0}"""
    entry_date_template = u"""[{0}]"""
    entry_category_template = u"""{0}"""
    entry_message_template = u"""{0}"""
    entry_datetime_format = "%Y/%m/%d %H:%M"
    entry_time_format = "%H:%M"

    def __init__(self, queryset):
        self.queryset = queryset
        
    def format_id(self, value):
        return self.entry_id_template.format(value)
        
    def format_created(self, value):
        created = value.strftime(self.entry_datetime_format)
        return click.style(
            self.entry_date_template.format(created),
            fg='green'
        )
        
    def format_category(self, value):
        if value:
            #return self.entry_category_template.format(value)
            return click.style(
                self.entry_category_template.format(value),
                fg='magenta'
            )
        
        return ""
        
    def format_message(self, value):
        return self.entry_message_template.format(value)
        
    def assemble_columns(self, entry):
        return [
            self.format_id(entry.id),
            self.format_created(entry.created),
            self.format_category(entry.category_name()),
            self.format_message(entry.content)
        ]
        
    def build_row(self, entry):
        return " ".join(self.assemble_columns(entry))
        
    def render(self):
        return "\n".join([self.build_row(entry) for entry in self.queryset])



try:
    from tabulate import tabulate
except ImportError:
    class TabulatedHistoryRenderer(BasicHistoryRenderer):
        # TODO: raise a warning from __init__
        pass
else:
    class TabulatedHistoryRenderer(BasicHistoryRenderer):
        def build_row(self, entry):
            return self.assemble_columns(entry)
        
        def render(self):
            return tabulate([self.build_row(entry) for entry in self.queryset], tablefmt="plain")

