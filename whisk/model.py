#
# Globals
#

from contextlib                 import contextmanager
from marshmallow                import Schema
from datetime                   import datetime
from sqlalchemy                 import Column, String, DateTime, BigInteger, ForeignKey
from sqlalchemy.orm             import class_mapper, synonym
from sqlalchemy.orm.exc         import UnmappedClassError
from sqlalchemy.ext.declarative import DeclarativeMeta, declared_attr, declarative_base

#
# Locals
#

from .core     import db
from .database import Query
from .helpers  import JSONSerializeMixin
from .security import hash_password

#
# Mixins
#

class PkMixin(object):
    __pk_name__ = 'id'
    __pk_type__ = BigInteger

    @declared_attr
    def __pk_config__(cls):
        return ( cls.__pk_name__, cls.__pk_type__ )
    
    @declared_attr
    def pk(cls):
        return Column( *cls.__pk_config__, primary_key=True )

class IdMixin(PkMixin):
    @declared_attr
    def id(cls):
        return synonym('pk')

class ChronoMixin(object):
    created_at = Column( DateTime, default=datetime.utcnow, nullable=False )
    updated_at = Column( DateTime )

#
# Query
#

class _QueryProperty(object):
    def __get__(self, obj, type):
        try:
            mapper = class_mapper(type)
            if mapper:
                return type.query_cls( mapper, session=db.session )
        except UnmappedClassError:
            return None

#
# Meta
#

class _Meta(DeclarativeMeta):
    def __init__(cls, classname, bases, dict_):
        return super().__init__( classname, bases, dict_ )

    def __call__(cls, *args, **kwargs):
        for key in kwargs:
            if hasattr(cls, 'SetAttributes') and type(getattr(cls, 'SetAttributes')) is type:
                if key in getattr(cls, 'SetAttributes').__dict__:
                    kwargs[key] = getattr(cls, 'SetAttributes').__dict__[key]( kwargs[key] )
            else:
                set_fn = 'set_{}'.format(key)
                if hasattr(cls, set_fn):
                    kwargs[key] = getattr( cls, set_fn )( cls, kwargs[key] )
        return super().__call__( *args, **kwargs )

#
# Model
#

class ModelSessionContext(object):
    def __init__(self, model):
        self.model = model
        self.name = 'whisk_model_{}'.format( self.model.__tablename__ )

    def __enter__(self):
        session = db.create_session( self.name )
        session.add( self.model )

        return session
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if not any([ exc_type, exc_val, exc_tb ]):
            db.get_session( self.name ).flush()
            db.session.merge( self.model )
        db.close_session( self.name )
    
    def init(self):
        pass
    
    def teardown(self):
        pass

class Model(JSONSerializeMixin):
    class Schema(Schema):
        pass

    class SessionContext(object):
        pass
    
    __pkname__ = 'id'
    __pktype__ = BigInteger
    __pktypename__ = 'int'

    query = None
    query_cls = Query
    
    @declared_attr
    def __singularname__(cls):
        return cls.__name__.lower()
    
    @declared_attr
    def __pluralname__(cls):
        if cls.__singularname__[-1] == 'y':
            return cls.__singularname__[:-1] + 'ies'
        else:
            return cls.__singularname__ + 's'

    @declared_attr
    def __tablename__(cls):
        return cls.__pluralname__

    def __repr__(self):
        return '<{0.__class__.__name__} {0.pk}>'.format(self)
    
    """ def __getattr__(self, key):
        value = self.__dict__[key]
        get_attrs = getattr( self, 'GetAttributes', None )

        if get_attrs and type(get_attrs) is type:
            if key in set_attrs.__dict__:
                value = get_attrs.__dict__[key](value)
        else:
            get_fn = 'get_{}'.format(key)
            if hasattr( self, get_fn ):
                value = getattr( self, get_fn )(value)

        return value """
    
    def __setattr__(self, key, value):
        set_attrs = getattr( self, 'SetAttributes', None )

        if set_attrs and type(set_attrs) is type:
            if key in set_attrs.__dict__:
                value = set_attrs.__dict__[key]( value )
        else:
            set_fn = getattr( self, 'set_{}'.format(key), None )
            if set_fn and callable(set_fn):
                value = set_fn(value)
        
        self.__dict__[key] = value

    @contextmanager
    def db_session(self):
        name = 'whisk_model_{}'.format( self.__tablename__ )
        session = db.create_session( name, autoflush=False )

        try:
            yield session
            session.flush()
        except:
            session.rollback()
            raise
        finally:
            db.session.merge(self)
            session.close()
    
    @classmethod
    def get(cls, *args, **kwargs):
        return cls.query.get(*args, **kwargs)
    
    @classmethod
    def all(cls, *args, **kwargs):
        return cls.query.all(*args, **kwargs)
    
    @classmethod
    def all_by(cls, *args, **kwargs):
        return cls.query.filter_by(*args, **kwargs).all()
    
    @classmethod
    def all_to_json(cls, *args, **kwargs):
        return cls.query.all_to_json(*args, **kwargs)
    
    @classmethod
    def first(cls, *args, **kwargs):
        return cls.query.first(*args, **kwargs)
    
    @classmethod
    def first_by(cls, *args, **kwargs):
        return cls.query.filter_by(*args, **kwargs).first()
    
    @classmethod
    def first_to_json(cls, *args, **kwargs):
        return cls.query.first_to_json(*args, **kwargs)
    
    @classmethod
    def filter(cls, *args, **kwargs):
        return cls.query.filter(*args, **kwargs)
    
    @classmethod
    def filter_by(cls, *args, **kwargs):
        return cls.query.filter_by(*args, **kwargs)

Model = declarative_base( cls=Model, metaclass=_Meta )
Model.query = _QueryProperty()

class IdcMixin(IdMixin, ChronoMixin):
    pass