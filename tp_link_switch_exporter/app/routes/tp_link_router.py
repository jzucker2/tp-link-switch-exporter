from flask import current_app as app
from ..routers.tp_link_router_router import TPLinkRouterRouter


log = app.logger


@app.route('/api/v1/tp-link-router/test')
def test_tp_link_router():
    router = TPLinkRouterRouter()
    return router.test_router_response()
