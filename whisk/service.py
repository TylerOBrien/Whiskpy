#
# Globals
#

from flask import jsonify, render_template

#
# Operations
#

class BaseOperation(object):
    pass

#
# SQL Read/Write
#

class BaseSQLOperation(BaseOperation):
    def __init__(self, model_cls, pk_name='id', pk_type='int'):
        self.model_cls = model_cls
        self.pk_name = pk_name
        self.pk_type = pk_type

class SQLReadOperation(BaseSQLOperation):
    def __init__(self, model_cls, **kwargs):
        super().__init__( model_cls=model_cls, **kwargs )

    def _read(self, **kwargs):
        rv = None
        
        if kwargs[self.pk_name] is None:
            rv = self.model_cls.all()
        else:
            rv = self.model_cls.get( kwargs[self.pk_name] )
        
        return rv
    
    def read_all(self):
        return self._read( **{ self.pk_name : None } )
    
    def read_one(self, pk):
        return self._read( **{ self.pk_name : pk } )

class SQLWriteOperation(BaseSQLOperation):
    def __init__(self, model_cls, **kwargs):
        super().__init__( model_cls=model_cls, **kwargs )

#
# Service
#

class Service(object):
    def __init__(self, plural_name, singular_name):
        self.plural_name = plural_name
        self.singular_name = singular_name

#
# SqlService
#

class SqlService(Service, SQLReadOperation, SQLWriteOperation):
    def __init__(self, model_cls, **kwargs):
        Service.__init__( self, plural_name=model_cls.__pluralname__, singular_name=model_cls.__singularname__ )
        SQLReadOperation.__init__( self, model_cls=model_cls, **kwargs )
        SQLWriteOperation.__init__( self, model_cls=model_cls, **kwargs )

#
# Api/Web
#

class ApiService(SqlService):
    def _read(self, **kwargs):
        return jsonify( super()._read( **kwargs ) )

class WebService(SqlService):
    def _read(self, **kwargs):
        name = self.plural_name if kwargs[self.pk_name] is None else self.singular_name
        template_params = { name: super()._read( **kwargs ) }

        return render_template( '{}.html'.format(name), **template_params )