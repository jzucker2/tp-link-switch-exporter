from flask import current_app as app
from ..clients.tp_link_switch import TPLinkSwitch
from ..metrics import Metrics
from .router import Router, RouterException


log = app.logger


class DebugRouterException(RouterException):
    pass


class DebugRouter(Router):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.switch_client = TPLinkSwitch.get_client()

    @property
    def service(self):
        return 'debug'

    @Metrics.DEBUG_ROUTE_TIME.time()
    def handle_debug_route_response(self):
        with Metrics.DEBUG_ROUTE_EXCEPTIONS.count_exceptions():
            p_m = 'handle debug route'
            log.debug(p_m)
            final_response = self.base_response('debug')
            self.switch_client.login()
            stats = self.switch_client.get_stats()
            log.info(f'stats: {stats}')
            return final_response
