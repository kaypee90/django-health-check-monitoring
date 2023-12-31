"""
Settings used by mpharma project.
This consists of the general produciton settings, with an optional import of any local
settings.
"""
import os
from config.settings.production import *

try:
    if os.environ.get("DEV_ENV"):
        from config.settings.development import *
except ImportError:
    pass
