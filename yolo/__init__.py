import os
from simple_settings import LazySettings

os.environ.setdefault('SIMPLE_SETTINGS', 'settings,settings_local')

settings = LazySettings('settings', 'settings_local')

