from enum import Enum


class ConfigKeys(Enum):
    ROUTERS = 'routers'
    ROUTER_NAME = 'router_name'
    ROUTER_IP = 'router_ip'
    ROUTER_PASSWORD = 'router_password'

    @property
    def key_name(self):
        return self.value
