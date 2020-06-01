#
# Globals
#

from whisk.request  import Request, Field, Required
from whisk.resource import ApiResource, RestfulMixin
from whisk.security import check_password

#
# Models
#

from app.models import User

#
# Module
#

class UserAuthRequest(Request):
    email    = Field( Required() )
    password = Field( Required() )

class UserCreateRequest(Request):
    email = Field( Required() )

    class Messages:
        email = {
            Required: 'You must supply an email'
        }

class UserResource(ApiResource, RestfulMixin):
    class Requests:
        create = UserCreateRequest