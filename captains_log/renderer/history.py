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
            print "render_results:", len(results)
            return tabulate([self.build_row(entry) for entry in results], tablefmt="plain")
        
        def render(self):
            """
            Render the whole results
            """
            sections = super(TabulatedHistoryRenderer, self).render()
            
            return "\n".join(sections)
