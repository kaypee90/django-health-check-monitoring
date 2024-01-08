from .base import *

OTHER_APPS = [
    "health_check.contrib.psutil",
]

INSTALLED_APPS += OTHER_APPS

PERSIST_HEALTH_CHECK_DATA = True

SYNC_APP_ID = "3959d4f2-8abb-408b-b8e8-c0eb56576af9"
SYNC_SERVER_URL = "http://localhost:8000"
SYNC_HEALTH_CHECK_DATA = True
