#
# Globals
#

from cerberus import errors as _cerberus_errors, Validator as _cerberus_Validator
from flask    import request as _flask_request

#
# Locals
#

from .core     import jwt
from .validate import Ruleset
from .validate import *

#
# Module
#

class Header(object):
    def __init__(self, *args, **kwargs):
        self.name = kwargs['name'] if 'name' in kwargs else None

        rules = kwargs['rules'] if 'rules' in kwargs else None

        if not self.name and not rules:
            rules = args
        
        ruleset_cls = Ruleset if 'ruleset_cls' not in kwargs else kwargs['ruleset_cls']

        self.ruleset = ruleset_cls( *rules )
    
    @property
    def schema(self):
        return { self.name : self.ruleset.schema }

class Field(object):
    def __init__(self, *args, **kwargs):
        self.name = kwargs['name'] if 'name' in kwargs else None

        rules = kwargs['rules'] if 'rules' in kwargs else None

        if not self.name and not rules:
            rules = args
        
        ruleset_cls = Ruleset if 'ruleset_cls' not in kwargs else kwargs['ruleset_cls']

        self.ruleset = ruleset_cls( *rules )
    
    @property
    def schema(self):
        return { self.name : self.ruleset.schema }

class Request(object):
    def __init__(self, fields=None, headers=None, validation_engine=None):
        self._headers = []
        self._fields = []
        self._data = {
            'headers': headers if headers is not None else _flask_request,
            'fields': fields if fields is not None else _flask_request }
        self._validation_engine = validation_engine if validation_engine is not None else _cerberus_Validator(allow_unknown=True, error_handler=ErrorTranslator( self ))

        for name in dir(self):
            if not name.startswith('_') and name not in [ 'schema', 'headers', 'fields', 'headers_schema', 'fields_schema', 'errors' ]:
                attr = getattr(self, name)

                if isinstance(attr, Header) or isinstance(attr, Field):
                    if not attr.name:
                        attr.name = name
                    if isinstance(attr, Header):
                        self._headers.append(attr)
                    else:
                        self._fields.append(attr)
                elif isinstance(attr, tuple):
                    self._fields.append( Field(name=name, rules=attr) )
                elif isinstance(attr, Rule):
                    self._fields.append( Field(name=name, rules=[ attr ]) )
        
        self._rulesets = {
            'headers': Ruleset(rules=self._headers),
            'fields': Ruleset(rules=self._fields)
        }
    
    @property
    def headers_schema(self):
        return self._rulesets['headers'].schema
    
    @property
    def fields_schema(self):
        return self._rulesets['fields'].schema
    
    @property
    def headers(self):
        if self._data['headers'] is _flask_request:
            return { **_flask_request.headers }
        else:
            return self._data['headers']
    
    @property
    def fields(self):
        if self._data['fields'] is _flask_request:
            if _flask_request.method == 'GET':
                return _flask_request.args
            else:
                return _flask_request.form
        else:
            return self._data['fields']
    
    @property
    def errors(self):
        return self._validation_engine.errors
    
    def validate(self):
        if not self._validation_engine( self.headers, self.headers_schema ):
            return False
        if not self._validation_engine( self.fields, self.fields_schema ):
            return False
        return True

class Authorized(Request):
    def ValidToken(field, value, error):
        if not jwt.check_token(value):
            error(field, __name__)
    
    Authorization = Header( Required(), Check( ValidToken ) )

    class Messages:
        Authorization = 'Unauthorized'