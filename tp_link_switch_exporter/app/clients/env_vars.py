import os


SWITCH_IP = os.environ.get('TP_LINK_SWITCH_IP')
SWITCH_NAME = os.environ.get('TP_LINK_SWITCH_NAME', 'default')
SWITCH_USERNAME = os.environ.get('TP_LINK_SWITCH_USERNAME')
SWITCH_PASSWORD = os.environ.get('TP_LINK_SWITCH_PASSWORD')


class EnvVars(object):
    @classmethod
    def get_default_switch_ip(cls):
        return SWITCH_IP

    @classmethod
    def get_default_switch_name(cls):
        return SWITCH_NAME

    @classmethod
    def get_default_switch_username(cls):
        return SWITCH_USERNAME

    @classmethod
    def get_default_switch_password(cls):
        return SWITCH_PASSWORD

    @classmethod
    def has_switch_config_env_vars(cls):
        switch_ip = cls.get_default_switch_ip()
        if not switch_ip:
            return False
        switch_password = cls.get_default_switch_password()
        if not switch_password:
            return False
        return True
