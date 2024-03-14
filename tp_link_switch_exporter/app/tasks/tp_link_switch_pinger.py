import os
from flask import current_app as app
from ..config import base_config


log = app.logger


class TPLinkSwitchPinger(object):
    # FIXME: doesn't work normally because of app context
    @classmethod
    def get_metrics_interval_seconds(cls):
        # METRICS_INTERVAL_SECONDS = int(
        #     app.config.get('METRICS_INTERVAL_SECONDS'))
        # return METRICS_INTERVAL_SECONDS
        default_interval = base_config.DEFAULT_METRICS_INTERVAL_SECONDS
        return os.environ.get('METRICS_INTERVAL_SECONDS', default_interval)

    @classmethod
    def should_schedule_switch_metrics_updates(cls):
        key = "SHOULD_SCHEDULE_SWITCH_METRICS_UPDATES"
        config_value = app.config.get(key)
        c_m = f'for {key} => {config_value}'
        log.debug(c_m)
        return bool(str(config_value) == "1")
