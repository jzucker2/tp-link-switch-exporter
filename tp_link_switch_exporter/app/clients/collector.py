from flask import current_app as app
from ..utils import global_get_now
from ..common.scrape_events import ScrapeEvents
from ..metrics import Metrics
from .tp_link_switch import TPLinkSwitch
# from .tp_link_switch import TPLinkRouter


log = app.logger


class CollectorException(Exception):
    pass


class Collector(object):
    DEFAULT_SWITCH_NAME = 'default'

    @classmethod
    def default_switch_name(cls):
        return cls.DEFAULT_SWITCH_NAME

    @classmethod
    def get_collector(cls, switch_client=None, **kwargs):
        if not switch_client:
            switch_client = TPLinkSwitch.get_client(**kwargs)
        switch_name = kwargs.get('switch_name')
        if not switch_name:
            switch_name = cls.default_switch_name()
        return cls(switch_client, switch_name)

    def __init__(self, switch_client, switch_name):
        super().__init__()
        self.switch_client = switch_client
        self.switch_name = switch_name
        self._last_power_value = None

    @classmethod
    def get_now(cls):
        return global_get_now()

    def __repr__(self):
        return f'Collector => blah: {self._last_power_value}'

    def _inc_scrape_event(self, event):
        Metrics.ROUTER_SCRAPE_EVENT_COLLECTOR_COUNTER.labels(
            switch_name=self.switch_name,
            scrape_event=event.value,
        ).inc()

    @property
    def switch_ip(self):
        return self.switch_client.switch_ip

    def _authorize(self):
        # self.switch_client.authorize()
        event = ScrapeEvents.AUTHORIZE
        self._inc_scrape_event(event)

    def _logout(self):
        pass
        event = ScrapeEvents.LOGOUT
        self._inc_scrape_event(event)

    def _get_firmware(self):
        pass
        event = ScrapeEvents.GET_FIRMWARE
        self._inc_scrape_event(event)

    def _get_status(self):
        pass
        event = ScrapeEvents.GET_STATUS
        self._inc_scrape_event(event)

    # def _record_status_metrics(self, status):
    #     if not status:
    #         return
    #     Metrics.ROUTER_WIFI_CLIENTS_TOTAL.labels(
    #         switch_name=self.switch_name,
    #     ).set(status.wifi_clients_total)
    #     Metrics.ROUTER_WIRED_CLIENTS_TOTAL.labels(
    #         switch_name=self.switch_name,
    #     ).set(status.wired_total)
    #     Metrics.ROUTER_CLIENTS_TOTAL.labels(
    #         switch_name=self.switch_name,
    #     ).set(status.clients_total)
    #     Metrics.ROUTER_MEMORY_USAGE.labels(
    #         switch_name=self.switch_name,
    #     ).set(status.mem_usage)
    #     Metrics.ROUTER_CPU_USAGE.labels(
    #         switch_name=self.switch_name,
    #     ).set(status.cpu_usage)

    # def _record_firmware_metrics(self, firmware):
    #     if not firmware:
    #         return
    #     log.debug(f'got firmware: {firmware}')

    def _get_switch_metrics(self):
        log.debug('_get_switch_metrics')
        self._inc_scrape_event(ScrapeEvents.ATTEMPT_GET_ROUTER_METRICS)
        try:
            # authorizing
            a_m = (f'attempting to authorize at '
                   f'self.switch_ip: {self.switch_ip}')
            log.debug(a_m)
            self._authorize()
            sa_m = (f'self.switch_ip: {self.switch_ip} '
                    f'succeeded at auth')
            log.debug(sa_m)
            # Get firmware info - returns Firmware
            # firmware = self._get_firmware()
            # log.debug(f'switch firmware: {firmware}')
            # self._record_firmware_metrics(firmware)
            #
            # # Get status info - returns Status
            # status = self._get_status()
            # log.debug(f'switch status: {status}')
            # self._record_status_metrics(status)
        except Exception as unexp:
            u_m = (f'self.switch_ip: {self.switch_ip} '
                   f'got exception unexp: {unexp}')
            log.error(u_m)
            self._inc_scrape_event(ScrapeEvents.ERROR)
        else:
            u_m = (f'self.switch_ip: {self.switch_ip} '
                   f'scraped successfully!')
            log.debug(u_m)
            self._inc_scrape_event(ScrapeEvents.SUCCESS)

        finally:
            # always logout as TP-Link Web
            # Interface only supports upto 1 user logged
            l_m = f'now logging out from self.switch_ip: {self.switch_ip}'
            log.debug(l_m)
            self._logout()

    def get_switch_metrics(self):
        return self._get_switch_metrics()

    def update_switch_metrics(self):
        return self.get_switch_metrics()
