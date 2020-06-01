#
# Globals
#

from os import getcwd

#
# Module
#

ROOT_FOLDER     = getcwd()
CONFIG_FOLDER   = ROOT_FOLDER + '/config'
APP_FOLDER      = ROOT_FOLDER + '/app'
TEMPLATE_FOLDER = APP_FOLDER + '/templates'
STATIC_FOLDER   = APP_FOLDER + '/static'
MIX_MANIFEST    = STATIC_FOLDER + '/mix-manifest.json'