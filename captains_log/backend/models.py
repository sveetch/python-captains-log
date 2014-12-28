"""
Data models with peewee
"""
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


class Entry(BaseModel):
    """
    Log entry
    """
    created = DateTimeField(index=True, null=False)
    category = ForeignKeyField(Category, related_name='entries', null=True)
    content = TextField()
