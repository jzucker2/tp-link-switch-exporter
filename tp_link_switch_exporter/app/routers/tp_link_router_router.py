from flask import current_app as app
from ..clients.tp_link_router import TPLinkRouter
from ..metrics import Metrics
from .router import Router, RouterException


log = app.logger


class TPLinkRouterRouterException(RouterException):
    pass


class TPLinkRouterRouter(Router):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.router_client = TPLinkRouter.get_client()

    @property
    def service(self):
        return 'tp_link_router'

    @Metrics.TP_LINK_SWITCH_TEST_TIME.time()
    def test_router_response(self):
        with Metrics.TP_LINK_SWITCH_TEST_EXCEPTIONS.count_exceptions():
            p_m = 'test for router'
            log.debug(p_m)
            final_response = self.base_response('test_router')
            result = self.router_client.get_firmware()
            log.debug(f'result: {result}')
            return final_response
