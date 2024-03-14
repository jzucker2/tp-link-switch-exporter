from tplinkrouterc6u import TplinkRouter
from flask import current_app as app
from .env_vars import EnvVars


log = app.logger


# https://github.com/AlexandrErohin/TP-Link-Archer-C6U


class TPLinkRouterException(Exception):
    pass


class TPLinkRouter(object):
    @classmethod
    def get_client(cls, **kwargs):
        return cls(**kwargs)

    @classmethod
    def get_default_router_ip(cls):
        return EnvVars.get_default_router_ip()

    @classmethod
    def get_default_router_username(cls):
        return EnvVars.get_default_router_username()

    @classmethod
    def get_default_router_password(cls):
        return EnvVars.get_default_router_password()

    def __init__(self, **kwargs):
        router_ip = kwargs.get(
            'router_ip',
            self.get_default_router_ip())
        self.router_ip = router_ip
        router_username = kwargs.get(
            'router_username',
            self.get_default_router_username())
        self.router_username = router_username
        router_password = kwargs.get(
            'router_password',
            self.get_default_router_password())
        self.router_password = router_password
        i_m = (f'creating client for router_ip: {router_ip}')
        log.debug(i_m)
        self._router = None

    @property
    def router(self):
        if self._router:
            return self._router
        self._router = TplinkRouter(
            self.router_ip,
            self.router_password)
        return self._router

    def authorize(self):
        self.router.authorize()

    def get_firmware(self):
        # Get firmware info - returns Firmware
        firmware = self.router.get_firmware()
        log.debug(f'router firmware: {firmware}')
        return firmware

    def get_status(self):
        # Get status info - returns Status
        status = self.router.get_status()
        log.debug(f'router status: {status}')
        return status

    def logout(self):
        self.router.logout()
