from flask import current_app as app
from ..utils import global_get_now
from ..common.scrape_events import ScrapeEvents
from ..metrics import Metrics
from .tp_link_router import TPLinkRouter


log = app.logger


class CollectorException(Exception):
    pass


class Collector(object):
    DEFAULT_ROUTER_NAME = 'default'

    @classmethod
    def default_router_name(cls):
        return cls.DEFAULT_ROUTER_NAME

    @classmethod
    def get_collector(cls, router_client=None, **kwargs):
        if not router_client:
            router_client = TPLinkRouter.get_client(**kwargs)
        router_name = kwargs.get('router_name')
        if not router_name:
            router_name = cls.default_router_name()
        return cls(router_client, router_name)

    def __init__(self, router_client, router_name):
        super().__init__()
        self.router_client = router_client
        self.router_name = router_name
        self._last_power_value = None

    @classmethod
    def get_now(cls):
        return global_get_now()

    def __repr__(self):
        return f'Collector => blah: {self._last_power_value}'

    def _inc_scrape_event(self, event):
        Metrics.ROUTER_SCRAPE_EVENT_COLLECTOR_COUNTER.labels(
            router_name=self.router_name,
            scrape_event=event.value,
        ).inc()

    @property
    def router_ip(self):
        return self.router_client.router_ip

    def _authorize(self):
        self.router_client.authorize()
        event = ScrapeEvents.AUTHORIZE
        self._inc_scrape_event(event)

    def _logout(self):
        self.router_client.logout()
        event = ScrapeEvents.LOGOUT
        self._inc_scrape_event(event)

    def _get_firmware(self):
        firmware = self.router_client.get_firmware()
        event = ScrapeEvents.GET_FIRMWARE
        self._inc_scrape_event(event)
        return firmware

    def _get_status(self):
        status = self.router_client.get_status()
        event = ScrapeEvents.GET_STATUS
        self._inc_scrape_event(event)
        return status

    def _record_status_metrics(self, status):
        if not status:
            return
        Metrics.ROUTER_WIFI_CLIENTS_TOTAL.labels(
            router_name=self.router_name,
        ).set(status.wifi_clients_total)
        Metrics.ROUTER_WIRED_CLIENTS_TOTAL.labels(
            router_name=self.router_name,
        ).set(status.wired_total)
        Metrics.ROUTER_CLIENTS_TOTAL.labels(
            router_name=self.router_name,
        ).set(status.clients_total)
        Metrics.ROUTER_MEMORY_USAGE.labels(
            router_name=self.router_name,
        ).set(status.mem_usage)
        Metrics.ROUTER_CPU_USAGE.labels(
            router_name=self.router_name,
        ).set(status.cpu_usage)

    def _record_firmware_metrics(self, firmware):
        if not firmware:
            return
        log.debug(f'got firmware: {firmware}')

    def _get_router_metrics(self):
        log.debug('_get_router_metrics')
        self._inc_scrape_event(ScrapeEvents.ATTEMPT_GET_ROUTER_METRICS)
        try:
            # authorizing
            a_m = (f'attempting to authorize at '
                   f'self.router_ip: {self.router_ip}')
            log.debug(a_m)
            self._authorize()
            sa_m = (f'self.router_ip: {self.router_ip} '
                    f'succeeded at auth')
            log.debug(sa_m)
            # Get firmware info - returns Firmware
            firmware = self._get_firmware()
            log.debug(f'router firmware: {firmware}')
            self._record_firmware_metrics(firmware)

            # Get status info - returns Status
            status = self._get_status()
            log.debug(f'router status: {status}')
            self._record_status_metrics(status)
        except Exception as unexp:
            u_m = (f'self.router_ip: {self.router_ip} '
                   f'got exception unexp: {unexp}')
            log.error(u_m)
            self._inc_scrape_event(ScrapeEvents.ERROR)
        else:
            u_m = (f'self.router_ip: {self.router_ip} '
                   f'scraped successfully!')
            log.debug(u_m)
            self._inc_scrape_event(ScrapeEvents.SUCCESS)

        finally:
            # always logout as TP-Link Web
            # Interface only supports upto 1 user logged
            l_m = f'now logging out from self.router_ip: {self.router_ip}'
            log.debug(l_m)
            self._logout()

    def get_router_metrics(self):
        return self._get_router_metrics()

    def update_router_metrics(self):
        return self.get_router_metrics()
