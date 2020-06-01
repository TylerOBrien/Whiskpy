#
# Globals
#

from whisk.auth       import login_user
from whisk.controller import Controller, ServiceController

#
# Locals
#

from app.models import User

#
# Module
#

class UserController(ServiceController):
    class ErrorHandler(ServiceController.ErrorHandler):
        def index(self, request, **kwargs):
            return 'The index endpoint went badly'

    def index(self):
        return self.service.read_all()

    def show(self, id):
        return self.service.read_one()
    
    def login(self):
        pass