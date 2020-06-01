#
# Globals
#

from whisk.sql   import Column, String, SmallInteger, Relationship
from whisk.model import Model, IdcMixin

#
# Locals
#

class Nutrient(Model, IdcMixin):
    name       = Column( String(255) )
    short_name = Column( String(255) )
    alt_name   = Column( String(255) )
    group      = Column( String(255) )
    unit       = Column( String(255) )
    decimals   = Column( SmallInteger() )