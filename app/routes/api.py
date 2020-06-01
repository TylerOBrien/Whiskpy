#
# Locals
# 

from app.models           import User
from app.http.controllers import UserController
from app.http.requests    import UserResource

#
# Module
#

routes = [
    UserResource( User, UserController )
]