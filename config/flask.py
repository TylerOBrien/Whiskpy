#
# Globals
#

from os import environ

#
# Locals
#

from config.app      import *
from config.database import *

#
# Module
#

DEBUG = True
SECRET_KEY = environ.get('APP_KEY')