import re
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
        self.ports = {}

    @property
    def mapping(self):
        """ This is a mapping of GUI status values to their meaning """
        return dict({
            '0': "down",
            '1': "auto",
            '2': "10/half",
            '3': "10/full",
            '4': "100/half",
            '5': "100/full",
            '6': "1000/full",
        })

    @property
    def session(self):
        return self._session

    def getPortStateMapping(self, state):
        if state in self.mapping:
            return self.mapping[state]
        else:
            return None

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
            e_m = (f"Error on login for "
                   f"{self.switch_username}@{self.switch_ip}: {err}")
            log.error(e_m)
            self.loggedin = False
            return False

    def _get_stats_url(self):
        return f"{self.base_url}/PortStatisticsRpm.htm"

    def _get_stats_headers(self):
        return dict({
            'Referer': f"{self.base_url}/",
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",  # noqa: E501
            'Upgrade-Insecure-Requests': "1",
        })

    def get_stats(self):
        """ The measurements are returned as a dictionary in this form:
                    stats[port][description]
                    stats[port][state]
                    stats[port][link_status]
                    stats[port][txGoodPkt]
                    stats[port][txBadPkt]
                    stats[port][rxGoodPkt]
                    stats[port][rxBadPkt]
                """
        stats = {}
        headers = self._get_stats_headers()
        try:
            r = self.session.get(self._get_stats_url(),
                                 headers=headers,
                                 timeout=5)
            log.debug("Received stats:" + r.text)

            # we're looking for something like this in the output:
            # state:[1,1,1,0,1,1,1,1,0,0],
            # link_status:[6,5,6,0,0,0,6,6,0,0],
            # pkts:[156660032,0,73463961,0,36934785,0,18955572,0,224590711,0,67687216,0,54497978,0,29301491,0,0,0,0,0,0,0,0,0,32241294,0,25417373,0,209448595,0,462006278,0,0,0]

            # state: 1 - Enabled, 0 - Disabled (administratively)
            # link_status: 0 - down, 1 - auto, 2 - 10Mbps half, 3 - 10Mbps full, 4 - 100Mbps half, 5 - 100Mbps full, 6 - 1Gbps full
            # pkts: every group of 4 values represent txGoodPkt, txBadPkt, rxGoodPkt, rxBadPkt

            stateMatch = re.search(r'state:\[([0-9,]+)\]', r.text)
            numberOfPorts = 0
            if stateMatch:
                state = stateMatch.group(1).split(",")
                # Note - that the last two entries in the json data do not
                # correspond to physical ports, so we'll skip them here...
                state = state[:-2]
                # populate the stats dictionary
                for p in range(1, len(state) + 1):
                    p = str(p)
                    if p not in stats:
                        stats[p] = {}
                        if p in self.ports:
                            stats[p]['description'] = self.ports[p]
                        else:
                            stats[p]['description'] = ""
                        stats[p]['state'] = state[int(p) - 1]
                        numberOfPorts += 1

            linkStatusMatch = re.search(r'link_status:\[([0-9,]+)\]', r.text)
            if linkStatusMatch:
                state = linkStatusMatch.group(1).split(",")
                # Note - that the last two entries in the json data
                # do not correspond to physical ports, so we'll
                # skip them here...
                state = state[:-2]
                # populate the stats dictionary
                for p in range(1, len(state) + 1):
                    p = str(p)
                    port_state = state[int(p) - 1]
                    stats[p]['link_status'] = self.getPortStateMapping(
                        port_state)

            pktsMatch = re.search(r'pkts:\[([0-9,]+)\]', r.text)
            if pktsMatch:
                pktData = pktsMatch.group(1).split(",")
                # Note - that the last two entries in the json data do not
                # correspond to physical ports, so we'll skip them here...
                pktData = pktData[:-2]

                # data in the array has 4 measurements for each port, in order
                for p in range(1, numberOfPorts + 1):
                    stats[str(p)]['txGoodPkt'] = pktData[(p - 1) * 4]
                    stats[str(p)]['txBadPkt'] = pktData[(p - 1) * 4 + 1]
                    stats[str(p)]['rxGoodPkt'] = pktData[(p - 1) * 4 + 2]
                    stats[str(p)]['rxBadPkt'] = pktData[(p - 1) * 4 + 3]

        except requests.exceptions.Timeout as errt:
            t_m = (f"Timeout on stats read for "
                   f"{self.switch_username}@{self.switch_ip}: {errt}")
            log.error(t_m)
            return stats
        except requests.exceptions.RequestException as err:
            e_m = (f"Error on stats read for "
                   f"{self.switch_username}@{self.switch_ip}: {err}")
            log.error(e_m)
            return stats
        return stats

    @property
    def switch(self):
        # FIXME: this needs to be actually implemented
        # if not self._switch:
        #     switch = self._switch
        # # self._switch = Tplinkswitch(
        # #     self.switch_ip,
        # #     self.switch_password)
        return self._switch
