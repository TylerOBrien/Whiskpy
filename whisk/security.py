#
# Globals
#

from flask        import current_app as _current_app
from bcrypt       import gensalt, checkpw as _checkpw, hashpw as _hashpw
from itsdangerous import SignatureExpired as _SignatureExpired, BadSignature as _BadSignature, TimedJSONWebSignatureSerializer as _TimedJWS

#
# Locals
#

from .helpers import FlaskPlugin

#
# Functions
#

def check_password(password, hashed_password):
    return _checkpw(password, hashed_password)

def hash_password(password):
    if type(password) is str:
        password = password.encode('utf-8')
    return _hashpw(password, gensalt())

#
# Module
#

class JSONWebToken(FlaskPlugin):
    TOKEN_VALID   = 0
    TOKEN_INVALID = 1
    TOKEN_EXPIRED = 2

    def init_app(self, app):
        self._set_appdata( 'jws', _TimedJWS( app.secret_key, expires_in=3600 ) )
    
    def check_token(self, token):
        try:
            self._get_appdata('jws').loads(token)
        except _SignatureExpired:
            return self.TOKEN_EXPIRED
        except _BadSignature:
            return self.TOKEN_INVALID
        return self.TOKEN_VALID
    
    def valid_token(self, token):
        return self.check_token(token) is self.TOKEN_VALID
    
    def expired_token(self, token):
        return self.check_token(token) is self.TOKEN_EXPIRED