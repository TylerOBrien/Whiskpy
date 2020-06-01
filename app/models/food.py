#
# Globals
#

from whisk.sql   import Column, ForeignKey, Relationship, Float, String, SmallInteger, BigInteger
from whisk.model import Model, IdcMixin

#
# Locals
#

class FoodGroup(Model, IdcMixin):
    name = Column( String(255) )

class Food(Model, IdcMixin):
    food_group_id = Column( BigInteger, ForeignKey('food_groups.id') )
    name          = Column( String(255) )
    description   = Column( String(255) )
    brand         = Column( String(255) )
    group         = Relationship( 'FoodGroup' )

class FoodMeta(Model, IdcMixin):
    food_id = Column( BigInteger, ForeignKey('foods.id') )
    name    = Column( String(255) )
    value   = Column( String(255) )
    food    = Relationship( 'Food', back_populates='meta' )

class FoodNutrient(Model, IdcMixin):
    food_id     = Column( BigInteger, ForeignKey('foods.id') )
    nutrient_id = Column( BigInteger, ForeignKey('nutrients.id') )
    amount      = Column( Float )
    unit        = Column( String(255) )
    nanograms   = ForeignKey( BigInteger )
    per         = Column( String(255) )

class FoodServing(Model, IdcMixin):
    user_id = Column( BigInteger, ForeignKey('users.id') )
    food_id = Column( BigInteger, ForeignKey('foods.id') )
    name    = Column( String(255) )
    amount  = Column( Float )
    unit    = Column( String(255) )
    order   = Column( SmallInteger )