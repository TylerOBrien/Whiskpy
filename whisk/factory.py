#
# Globals
#

from os    import getcwd
from flask import Flask as _flask_Flask, Blueprint as _flask_Blueprint

#
# Locals
#

from .helpers import JSONEncoder

#
# Module
#

def create_app(package_name, routes=[], settings_override=None):
    from werkzeug.debug import DebuggedApplication

    package_path = getcwd()
    app = _flask_Flask( package_name, root_path='{}/app'.format(package_path) )

    app.config.from_pyfile( '{}/config/flask.py'.format(package_path) )
    app.config.from_object( settings_override )

    app.json_encoder = JSONEncoder

    if app.debug:
        app.wsgi_app = DebuggedApplication( app.wsgi_app, True )
    else:
        pass

    with app.app_context():
        from .core import auth, db, jwt

        auth.init_app(app)
        db.init_app(app)
        jwt.init_app(app)

        for route in routes:
            if not isinstance( route, _flask_Blueprint ) :
                if hasattr( route, 'to_flask_blueprint' ):
                    route = route.to_flask_blueprint()
            app.register_blueprint(route)

        return app