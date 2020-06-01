#
# Globals
#

from flask import Blueprint as _flask_Blueprint

#
# Locals
#

from .schema  import SchemaItem, SchemaModel
from .service import ApiService, WebService

#
# Route
#

class Route(SchemaItem):
    def __init__(self, method, uri, request_cls=None, **kwargs):
        super( Route, self ).__init__( method=method, uri=uri, request_cls=request_cls, config={ **kwargs } )
    
    def create_url_rule(self, service, controller_cls):
        options = self.config['options'] if 'options' in self.config else {}

        if 'defaults' in options:
            defaults = {}
            for key,value in options['defaults'].items():
                defaults[ key.format(**self.config) ] = value
            options['defaults'] = defaults
        
        return dict(
            **options,
            rule = self.uri.format(**self.config),
            endpoint = self.name,
            methods = [ self.method ],
            view_func = controller_cls.as_view( self.name, service, self.request_cls, self.name )
        )

class Get(Route):
    def __init__(self, uri, **kwargs):
        super( Get, self ).__init__( method='GET', uri=uri, **kwargs )

class Post(Route):
    def __init__(self, uri, **kwargs):
        super( Post, self ).__init__( method='POST', uri=uri, **kwargs )

class Put(Route):
    def __init__(self, uri, **kwargs):
        super( Put, self ).__init__( method='PUT', uri=uri, **kwargs )

class Delete(Route):
    def __init__(self, uri, **kwargs):
        super( Delete, self ).__init__( method='DELETE', uri=uri, **kwargs )

#
# Blueprint
#

class Blueprint(SchemaModel):
    def __init__(self, **kwargs):
        self.config = kwargs

        for name in dir(self):
            if not name.startswith('_') and not name.startswith('schema'):
                attr = getattr( self, name )

                if isinstance( attr, SchemaItem ):
                    if not getattr( attr, name, None ):
                        attr.name = name
                    if not getattr( attr, 'config', None ):
                        attr.config = {}
                    attr.config.update( self.config )

    def to_flask_blueprint(self, name, import_name, service=None, controller_cls=None, **kwargs):
        blueprint = _flask_Blueprint( name, import_name, **kwargs )

        for name,route in self.model.items():
            blueprint.add_url_rule( **route.create_url_rule( service, controller_cls ) )

        return blueprint

#
# Resource
#

class Resource(Blueprint):
    def __init__(self, service, controller_cls, **blueprint_kwargs):
        self.service = service
        self.controller_cls = controller_cls
        self.blueprint_kwargs = blueprint_kwargs

        config = dict(
            pk_name = service.model_cls.__pkname__,
            pk_type = service.model_cls.__pktypename__
        )

        super( Resource, self ).__init__( **config )
    
    def to_flask_blueprint(self):
        name = self.service.model_cls.__pluralname__
        url_prefix = '/' + name
        config = dict(
            **self.blueprint_kwargs,
            service = self.service,
            controller_cls = self.controller_cls,
            url_prefix = url_prefix
        )

        return super( Resource, self ).to_flask_blueprint( name, __name__, **config )

class ApiResource(Resource):
    def __init__(self, model_cls, controller_cls, **kwargs):
        super().__init__( ApiService(model_cls), controller_cls, **kwargs )

class WebResource(Resource):
    def __init__(self, model_cls, controller_cls, **kwargs):
        super().__init__( WebService(model_cls), controller_cls, **kwargs )

class RestfulMixin(Resource):
    index  = Get( '/', defaults={ '{pk_name}': None } )
    show   = Get( '/<{pk_type}:{pk_name}>' )
    create = Post( '/' )
    update = Put( '/<{pk_type}:{pk_name}>' )
    delete = Delete( '/<{pk_type}:{pk_name}>' )

#
# Functions
#

def create_resource(model_cls=None, service_cls=None, controller_cls=None, resource_cls=None, **kwargs):
    config = dict(
        **kwargs,
        controller_cls = controller_cls
    )

    return resource_cls( service_cls(model_cls), **config )