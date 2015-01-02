.. _Django: https://www.djangoproject.com/

Introduction
============

Captain's log is a simple command line utility to fastly write some text about jobs you have done.

It's a simple method for developers (that allready have a terminal session opened) to write some stuff about jobs during a day, so they don't have to remember what they have done and so fill their datebook !

Warning, this software should contains some *StarTrek* quotes and vocabulary.

TODO
====

* Finish history renderer;
* Implement history filters;
* Implement a config file to change some behaviors and options;
* Finish the README;

Proposal
========

*(This is the draft that leaded to development, the final production should diverge a little bit)*

What
----

A simple command line utility to add log for what you do.

This is not a *todo list* alike, there is no check/uncheck action for entries.

Where
-----

Should be available from anywhere. So it must share its log from a location in the user home directory, something like : ::

    $HOME/.captains-backlog/foo.log

Why
---

To help developers to log what they did during working days, so they allways have a log resuming projects they afforded and so are much able to fill their activities in datebooks.

Generally, developers allways have an opened shell session to work, so a command line should be enough.

How
---

Adding entry
************

This have to be really fast and easy to use, so at least we should have something like: ::

    captains-log add -c parrot "Did something"
    captains-log add -c setic start
    captains-log add "writing some ideas"
    captains-log add -c setic stop
    captains-log add -c parrot "go to prod"
    captains-log add -c parrot stop
    
The first line open a log for the ``parrot`` category with the message ``Did something``. 

**captains-log** will write it to a log file or/and a sqlite3 backend in a shared directory (in the user's home) so we can use it from anywhere in the user's space.

**Command line details :** ``captains-log add [-c category] message``

The command should return the entry ID just after it have saved it.

Removing entry
**************

We need also a way to remove some entries if needed.

Removing an entry from an ID : ::

    captains-log del 1
    captains-log del 001

The two way should to write digit or not should works.

Removing the last writed entry: ::

    captains-log del last

**Command line details :** ``captains-log remove [ID or 'last' value]``

History
*******

Also we need an history view to be able to see history at anytime without to go to look in the logs, so something like that: ::

    captains-log log

Think about to limit the history at last to the current month, to avoid thousand of entries. Then so there should be an argument to view other months.

That should display something like that: ::

    001 - [26-12-2014 10:02] (parrot) Did something
    002 - [26-12-2014 10:58] (setic) 
    003 - [26-12-2014 11:09] writing some ideas
    004 - [26-12-2014 11:25] (setic) 
    005 - [26-12-2014 11:47] (parrot) go to prod
    006 - [26-12-2014 12:10] (parrot)

This should use colorized text output for better visibility between date, name and message. The common format should be : ::

    ID - [ENTRY DATE] (category) message

* ``ID`` is a numeric id padded on X digits where X is calculated from the total of messages to display;
* ``[ENTRY DATE]`` is automatic;
* ``category`` is optionnal, if not given it will go to *global*;
* ``message`` should not be optional;

Then it could be nice to have an history view with entries group by days like : ::

    Mercredi 25 Décembre 2014
    =========================

    * [10:00] parrot: start
    * [11:15] go to bureau
    * [17:49] back
    * [18:33] parrot: stop

    Vendredi 26 Décembre 2014
    =========================

    * [10:02] parrot: Did something
    * [10:58] setic: start
    * [11:09] writing some ideas
    * [11:25] setic: stop
    * [11:47] parrot: go to prod
    * [12:10] parrot: stop

**Command line details :** ``captains-log history``

(Filtering option arguments have to be studied)

Aliases
*******

Write something in README about a good idea to create a bash alias to ``captains-log`` for a more shorter command to type.

