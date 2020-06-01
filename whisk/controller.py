#
# Globals
#

from flask.views import View

#
# Module
#

class Controller(View):
    class ErrorHandler(object):
        def __call__(self, endpoint=None, handler_func=None, request=None, error_message=None, **kwargs):
            override_func = getattr( self, endpoint, None )
            if override_func:
                return override_func( endpoint=endpoint, handler_func=handler_func, request=request, error_message=error_message, **kwargs )
            else:
                return request.errors

    def __init__(self, request_cls=None, endpoint=None):
        self.request_cls = request_cls
        self.endpoint = endpoint

    def dispatch_request(self, *args, **kwargs):
        handler_func = getattr( self, self.endpoint )

        if self.request_cls:
            request = self.request_cls()
            if not request.validate():
                return self.ErrorHandler()( name=self.endpoint, handler_func=handler_func, request=request, **kwargs )
        
        return handler_func( **kwargs )

class ServiceController(Controller):
    def __init__(self, service, *args, **kwargs):
        self.service = service
        
        super().__init__( *args, **kwargs )