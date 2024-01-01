from .base import *

OTHER_APPS = [
    "health_check.contrib.psutil",
]

INSTALLED_APPS += OTHER_APPS

PERSIST_HEALTH_CHECK_DATA = True
