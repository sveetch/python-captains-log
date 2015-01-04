# -*- coding: utf-8 -*-
"""
Renderers for Entry history browsing
"""
import click

from captains_log.backend.models import Category, Entry
from captains_log.renderer import GroupTitle, ColoredOutputMixin, BaseRenderer, GrouperRenderer


class SimpleHistoryRenderer(ColoredOutputMixin, GrouperRenderer):
    """
    Simple rendered than simply join entry columns with a space
    """
    def render_results(self, results):
        """
        Render results section
        """
        return "\n".join([self.build_row(entry) for entry in results])
    
    def render(self):
        """
        Render the whole results
        """
        sections = super(SimpleHistoryRenderer, self).render()
        
        return "\n".join(sections)
    


try:
    from tabulate import tabulate
except ImportError:
    class TabulatedHistoryRenderer(GrouperRenderer):
        # TODO: raise a warning from __init__ to warn if using and tabulate is not installed
        #       Also put a flag to know that this is a dummy renderer
        pass
else:
    class TabulatedHistoryRenderer(ColoredOutputMixin, GrouperRenderer):
        """
        Renderer that use ``tabulate`` app to render results in data 
        tables (with aligned and padded columns values)
        """
        def build_row(self, entry):
            """
            Simply return the values list untouched
            """
            return self.assemble_columns(entry)

        def render_results(self, results):
            """
            Render results section
            """
            return tabulate([self.build_row(entry) for entry in results], tablefmt="plain")+"\n"
        
        def render(self):
            """
            Render the whole results
            """
            sections = super(TabulatedHistoryRenderer, self).render()
            
            return "\n".join(sections)


class ColumnedHistoryRenderer(ColoredOutputMixin, GrouperRenderer):
    """
    Try to implement a better tabulated render than the one with 'tabulate' 
    app that can't manage a title on a whole line
    
    In fact we are just padding id and category name, date does not change 
    with the default date format and we don't care about message because 
    it's the last column
    """
    def post_regroup_process(self, sections):
        """
        Find the most largest category name used from all entries
        """
        self.largest_category_name = max([k for k in self.categories if k], key=len)
        # Calculate the most largest ID representation when formatted using the 
        # last entry (that should allways have the higher id)
        self.largest_entry_id = len(super(ColumnedHistoryRenderer, self).format_id(self.ending_entry.id))
        
        return sections
    
    def post_ungrouped_process(self, sections):
        """
        Within ``ColumnedHistoryRenderer`` this is just a mirror to 
        ``post_regroup_process`` because the only thing it do is to find the 
        most largest category name
        """
        return self.post_regroup_process(sections)
    
    def format_id(self, value):
        return super(ColumnedHistoryRenderer, self).format_id(value).ljust(self.largest_entry_id)
    
    def format_category(self, value):
        if value is None:
            value = ""
        
        value = value.ljust(len(self.largest_category_name))
        if value:
            value = click.style(
                super(ColoredOutputMixin, self).format_category(value),
                fg='magenta'
            )
            
        return value
    
    def render_results(self, results):
        """
        Render results section
        """
        return ("\n".join([self.build_row(entry) for entry in results]))+"\n"
    
    def render(self):
        """
        Render the whole results
        """
        sections = super(ColumnedHistoryRenderer, self).render()
        
        return "\n".join(sections)

