import requests
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
    def get_default_switch_port(cls):
        return EnvVars.get_default_switch_port()

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
        switch_port = int(kwargs.get(
            'switch_port',
            self.get_default_switch_port()))
        self.switch_port = switch_port
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
        self.base_url = f"http://{self.switch_ip}:{self.switch_port}"
        self._switch = None
        self.loggedin = False
        self._session = requests.Session()

    @property
    def session(self):
        return self._session

    def _get_login_body(self):
        return dict({
            "logon": "Login",
            "username": self.switch_username,
            "password": self.switch_password,
        })

    def _get_login_headers(self):
        return dict({
            'Referer': f"{self.base_url}/Logout.htm",
        })

    def _get_login_url(self):
        return f"{self.base_url}/logon.cgi"

    def login(self):
        data = self._get_login_body()
        headers = self._get_login_headers()
        try:
            r = self.session.post(self._get_login_url(),
                                  data=data,
                                  headers=headers,
                                  timeout=5)
            log.debug("Logged in:" + r.text)
            self.loggedin = True
            return True
        except requests.exceptions.Timeout as errt:
            t_m = (f"Timeout on login for "
                   f"{self.switch_username}@{self.switch_ip}: {errt}")
            log.error(t_m)
            self.loggedin = False
            return False
        except requests.exceptions.RequestException as err:
            e_m = f"Error on login for {self.switch_username}@{self.switch_ip}: {err}"
            log.error(e_m)
            self.loggedin = False
            return False

    @property
    def switch(self):
        # FIXME: this needs to be actually implemented
        # if not self._switch:
        #     switch = self._switch
        # # self._switch = Tplinkswitch(
        # #     self.switch_ip,
        # #     self.switch_password)
        return self._switch
