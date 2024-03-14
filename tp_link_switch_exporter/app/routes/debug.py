from flask import current_app as app
from ..routers.debug_router import DebugRouter


log = app.logger


@app.route('/api/v1/debug')
def handle_debug_route():
    router = DebugRouter()
    return router.handle_debug_route_response()
