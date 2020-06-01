#
# Globals
#

from marshmallow import Schema
from json        import loads as json_loads
from flask       import current_app, url_for
from flask.json  import JSONEncoder as _flask_JSONEncoder

#
# Flask Plugin
#

class FlaskPlugin(object):
    def __init__(self, app=None):
        self.app = app
        self._flask_appdata = {}

        if app is not None:
            self.init_app(app)
    
    def _get_appdata(self, key, *default):
        if current_app not in self._flask_appdata:
            self._flask_appdata[current_app] = {}
        return self._flask_appdata[current_app][key]
    
    def _set_appdata(self, key, value):
        if current_app not in self._flask_appdata:
            self._flask_appdata[current_app] = {}
        self._flask_appdata[current_app][key] = value
        return value

#
# JSON
#

class JSONEncoder(_flask_JSONEncoder):
    def default(self, obj):
        if isinstance( obj, JSONSerializeMixin ):
            return obj.to_json()
        return super().default(obj)

class JSONSerializeMixin(object):
    class Schema(Schema):
        pass

    def to_json(self, **kwargs):
        return self.Schema( **kwargs ).dump(self)

#
# Jinja2 Extensions
#

def _webpack_mix_get(app, name):
    def _filter_manifest(filename):
        pivot = filename.index('?')
        return dict( filename=filename[1:pivot], id=filename[pivot+4:] )
    
    manifest_path = '{}/mix-manifest.json'.format( app.config.get('STATIC_FOLDER') )

    with open(manifest_path) as file:
        manifest = json_loads( file.read() )
    
    return url_for('static', **_filter_manifest(manifest[name]))

def init_jinja_extensions(app):
    @app.context_processor
    def mix_processor():
        def mix(name):
            return _webpack_mix_get( app, name )
        return dict( mix=mix )