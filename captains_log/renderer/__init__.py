# -*- coding: utf-8 -*-
"""
Commn renderers stuff
"""
import click

from captains_log.backend.models import Category, Entry


class GroupTitle(object):
    """
    A simple object to distinct titles from list results in group 
    sections
    
    So it's just a simple object to embed a title string
    """
    def __init__(self, title):
        self.title = title
    
    def __unicode__(self):
        return self.title
    
    def __str__(self):
        return self.title



class ColoredOutputMixin(object):
    """
    A mixin to use with a Renderer object, has to be the most left inherit
    
    Use click's "style" method to easily use colorama for output
    """
    def format_created(self, value):
        return click.style(
            super(ColoredOutputMixin, self).format_created(value),
            fg='green'
        )
        
    def format_category(self, value):
        if value:
            return click.style(
                super(ColoredOutputMixin, self).format_category(value),
                fg='magenta'
            )
        return ""



class BaseRenderer(object):
    """
    Basic rendered, the render method does not return a string, but the 
    processed results with their formatted values
    """
    entry_id_template = u"""{0}"""
    entry_date_template = u"""[{0}]"""
    entry_category_template = u"""{0}"""
    entry_message_template = u"""{0}"""
    entry_datetime_format = "%Y/%m/%d %H:%M"
    entry_time_format = "%H:%M"

    def __init__(self, queryset):
        self.queryset = queryset
        
    def format_id(self, value):
        """Format Entry id"""
        return self.entry_id_template.format(value)
        
    def format_created(self, value):
        """Format Entry created datetime"""
        created = value.strftime(self.entry_datetime_format)
        return self.entry_date_template.format(created)
        
    def format_category(self, value):
        """Format Entry category object"""
        if value:
            return self.entry_category_template.format(value)
        
        return ""
        
    def format_message(self, value):
        """Format Entry message"""
        return self.entry_message_template.format(value)
        
    def assemble_columns(self, entry):
        """Assemble formatted Entry value as columns"""
        return [
            self.format_id(entry.id),
            self.format_created(entry.created),
            self.format_category(entry.category_name()),
            self.format_message(entry.content)
        ]
        
    def build_row(self, entry):
        """
        Build an Entry row
        
        Just joining values with a space and return a string
        """
        return " ".join(self.assemble_columns(entry))
        
    def pre_process(self):
        """
        Pre processing results and return them as a list
        """
        entries = list(self.queryset)
        
        return entries
    
    def render(self):
        """
        Render the whole results
        """
        results = self.pre_process()
        
        self.starting_entry = results[0].created
        self.ending_entry = results[-1].created
        
        self.not_the_same_day_mode = (self.starting_entry != self.ending_entry)
        
        return results



class GrouperRenderer(BaseRenderer):
    """
    Like the BaseRenderer but contains additional stuff to implement results grouping
    
    Principes is to regroup results by some condition (like the datetime) into 
    sections then return a list of section list that final renderer can reformat 
    to suit to their needs.
    """
    group_month_format = "%A, %d %B %Y"
        
    #def format_created(self, value):
        #"""Format Entry created datetime"""
        #created = value.strftime(self.entry_time_format)
        #return self.entry_date_template.format(created)
    
    def regroup(self, entries):
        """
        Regroup datas
        # - Execute the query so we can pre-process results before starting to render it;
        # - Divide results in days (should be easy to cut because results are date ordere);
        # - Regroup by days or month ?
        # - Put a title for each group
        """
        sections = []
        if self.not_the_same_day_mode:
            i = 0
            current_day = None
            current_group = None
            for item in entries:
                # Reset counter if we are in another day than saved current date
                if current_day and item.created.date() != current_day:
                    i = 0
                
                # Open a new section with the title and its entries
                if i == 0:
                    # Push the previous waiting entries group as a section
                    current_day = item.created.date()
                    if current_group is not None:
                        sections.append(current_group)
                    # Open new group with its title
                    current_group = []
                    sections.append(GroupTitle(item.created.strftime(self.group_month_format)))
                # Store item in the current group
                current_group.append(item)
                i += 1
                    
            # Push remaining last group as a section
            if current_group:
                sections.append(current_group)
                
            return sections
        
        return [GroupTitle(self.starting_entry.strftime(self.group_month_format)), entries]
        
    def render_title(self, title):
        """
        Render a title section
        """
        title = unicode(title)
        return "\n".join(["="*len(title), title, "="*len(title)])
        
    def render_results(self, results):
        """
        Render results section
        """
        return [self.build_row(entry) for entry in results]
    
    def render(self):
        """
        Render the whole results
        """
        results = super(GrouperRenderer, self).render()
        elements = self.regroup(results)
        
        sections = []
        for group in elements:
            if isinstance(group, GroupTitle):
                sections.append(self.render_title(group))
            else:
                sections.append(self.render_results(group))
                # Little trick to add a line separation between a group and the following title
                sections.append("")
                
        return sections
