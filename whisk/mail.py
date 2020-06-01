#
# Globals
#

from flask_mail import Message, Mail as _flask_Mail

#
# Locals
#

from .helpers import FlaskPlugin

#
# Module
#

class Mail(FlaskPlugin):
    def init_app(self, app):
        pass