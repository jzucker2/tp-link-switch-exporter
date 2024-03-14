from flask import current_app as app
from ..clients.tp_link_switch import TPLinkSwitch
# from ..clients.tp_link_router import TPLinkRouter
from ..metrics import Metrics
from .router import Router, RouterException


log = app.logger


class TPLinkSwitchRouterException(RouterException):
    pass


class TPLinkSwitchRouter(Router):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.switch_client = TPLinkSwitch.get_client()

    @property
    def service(self):
        return 'tp_link_switch'

    @Metrics.TP_LINK_SWITCH_TEST_TIME.time()
    def test_switch_response(self):
        with Metrics.TP_LINK_SWITCH_TEST_EXCEPTIONS.count_exceptions():
            p_m = 'test for switch'
            log.debug(p_m)
            final_response = self.base_response('test_switch')
            self.switch_client.login()
            stats = self.switch_client.get_stats()
            log.info(f'stats: {stats}')
            return final_response
