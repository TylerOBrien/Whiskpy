#
# Globals
#

from flask_login import UserMixin as AuthMixin, login_user, logout_user

#
# Globals
#

from .helpers import FlaskPlugin

#
# Module
#

class Auth(FlaskPlugin):
    def init_app(self, app):
        from flask_login import LoginManager
        from app.models  import User

        user_cls = self._set_appdata( 'user_cls', User )
        login_manager = self._set_appdata( 'login_manager', LoginManager(app) )

        @login_manager.user_loader
        def load_user(user_id):
            return user_cls.get(user_id)