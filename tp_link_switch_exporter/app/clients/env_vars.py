import os


ROUTER_IP = os.environ.get('TP_LINK_SWITCH_IP')
ROUTER_NAME = os.environ.get('TP_LINK_SWITCH_NAME', 'default')
ROUTER_USERNAME = os.environ.get('TP_LINK_SWITCH_USERNAME')
ROUTER_PASSWORD = os.environ.get('TP_LINK_SWITCH_PASSWORD')


class EnvVars(object):
    @classmethod
    def get_default_router_ip(cls):
        return ROUTER_IP

    @classmethod
    def get_default_router_name(cls):
        return ROUTER_NAME

    @classmethod
    def get_default_router_username(cls):
        return ROUTER_USERNAME

    @classmethod
    def get_default_router_password(cls):
        return ROUTER_PASSWORD

    @classmethod
    def has_router_config_env_vars(cls):
        router_ip = cls.get_default_router_ip()
        if not router_ip:
            return False
        router_password = cls.get_default_router_password()
        if not router_password:
            return False
        return True
