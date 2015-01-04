"""
Default settings used from the script

New settings added here will not be automatically effective, you have to 
define it also in ``conf.__init__.merge_settings``
"""

# Script config dir
APPCONFIG_LOCATION = '~/.captains-log'

# Database filepath (relative to APPCONFIG_LOCATION)
DATABASE_LOCATION = 'database.sqlite3'

# Language code to enable within LC_ALL during script execution
# Let it to empty string to inherit from user locale, use a valid code 
# (like "fr_FR.UTF-8") to force it, use None to disable this feature
LANGUAGE_CODE = ''
