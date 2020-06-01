#
# Globals
#

from os import environ

#
# Module
#

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = '{type}://{username}:{password}@{host}/{database}'.format(
    type     = environ.get('DB_TYPE'),
    username = environ.get('DB_USERNAME'),
    password = environ.get('DB_PASSWORD'),
    host     = environ.get('DB_HOST'),
    database = environ.get('DB_DATABASE')
)