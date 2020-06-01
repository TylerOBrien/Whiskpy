#
# Globals
#

from marshmallow import Schema
from whisk.sql   import Column, BigInteger, ForeignKey, String, Relationship
from whisk.model import Model, IdcMixin

#
# Locals
#

class Message(Model, IdcMixin):
    user_id = Column( BigInteger, ForeignKey('users.id') )
    #user    = Relationship('User', backref_populates='messages')
    subject = Column(String(255))
    content = Column(String(255))

    class Schema(Schema):
        class Meta:
            fields = ('id', 'subject', 'content', 'created_at', 'updated_at')