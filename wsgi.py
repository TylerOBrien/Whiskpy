#
# Setup
#

from dotenv import load_dotenv

load_dotenv()

#
# Globals
#

from werkzeug.serving    import run_simple
from werkzeug.middleware import dispatcher

#
# Locals
#

from app import api, web

#
# Module
#

application = dispatcher.DispatcherMiddleware(web.create_app(), {
    '/api/v1': api.create_app()
})

if __name__ == '__main__':
    run_simple('0.0.0.0', 5000, application,
               use_reloader=True, use_debugger=True)