from flask import current_app as app
from ..routers.tp_link_switch_router import TPLinkSwitchRouter


log = app.logger


@app.route('/api/v1/tp-link-switch/test')
def test_tp_link_switch():
    router = TPLinkSwitchRouter()
    return router.test_switch_response()
