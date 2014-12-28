import os
from captains_log.conf import defaults

def merge_settings(**kwargs):
    """
    Merge default app settings with optional user defined options
    """
    d = {
        'config_dir': defaults.APPCONFIG_LOCATION,
        'database_name': defaults.DATABASE_LOCATION,
    }
    d.update(kwargs)
    
    if d['config_dir'].startswith('~'):
        d['config_dir'] = os.path.expanduser(d['config_dir'])
    
    d['database_filepath'] = os.path.join(d['config_dir'], d['database_name'])
    
    return d
