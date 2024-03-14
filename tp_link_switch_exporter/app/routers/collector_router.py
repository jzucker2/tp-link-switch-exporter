from flask import current_app as app
from ..clients.config_parser import ConfigParser
from ..clients.env_vars import EnvVars
from ..common.config_keys import ConfigKeys
from ..clients.collector import Collector
from ..metrics import Metrics
from .router import Router, RouterException


log = app.logger


class CollectorRouterException(RouterException):
    pass


class CollectorRouter(Router):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._config = None
        self.collector = Collector.get_collector()
        self._collectors = None

    @property
    def config(self):
        if not self._config:
            self._config = ConfigParser.import_config()
        return self._config

    @property
    def collectors(self):
        if not self._collectors:
            collectors = self._create_collectors()
            self._collectors = list(collectors)
        return self._collectors

    @classmethod
    def _create_collector(cls, ip, name, password):
        return Collector.get_collector(
            router_ip=ip,
            router_password=password,
            router_name=name)

    @classmethod
    def _create_env_var_collector(cls):
        router_name = EnvVars.get_default_router_name()
        router_ip = EnvVars.get_default_router_ip()
        router_password = EnvVars.get_default_router_password()
        return cls._create_collector(router_ip, router_name, router_password)

    @classmethod
    def _create_collector_from_config(cls, router_config):
        router_name = router_config[ConfigKeys.ROUTER_NAME.key_name]
        router_ip = router_config[ConfigKeys.ROUTER_IP.key_name]
        router_password = router_config[ConfigKeys.ROUTER_PASSWORD.key_name]
        collector = cls._create_collector(
            router_ip,
            router_name,
            router_password)
        return collector

    @classmethod
    def _has_router_config_env_vars(cls):
        return EnvVars.has_router_config_env_vars()

    @classmethod
    def should_use_config_file(cls):
        if cls._has_router_config_env_vars():
            return False
        return True

    def _get_config_routers(self):
        config = self.config
        return ConfigParser.get_routers(config)

    def _create_collectors(self):
        collectors = []
        if self.should_use_config_file():
            log.debug('Using yml config file for router configs')
            routers = self._get_config_routers()
            for router_config in routers:
                collector = self._create_collector_from_config(router_config)
                collectors.append(collector)
        else:
            log.debug('Using env vars for router configs')
            collector = self._create_env_var_collector()
            collectors.append(collector)
        return list(collectors)

    @property
    def service(self):
        return 'collector'

    @Metrics.SIMPLE_COLLECTOR_ROUTE_TIME.time()
    def handle_simple_collector_route_response(self):
        with Metrics.SIMPLE_EXPORTER_ROUTE_EXCEPTIONS.count_exceptions():
            p_m = 'handle simple collector route'
            log.debug(p_m)
            final_response = self.base_response('simple')
            collector = self._create_env_var_collector()
            result = collector.get_router_metrics()
            r_m = f'self.collector: {self.collector} got result: {result}'
            log.debug(r_m)
            return final_response

    @Metrics.COLLECTOR_METRICS_UPDATE_ROUTE_TIME.time()
    def handle_collector_metrics_update_route_response(self):
        with Metrics.COLLECTOR_METRICS_UPDATE_ROUTE_EXCEPTIONS.count_exceptions():  # noqa: E501
            p_m = 'handle collector metrics update route'
            log.debug(p_m)
            final_response = self.base_response('metrics_update')
            for collector in self.collectors:
                result = collector.update_router_metrics()
                r_m = f'self.collector: {self.collector} got result: {result}'
                log.debug(r_m)
            return final_response
