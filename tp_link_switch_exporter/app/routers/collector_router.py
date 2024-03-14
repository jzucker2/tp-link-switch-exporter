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
    def _create_collector(cls, ip, name, username, password):
        return Collector.get_collector(
            switch_ip=ip,
            switch_username=username,
            switch_password=password,
            switch_name=name)

    @classmethod
    def _create_env_var_collector(cls):
        switch_name = EnvVars.get_default_switch_name()
        switch_ip = EnvVars.get_default_switch_ip()
        switch_username = EnvVars.get_default_switch_username()
        switch_password = EnvVars.get_default_switch_password()
        return cls._create_collector(
            switch_ip,
            switch_name,
            switch_username,
            switch_password)

    @classmethod
    def _create_collector_from_config(cls, switch_config):
        switch_name = switch_config[ConfigKeys.SWITCH_NAME.key_name]
        switch_ip = switch_config[ConfigKeys.SWITCH_IP.key_name]
        switch_username = switch_config[ConfigKeys.SWITCH_USERNAME.key_name]
        switch_password = switch_config[ConfigKeys.SWITCH_PASSWORD.key_name]
        collector = cls._create_collector(
            switch_ip,
            switch_name,
            switch_username,
            switch_password)
        return collector

    @classmethod
    def _has_switch_config_env_vars(cls):
        return EnvVars.has_switch_config_env_vars()

    @classmethod
    def should_use_config_file(cls):
        if cls._has_switch_config_env_vars():
            return False
        return True

    def _get_config_switches(self):
        config = self.config
        return ConfigParser.get_switches(config)

    def _create_collectors(self):
        collectors = []
        if self.should_use_config_file():
            log.debug('Using yml config file for switch configs')
            switches = self._get_config_switches()
            for switch_config in switches:
                collector = self._create_collector_from_config(switch_config)
                collectors.append(collector)
        else:
            log.debug('Using env vars for switch configs')
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
            result = collector.get_switch_metrics()
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
                result = collector.update_switch_metrics()
                r_m = f'self.collector: {self.collector} got result: {result}'
                log.debug(r_m)
            return final_response
