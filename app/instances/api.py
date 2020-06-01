#
# Module
#

def create_app(settings_override=None):
    from whisk.factory  import create_app as _create_app_base
    from app.routes.api import routes

    app = _create_app_base(__name__, routes, settings_override)

    return app