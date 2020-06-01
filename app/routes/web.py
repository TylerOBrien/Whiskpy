#
# Globals
#

from whisk.resource import WebResource, Get

#
# Locals
#

from app.http.controllers import UserController
from app.models           import User

#
# Module
#

class UserResource(WebResource):
    index  = Get('/')

routes = [ 
    UserResource( User, UserController )
]