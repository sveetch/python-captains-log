.. _click: https://github.com/mitsuhiko/click
.. _colorama: https://github.com/tartley/colorama
.. _peewee: https://github.com/coleifer/peewee

Introduction
============

Captain's log is a simple command line utility to quickly write some text about jobs you have done.

It's a simple method for developers (that already have a terminal session opened) to write some stuff about jobs during a day, so they don't have to remember what they have done and so fill their datebook !

Warning, this software should contains some *StarTrek* quotes and vocabulary.

What
****

A simple command line utility to log what you do.

This is not a *todo list* alike, there is no check/uncheck action for entries.

Where
*****

The app install its stuff in the user home directory by default and so should be usable from anywhere.

Users does not share their logs by default although you should be able to do an unique install for multiple users.

Why
***

To help developers to log what they did during working days, so they always have a log resuming projects they worked on and so are more able to fill their activities in datebooks.

Generally, developers always have an opened shell session to work on, so a command line should be enough.

Links
*****

* Download his `PyPi package <http://pypi.python.org/pypi/python-captains-log>`_;
* Clone it on his `Github repository <https://github.com/sveetch/python-captains-log>`_;

Requires
--------

* `click`_ == 3.3;
* `colorama`_ == 0.3.2;
* `peewee`_ == 2.4.5;

Install
=======

Just install it from PyPi : ::

    pip install python-captains-log

Dependancies are quite simple and have not sub-dependancies so it should be safe enough to install it on your system using PIP.

When it's done, the app need a minimal config stuff to be installed before working, like it's database file and config file, see *Usage - Install*.

Usage
=====

Here is the command line help: ::

    Usage: captains-log [OPTIONS] COMMAND [ARGS]...

    Captain's log is a command line to write simple log messages

    Take care to quote your texts when they contains spaces. Also, note that
    some characters like "!" will be processed by Bash as some special
    characters and results in unwanted behaviors, avoid them if you don't know
    how to escape them.

    Options:
    --config-dir PATH  Path to the directory where the app config resides
    --help             Show this message and exit.

    Commands:
    add      Add a new log entry
    del      Remove an existing log entry
    history  Browse your logs history
    install  Install the required config
    reset    Restart with a new install

Install
*******

Before the first usage, each user have to use the following command: ::

    captains-log install

This will automatically install all needed stuff in a dedicated app directory, default is to do it in a ``.captains-log`` directory in the user's home directory.

If you don't do this, the app will notify you about this missing stuff and will refuse to go further.

You can use an another directory for *captain's log* stuff but you will have to specify it, there is two ways for this :

* Using ``--config-dir`` option each time you invoke the command line (this is option is available for all command line actions);
* Set a shell environment variable named ``CAPTAINSLOG_DIR`` that contains the absolute path to the directory like this: ::
    
    export CAPTAINSLOG_DIR=/home/foo/my-captains-log-dir
    
  Or you can do it in your ``.bashrc``.

Note that this app stuff have to be created for each user that want to use it, although you should be able to share it between them if needed.

Reset
*****

Sometime you will need to *reset* your install, so use this : ::

    captains-log reset

This will **remove all your content** (database and config) then re-launch the install process. Take care to backup your config before if you don't want to lose them, the command line doesn't care about this for you.
    
Adding an entry
***************

Add an entry message without a category: ::

    captains-log add Hello

Add an entry message with a category: ::

    captains-log add -c Foo Hello

You have to quote your texts if they contain spaces: ::

    captains-log add -c "Foo bar" "Hello world."

Also, note that your shell can interprets some characters like ``!`` even if quoted, just avoid them if you don't know how to escape them (when it's possible).

When an entry is created, the command line will return its ID than you can't use to remove it if needed.

Removing an entry
*****************

Just use the entry ID you want to remove: ::

    captains-log del 42

Removing the last created entry using the special keyword ``last``: ::

    captains-log del last

Be aware that there is no confirmation prompt before removing the entry.

History
*******

The history *browser* allow you to see your created entries: ::

    captains-log history

This will display your history like this: ::

    Monday, 12 December 2014
    ========================

     97) [10:00]                Wake up
     98) [11:15] MyCategory     Starting to do stuff

    Wednesday 25 December 2014
    ==========================

     99) [10:00]                Coffee time
    100) [11:15] MyCategory     Ping
    101) [17:49] Other category Hello world
    102) [18:33] MyCategory     Pong

    Friday 26 December 2014
    =======================

    103) [09:15] MyCategory     Fix a bug
    104) [10:00]                Coffee time
    105) [15:40] Other category Waiting answer
    106) [17:45] MyCategory     Go to production

Actually, the default behavior is to display all your entries from any date period. But the command line action accepts an optional argument to give a keyword about the period you want to see: ::

    # Entries of the current year
    captains-log history year
    
    # Entries of the current month
    captains-log history month
    
    # Entries of the current day
    captains-log history day
    
    # Entries that contains "Coffee"
    captains-log history -s "Coffee"

The history is columnized and even have colorized parts if your shell and terminal console support them. Also you can change some formatting from your settings file if needed like changing the date format, see the *Setting* part.

Settings
********

In your installed Captain's log directory from the ``install`` action, there is a ``settings.json`` file where you can change some settings that can change some behaviors.

::

    {
        "ENTRY_TIME_FORMAT": "%H:%M", 
        "LANGUAGE_CODE": "", 
        "DATABASE_NAME": "database.sqlite3", 
        "ENTRY_DATE_TEMPLATE": "[{0}]", 
        "ENTRY_ID_TEMPLATE": "{0})", 
        "ENTRY_CATEGORY_TEMPLATE": "{0}", 
        "GROUP_MONTH_FORMAT": "%A, %d %B %Y", 
        "ENTRY_MESSAGE_TEMPLATE": "{0}"
    }

Where :

* ``ENTRY_TIME_FORMAT`` is the time format to use when displaying an entry time;
* ``LANGUAGE_CODE`` is a locale code that is supported on your system like "fr_FR.UTF-8", let it to an empty string to automatically use your system locale;
* ``DATABASE_NAME`` is the filename for the sqlite3 database file installed in the Captain's log directory;
* ``ENTRY_ID_TEMPLATE`` is the template string to format the entry's ID;
* ``ENTRY_CATEGORY_TEMPLATE`` is the template string to format the entry's category name;
* ``ENTRY_DATE_TEMPLATE`` is the template string to format the entry's day datetime (it's string display, not the date format itself);
* ``ENTRY_MESSAGE_TEMPLATE`` is the template string to format the entry's message;
* ``GROUP_MONTH_FORMAT`` is the datetime format to use when displaying a day date (the title for each day group);
