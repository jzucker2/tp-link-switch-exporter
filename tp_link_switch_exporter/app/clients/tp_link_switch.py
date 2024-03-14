from flask import current_app as app
from .env_vars import EnvVars


log = app.logger


# https://github.com/AlexandrErohin/TP-Link-Archer-C6U


class TPLinkSwitchException(Exception):
    pass


class TPLinkSwitch(object):
    @classmethod
    def get_client(cls, **kwargs):
        return cls(**kwargs)

    @classmethod
    def get_default_switch_ip(cls):
        return EnvVars.get_default_switch_ip()

    @classmethod
    def get_default_switch_username(cls):
        return EnvVars.get_default_switch_username()

    @classmethod
    def get_default_switch_password(cls):
        return EnvVars.get_default_switch_password()

    def __init__(self, **kwargs):
        switch_ip = kwargs.get(
            'switch_ip',
            self.get_default_switch_ip())
        self.switch_ip = switch_ip
        switch_username = kwargs.get(
            'switch_username',
            self.get_default_switch_username())
        self.switch_username = switch_username
        switch_password = kwargs.get(
            'switch_password',
            self.get_default_switch_password())
        self.switch_password = switch_password
        i_m = (f'creating client for switch_ip: {switch_ip}')
        log.debug(i_m)
        self._switch = None

    @property
    def switch(self):
        # FIXME: this needs to be actually implemented
        # if not self._switch:
        #     switch = self._switch
        # # self._switch = Tplinkswitch(
        # #     self.switch_ip,
        # #     self.switch_password)
        return self._switch
