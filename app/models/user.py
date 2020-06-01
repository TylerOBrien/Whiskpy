#
# Globals
#

from whisk.auth     import AuthMixin
from whisk.security import hash_password
from whisk.sql      import Column, String, BigInteger, ForeignKey, Relationship
from whisk.model    import Model, IdcMixin

#
# Locals
#

class User(Model, IdcMixin):
    email    = Column( String(255), index=True, unique=True )
    password = Column( String(255) )

    class SetAttributes:
        password = hash_password

    class Schema(Model.Schema):
        class Meta:
            fields = ('id', 'email', 'created_at', 'updated_at')

class UserMeta(Model, IdcMixin):
    user_id = Column( BigInteger, ForeignKey('users.id') )
    group   = Column( String(255) )
    name    = Column( String(255) )
    value   = Column( String(255) )
    #user    = Relationship( 'User', back_populates='meta' )