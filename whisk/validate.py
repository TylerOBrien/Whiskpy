#
# Globals
#

from cerberus import errors as _errors

#
# Classes
#

class ErrorMeta(type):
    def __hash__(cls):
        return cls.__error_code__

    def __eq__(cls, error_code):
        return cls.__error_code__ == error_code

class ErrorTranslator(_errors.BasicErrorHandler):
    def __init__(self, ruleset, *args, **kwargs):
        self._error_messages = getattr(ruleset, 'Messages', None)
        super( ErrorTranslator, self ).__init__( *args, **kwargs )
    
    def _format_message(self, field, error):
        messages = getattr(self._error_messages, field, None)

        if messages:
            message = None
            if isinstance( messages, str ):
                message = messages
            elif isinstance( messages, dict ):
                if error.code in messages:
                    message = messages[error.code]
            if message:
                return message.format( *error.info, constraint=error.constraint, field=field, value=error.value )
        return super( ErrorTranslator, self )._format_message( field, error )

#
# Classes
#

class Rule(object, metaclass=ErrorMeta):
    def __init__(self, name, value):
        self.name = name
        self.value = value
    
    @property
    def schema(self):
        return { self.name: self.value }

class Ruleset(object):
    def __init__(self, *args, **kwargs):
        self.rules = kwargs['rules'] if 'rules' in kwargs else args
    
    @property
    def schema(self):
        schema = {}
        for rule in self.rules:
            schema.update( rule.schema )
        return schema

#
# 
#

class Required(Rule):
    __error_code__ = _errors.REQUIRED_FIELD.code

    def __init__(self):
        super( Required, self ).__init__( 'required', True )

class Check(Rule):
    __error_code__ = -1

    def __init__(self, predicate):
        super( Check, self ).__init__( 'check_with', predicate )

#
# Structures
#

class Contains(Rule):
    def __init__(self, children):
        super( Contains, self ).__init__( 'contains', children )

class Excludes(Rule):
    def __init__(self, children):
        super( Excludes, self ).__init__( 'excludes', children )

class NotEmpty(Rule):
    def __init__(self):
        super( NotEmpty, self ).__init__( 'empty', False )

#
# Types
#

class Type(Rule):
    __error_code__ = _errors.BAD_TYPE.code

    def __init__(self, typename):
        super( Type, self ).__init__( 'type', typename )

class Boolean(Type):
    def __init__(self):
        super( Boolean, self ).__init__('boolean')

class Date(Type):
    def __init__(self):
        super( Date, self ).__init__('date')

class DateTime(Type):
    def __init__(self):
        super( DateTime, self ).__init__('datetime')

class String(Type):
    def __init__(self):
        super( String, self ).__init__('string')

class Integer(Type):
    def __init__(self):
        super( Integer, self ).__init__('integer')

class Float(Type):
    def __init__(self):
        super( Float, self ).__init__('float')

class Number(Type):
    def __init__(self):
        super( Number, self ).__init__('number')

class Dict(Type):
    def __init__(self):
        super( Dict, self ).__init__('dict')

class List(Type):
    def __init__(self):
        super( List, self ).__init__('list')

#
# Math
#

class Min(Rule):
    def __init__(self, minimum):
        super( Min, self ).__init__( 'min', minimum )

#
# Equality
#

class Equal(Rule):
    __error_code__ = _errors.UNALLOWED_VALUE.code

    def __init__(self, *args, **kwargs):
        super( Equal, self ).__init__( 'allowed', args if not kwargs else [] )

Allowed = Equal

class NotEqual(Rule):
    __error_code__ = _errors.FORBIDDEN_VALUE.code

    def __init__(self, *args, **kwargs):
        super( NotEqual, self ).__init__( 'forbidden', args if not kwargs else [] )

Forbidden = NotEqual