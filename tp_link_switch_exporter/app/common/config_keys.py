from enum import Enum


class ConfigKeys(Enum):
    SWITCHES = 'switches'
    SWITCH_NAME = 'switch_name'
    SWITCH_IP = 'switch_ip'
    SWITCH_PORT = 'switch_port'
    SWITCH_USERNAME = 'switch_username'
    SWITCH_PASSWORD = 'switch_password'

    @property
    def key_name(self):
        return self.value
