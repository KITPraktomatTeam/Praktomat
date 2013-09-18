#!/usr/bin/env python
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.test')

import warnings
from django.core.cache import CacheKeyWarning
warnings.simplefilter("ignore", CacheKeyWarning)

from django.core.management import execute_from_command_line
if __name__ == "__main__":
    execute_from_command_line(sys.argv)
