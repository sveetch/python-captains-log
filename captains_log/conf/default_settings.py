"""
Default settings used from the script
"""

# Script config dir
CONFIG_DIR = '~/.captains-log'

# Database filepath (relative to APPCONFIG_LOCATION)
DATABASE_NAME = 'database.sqlite3'

# Language code to enable within LC_ALL during script execution
# Let it to empty string to inherit from user locale, use a valid code 
# (like "fr_FR.UTF-8") to force it, use None to disable this feature
LANGUAGE_CODE = ''


ENTRY_ID_TEMPLATE = u"""{0})"""
ENTRY_DATE_TEMPLATE = u"""[{0}]"""
ENTRY_CATEGORY_TEMPLATE = u"""{0}"""
ENTRY_MESSAGE_TEMPLATE = u"""{0}"""


GROUP_MONTH_FORMAT = "%A, %d %B %Y"
ENTRY_DATETIME_FORMAT = "%Y/%m/%d %H:%M"
ENTRY_TIME_FORMAT = "%H:%M"
