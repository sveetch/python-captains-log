import click, copy, json, os
import warnings
from captains_log.conf import default_settings

ENVIRONMENT_CFG_DIR_VARIABLE = "CAPTAINSLOG_DIR"
ENVIRONMENT_CFG_FILENAME_VARIABLE = "CAPTAINSLOG_SETTINGS"

DEFAULT_CONFIG_DIR = '~/.captains-log'
DEFAULT_SETTINGS_FILENAME = "settings.json"

def validate_identifier(seq):
    if not seq:
        return False
    if seq[0].isdigit():
        return False
    # get an iterator
    itr = iter(seq)
    # pull remaining characters and yield legal ones for identifier
    for ch in itr:
        if ch != '_' and not ch.isalpha() and not ch.isdigit():
            return False
    return True

class SettingsLoader(object):
    """
    Settings loader and "interface"
    
    Load the settings from the default ones then if possible merge in the 
    user ones in its config dir
    
    This is somewhat a lazy loading because the load is done only the first time an 
    attribute is getted.
    
    This is not where the settings is effectively stored, see SettingsStore 
    instead, but it contains some method to interact with settings :
    
    * To change a setting, use the method ``set_setting(name, value)``;
    * To merge settings from a dict, use the method ``merge_settings(dict)``;
    * You can directly acceed to SettingsStore settings attributes;
    
    User can set some environment variables to changes behaviors :
    
    * ``CAPTAINSLOG_DIR`` to define a path to the app directory that contains the settings file and the database file;
    * ``CAPTAINSLOG_SETTINGS`` to define a filename for the settings file;
    
    """
    def __init__(self):
        self._wrapped = None
    
    def _setup(self):
        """
        Load the settings module pointed to by the environment variable. This
        is used the first time we need any settings at all, if the user has not
        previously configured the settings manually.
        """
        self._defaults = default_settings
        
        try:
            config_dir = os.environ[ENVIRONMENT_CFG_DIR_VARIABLE]
            if not config_dir: # If it's set but is an empty string.
                raise KeyError
        except KeyError:
            config_dir = DEFAULT_CONFIG_DIR
    
        # Expand user home dir prefix to an absolute path
        if config_dir.startswith('~'):
            config_dir = os.path.expanduser(config_dir)
        
        try:
            settings_filename = os.environ[ENVIRONMENT_CFG_FILENAME_VARIABLE]
            if not config_dir: # If it's set but is an empty string.
                raise KeyError
        except KeyError:
            settings_filename = DEFAULT_SETTINGS_FILENAME
        
        self._wrapped = SettingsStore(config_dir, settings_filename)

    def __getattr__(self, name):
        """
        To get a value for a SettingsStore settings attribute
        """
        if self._wrapped is None:
            self._setup()
        return getattr(self._wrapped, name)

    def set_setting(self, name, value):
        """
        To set a value for a SettingsStore settings attribute
        """
        if self._wrapped is None:
            self._setup()
        setattr(self._wrapped, name, value)

    def merge_settings(self, kwargs):
        """
        To merge a dict into SettingsStore settings attribute
        """
        if self._wrapped is None:
            self._setup()
        self._wrapped.merge(kwargs)


class SettingsStore(object):
    """
    Settings store where the settings value are stored
    """
    automatic_settings = ['DATABASE_FILEPATH']
    override_excludes = ['CONFIG_DIR', 'SETTINGS_FILENAME', 'SETTINGS_FILEPATH', 'DATABASE_FILEPATH']
    
    def __init__(self, config_dir, settings_filename):
        settings_filepath = os.path.join(config_dir, settings_filename)
        
        # update this dict from global settings (but only for ALL_CAPS settings)
        for setting in dir(default_settings):
            if setting == setting.upper():
                setattr(self, setting, getattr(default_settings, setting))

        # Store some internal settings that are not overridable
        self.CONFIG_DIR = config_dir
        self.SETTINGS_FILENAME = settings_filename
        self.SETTINGS_FILEPATH = settings_filepath
        # Automatic calculated settings
        self._make_automatic_settings()
        
        # Try to open user settings file to overrides the default settings
        try:
            with open(self.SETTINGS_FILEPATH, 'r') as fp:
                settings_overrides = json.load(fp)
        except IOError as e:
            click.echo(click.style(
                "\n\n".join([
                    "Could not import settings '{0}': {1}".format(self.SETTINGS_FILEPATH, e),
                    "Default settings will be used instead, you should resolve this problem to avoid this message."
                ]),
                fg='yellow'
            ))
        except ValueError as e:
            click.echo(click.style(
                "\n\n".join([
                    "Could not import settings '{0}': {1}".format(self.SETTINGS_FILEPATH, e),
                    "Default settings will be used instead, you should resolve this problem to avoid this message."
                ]),
                fg='yellow'
            ))
        else:
            # Overriding default settings
            self.merge(settings_overrides)
            
    def _make_automatic_settings(self):
        """
        Build automatic settings
        """
        super(SettingsStore, self).__setattr__('DATABASE_FILEPATH', os.path.join(self.CONFIG_DIR, self.DATABASE_NAME))

    def __setattr__(self, name, value):
        super(SettingsStore, self).__setattr__(name, value)
        # Rebuild automatic calculated settings
        if name in self.automatic_settings:
            self._make_automatic_settings()
            
    def merge(self, kwargs):
        """
        Overriding settings from a dict
        """
        for name, value in kwargs.items():
            # 1) Validate variable name (JSON any key if quoted as a string)
            # 2) Enforce to use only uppercase names, other are ignored
            if name not in self.override_excludes and validate_identifier(name) and name == name.upper():
                setattr(self, name, value)
        # Rebuild automatic calculated settings
        self._make_automatic_settings()

    
    def exportable_names(self):
        """
        Return a list of Setting attribute names that can be 
        exported/overrided as a setting
        """
        names = []
        for setting in dir(self):
            if setting == setting.upper() and setting not in self.override_excludes:
                names.append(setting)
        #return sorted(names)
        return names
    
    def as_dict(self):
        """
        Return a dict of settings that can be used in a user settings file
        """
        output = {}
        for name in self.exportable_names():
            output[name] = getattr(self, name)
        
        return output
    
    def as_json(self):
        """
        Return a JSON dict of settings that can be used in a user settings file
        """
        return json.dumps(self.as_dict(), indent=4)


settings = SettingsLoader()