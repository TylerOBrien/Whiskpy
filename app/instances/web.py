#
# Globals
#

from flask          import current_app
from whisk.resource import create_resource as _create_resource_base
from whisk.service  import WebService

#
# Module
#

def create_app(settings_override=None):
    from whisk.factory  import create_app as create_app_base
    from app.routes.web import routes

    app = create_app_base(__name__, routes, settings_override)

    return app

def create_resource(model_cls, service_cls=WebService, **kwargs):
    config = dict(
        template_folder = '{}/{}'.format( current_app.config.get('TEMPLATE_FOLDER'), model_cls.__pluralname__ ),
        **kwargs
    )

    return _create_resource_base( model_cls=model_cls, service_cls=service_cls, **kwargs )