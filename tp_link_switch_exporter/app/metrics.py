from enum import Enum
from prometheus_flask_exporter.multiprocess import GunicornPrometheusMetrics
from prometheus_flask_exporter import Counter, Summary, Gauge


class Labels(Enum):
    DEVICE = 'device'
    SCRAPE_EVENT = 'scrape_event'
    SWITCH_NAME = 'switch_name'

    @classmethod
    def labels(cls):
        return list([
            cls.DEVICE.value,
        ])

    @classmethod
    def basic_switch_labels(cls):
        return list([
            cls.SWITCH_NAME.value,
        ])

    @classmethod
    def scrape_event_labels(cls):
        return list([
            cls.SWITCH_NAME.value,
            cls.SCRAPE_EVENT.value,
        ])


class Metrics(object):
    DEBUG_ROUTE_TIME = Summary(
        'tp_link_switch_exporter_debug_route_time',
        'Time spent to handle debug route request')

    DEBUG_ROUTE_EXCEPTIONS = Counter(
        'tp_link_switch_exporter_debug_route_exceptions',
        'Exceptions while attempting to handle debug route request')

    TP_LINK_SWITCH_TEST_TIME = Summary(
        'tp_link_switch_exporter_switch_test_time',
        'Time spent to get quick info from TP-Link switch')

    TP_LINK_SWITCH_TEST_EXCEPTIONS = Counter(
        'tp_link_switch_exporter_switch_test_exceptions',
        'Exceptions while attempting to get quick info from TP-Link switch')

    SIMPLE_COLLECTOR_ROUTE_TIME = Summary(
        'tp_link_switch_exporter_simple_collector_route_time',
        'Time spent to handle simple collector route request')

    SIMPLE_EXPORTER_ROUTE_EXCEPTIONS = Counter(
        'tp_link_switch_exporter_simple_collector_route_exceptions',
        'Exceptions while attempting to handle simple collector route request')

    COLLECTOR_METRICS_UPDATE_ROUTE_TIME = Summary(
        'tp_link_switch_exporter_collector_metrics_update_route_time',
        'Time spent to handle collector metrics update route request')

    COLLECTOR_METRICS_UPDATE_ROUTE_EXCEPTIONS = Counter(
        'tp_link_switch_exporter_collector_metrics_update_route_exceptions',
        'Exceptions while attempting collector metrics update route request')

    ROUTER_SCRAPE_EVENT_COLLECTOR_COUNTER = Counter(
        'tp_link_switch_exporter_scrape_event_collector_count',
        'The count of events related to scraping a switch by collector',
        Labels.scrape_event_labels()
    )

    # switch specific stats

    ROUTER_WIFI_CLIENTS_TOTAL = Gauge(
        'tp_link_switch_exporter_switch_wifi_clients_total',
        'Total number of Wi-Fi clients connected to this switch',
        Labels.basic_switch_labels())

    ROUTER_WIRED_CLIENTS_TOTAL = Gauge(
        'tp_link_switch_exporter_switch_wired_clients_total',
        'Total number of wired clients connected to this switch',
        Labels.basic_switch_labels())

    ROUTER_CLIENTS_TOTAL = Gauge(
        'tp_link_switch_exporter_switch_clients_total',
        'Total number of total clients connected to this switch',
        Labels.basic_switch_labels())

    ROUTER_MEMORY_USAGE = Gauge(
        'tp_link_switch_exporter_switch_memory_usage',
        'The memory usage of the switch',
        Labels.basic_switch_labels())

    ROUTER_CPU_USAGE = Gauge(
        'tp_link_switch_exporter_switch_cpu_usage',
        'The cpu usage of the switch',
        Labels.basic_switch_labels())


# https://github.com/rycus86/prometheus_flask_exporter#app-factory-pattern
# https://github.com/rycus86/prometheus_flask_exporter/blob/master/examples/gunicorn-app-factory/app_setup.py
def get_metrics_app_factory():
    return GunicornPrometheusMetrics.for_app_factory()


metrics = get_metrics_app_factory()
