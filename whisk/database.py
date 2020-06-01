#
# Globals
#

from flask          import _app_ctx_stack, current_app
from sqlalchemy     import create_engine
from sqlalchemy.orm import sessionmaker as _sessionmaker, Query as _BaseQuery

#
# Globals
#

from .helpers import FlaskPlugin, JSONSerializeMixin

#
# Module
#

class WhiskSqlError(Exception):
    def __init__(self, message):
        self.message = message

class WhiskSql(FlaskPlugin):
    def init_app(self, app):
        app.config['WHISK_DB_SESSION_NAME'] = 'whisk_db_global_session'

        engine = create_engine( current_app.config['SQLALCHEMY_DATABASE_URI'] )

        self._set_appdata( 'engine', engine )
        self._set_appdata( 'session_cls', self.create_session_cls() )
        self._set_appdata( 'sessions', {} )
        self._set_appdata( 'is_global_session_reload_pending', False )

        app.teardown_appcontext( self.teardown )
    
    def teardown(self, exception):
        ctx = _app_ctx_stack.top
        name = current_app.config['WHISK_DB_SESSION_NAME']
        global_session = getattr( ctx, name, None )

        if global_session is not None:
            global_session.commit()
            global_session.close()
        
        for _,session in self._get_appdata('sessions').items():
            session.close()
    
    def reload_global_session(self):
        ctx = _app_ctx_stack.top
        name = current_app.config['WHISK_DB_SESSION_NAME']

        if ctx is not None:
            self._set_appdata( 'is_global_session_reload_pending', True )
    
    def get_session(self, name, create_if_not_found=False, **create_kwargs):
        session = None
        sessions = self._get_appdata('sessions')

        if name not in sessions:
            if create_if_not_found:
                session = self.create_session( name, **create_kwargs )
        else:
            session = sessions[name]
        
        return session
    
    def create_session_cls(self, **kwargs):
        if 'bind' not in kwargs:
            kwargs['bind'] = self._get_appdata('engine')
        return _sessionmaker( **kwargs )
    
    def create_session(self, name, session_cls=None, **kwargs):
        sessions = self._get_appdata('sessions')

        if name in sessions:
            raise WhiskSqlError( 'Session "{}" already exists'.format(name) )
        
        if not session_cls:
            session = self._get_appdata('session_cls')( **kwargs )
        else:
            session = session_cls()
        
        sessions[name] = session
        
        return session
    
    def close_session(self, name):
        sessions = self._get_appdata('sessions')

        if name not in sessions:
            raise WhiskSqlError( 'Session "{}" not found'.format(name) )

        sessions[name].close()
        
        del sessions[name];
    
    @property
    def session(self):
        ctx = _app_ctx_stack.top
        name = current_app.config['WHISK_DB_SESSION_NAME']

        if ctx is not None:
            global_session = getattr( ctx, name, None )
            is_reload_pending = self._get_appdata( 'is_global_session_reload_pending' )
            
            if global_session is None or is_reload_pending:
                global_session = self._get_appdata('session_cls')()
                setattr( ctx, name, global_session )
            
            if is_reload_pending:
                self._set_appdata( 'is_global_session_reload_pending', False )

            return global_session

#
# Query
#

class Query(_BaseQuery, JSONSerializeMixin):
    def all_to_json(self):
        return [ row.to_json() for row in self.all() ]
    
    def first_to_json(self):
        return self.first().to_json()
    
    def to_json(self):
        return self.all_to_json()