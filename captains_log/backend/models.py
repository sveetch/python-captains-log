"""
Data models with peewee
"""
import datetime

from peewee import SqliteDatabase, Model, DateTimeField, CharField, ForeignKeyField, TextField

# Lazy database connector
CaptainsLogDatabase = SqliteDatabase(None)

class BaseModel(Model):
    """
    Base model to share the same database connector
    """
    class Meta:
        database = CaptainsLogDatabase


class Category(BaseModel):
    """
    Category
    """
    created = DateTimeField(null=False)
    name = CharField(max_length=60, unique=True, null=False)
    
    def save(self, *args, **kwargs):
        self.created = datetime.datetime.now()
        return super(Category, self).save(*args, **kwargs)


class Entry(BaseModel):
    """
    Log entry
    """
    created = DateTimeField(index=True, null=False)
    category = ForeignKeyField(Category, related_name='entries', null=True)
    content = TextField()
    
    def category_name(self):
        if self.category is not None and self.category.id is not None:
            return self.category.name
        return None
    
    def save(self, *args, **kwargs):
        self.created = datetime.datetime.now()
        return super(Entry, self).save(*args, **kwargs)
