#
# Item
#

class SchemaItemError(Exception):
    def __init__(self, message):
        self.message = message

class SchemaItem(object):
    def __init__(self, **kwargs):
        for key,value in kwargs.items():
            if key == 'schema':
                raise SchemaItemError('Cannot have schema item named "schema"')
            setattr( self, key, value )

    @property
    def schema(self):
        rv = {}
        for name in dir(self):
            if not name.startswith('_') and name != 'schema':
                rv[name] = getattr( self, name )
        return rv

#
# Model
#

class SchemaModel(object):
    def _get_schema_item(self, name):
        attr = getattr( self, name )
        if isinstance( attr, SchemaItem ):
            return attr
        return None
    
    def _gen_schema_items(self):
        for name in dir(self):
            if not name.startswith('_') and name not in [ 'schema', 'model' ]:
                attr = self._get_schema_item(name)
                if attr:
                    yield name,attr

    @property
    def schema(self):
        items = {}
        for name,item in self._gen_schema_items():
            items[name] = item.schema
        return items
    
    @property
    def model(self):
        items = {}
        for name,item in self._gen_schema_items():
            items[name] = item
        return items