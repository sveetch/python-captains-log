# -*- coding: utf-8 -*-
"""
A script to dump some dummy datas

WARNING: Remember to comment Entry model method "save" before using this to 
         avoid 'created' attribute to be automatically filled with datetime.now()
"""
import os, datetime
import click
import peewee
import random, shutil

import arrow

from captains_log.conf.install import install_app
from captains_log.backend.init import init_database
from captains_log.backend.models import CaptainsLogDatabase, Category, Entry

from captains_log.conf import merge_settings

DUMMY_CATEGORIES = [
    u"General",
    u"ACME",
    u"Foo-bar",
    u"Dummy",
    u"Customer1",
    u"Starfleet",
    u"DS9",
    u"Emencia",
    u"R&D",
    u"Customer2",
]

TRIBUNE_TITLES = (
    u'Avengers Mansion', # Marvel Comics
    u'Gotham City', # DC Comics
    u'Morrison Hotel', # Album des Doors
    u'Maysaf', # Assassin's Creed
    u'Cheyenn Mountain', # Stargate
    u'Mines of Moria', # LOTRO
    # Red Dead Redemption
    u'Armadillo',
    u'Chuparosa',
    u'Tumbleweed',
    # Babylon 5
    u'Secteur Gris, niveau 6',
    u'Zahadum',
    # Fallout3
    u'Abri 101',
    u'Rockopolis',
    u'Megaton',
    # GTA
    u'Vice City',
    u'San Andreas',
    u'Liberty City',
    # Papers, Please
    u"La voix de l'Arstotzka",
    # Hercule Poirot
    u'Whitehaven Mansions',
    # Walking dead
    u'Woodbury',
    u'West Georgia Correctional Facility',
    # Zorel
    u'La trouée des Trolls',
    u'Twilight Zone',
    u'Mon curé chez les musselidés',
    u'One mussel on the moon',
    u"Nan c'est à côté",
    u'Here be dragons',
    # Profitroll
    u'Le petit bonhomme en mousse',
    # Fab&lhg
    u'Au royaume des lusers, les geeks sont rois',
    # Eddy
    u'Parle à ma main',
    # Sensei
    u"Place de l'inquisition",
    # Nostromo
    u"On n'est pas à C dans l'air ici",
    # Divers
    u"Tom Petty Fan club",
    u"L'île aux pirates",
    u'Environnement Confiné',
    u'Hôtel Palace',
    u'La Tour de Gay',
    u'1 rue Sésame',
    u'Zone 42',
    u'Dance Floor',
    u'Poire Mécanique',
    u'Tibet Libre',
    u'PaTribune PaLibre',
    u'Hello World',
    u'Hello Kitty Land',
    u'La Tour Sombre',
    u'[:uxam]',
    u'Grrrrrr',
    u'I can haz shiny post too',
    u'Institut de la connaissance universelle',
    u'Please, insert coin',
    u'alt.tribune.dax',
    u'/b/',
    u"Only Classic Rock n' Roll",
    u"Dollarmussels",
)




# Boot settings
settings = merge_settings(**{})
    
# Remove previous config
if os.path.exists(settings['config_dir']):
    shutil.rmtree(settings['config_dir'])

# Then redo install
install_app(settings)

# Connect database again
init_database(settings)
print 

# Create categories
print "Creating Categories"
categories_choices = [None,]
for name in DUMMY_CATEGORIES:
    categories_choices.append(Category.create(name=name))
print




# Create datetime hour ranges for two years
# First year
start = datetime.datetime(2014, 3, 5, 12, 30)
end = datetime.datetime(2014, 7, 10, 13, 30)
datetimes_choices = arrow.Arrow.span_range('hour', start, end)
# Second year
start = datetime.datetime(2014, 12, 10, 10, 5)
end = datetime.datetime(2015, 3, 2, 18, 0)
datetimes_choices = datetimes_choices + arrow.Arrow.span_range('hour', start, end)




# Keep only the start from the ranges
datetimes_choices = [start for start,end in datetimes_choices]

print "Datetimes choices:", len(datetimes_choices)




# Filter datetime to be only between 9h and 19h
def filter_scope_working_hours(item):
    if item.hour < 9 or item.hour > 19:
        return False
    return True
datetimes_choices = filter(filter_scope_working_hours, datetimes_choices)
print "Filtered results:", len(datetimes_choices)



# Selected X random datetime items
ENTRY_ITEMS_MAX = 400
selected_datetimes = []
while len(selected_datetimes)<ENTRY_ITEMS_MAX:
    # Choose a random item
    choosed = random.choice(datetimes_choices)
    # Append it to selected list
    selected_datetimes.append(choosed)
    # Remove item so it can be selected only once
    datetimes_choices.pop(datetimes_choices.index(choosed))



# Re order selected datetimes
selected_datetimes = sorted(selected_datetimes)


def safe_category_name(category):
    if not category:
        return None
    return category.name

# Prepare entry datas for each selected datetimes
bulk_datas = []
for item in selected_datetimes:
    category = random.choice(categories_choices)
    message = random.choice(TRIBUNE_TITLES)
    print item.format('YYYY-MM-DD HH:mm'), safe_category_name(category), message
    print type(item.datetime)
    print
    #entry_obj = Entry.create(created=item.datetime, category=category, content=message)
    bulk_datas.append({
        #'created': item.datetime,
        'created': item.naive, # Use naive datetime, seems at least sqlite does not like TZ
        'category': category,
        'content': message,
    })

# Create this in bulk mode
with CaptainsLogDatabase.transaction():
    for idx in range(0, len(bulk_datas), 1000):
        Entry.insert_many(bulk_datas[idx:idx+1000]).execute()

print "Finished!"