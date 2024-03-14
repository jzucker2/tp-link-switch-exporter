from enum import Enum


class ScrapeEvents(Enum):
    # FIXME: this needs to be updated to be relevant again
    AUTHORIZE = 'authorize'
    LOGOUT = 'logout'
    GET_FIRMWARE = 'get_firmware'
    GET_STATUS = 'get_status'
    ATTEMPT_GET_ROUTER_METRICS = 'attempt_get_router_metrics'
    SUCCESS = 'success'
    ERROR = 'error'
