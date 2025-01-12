"""
Settings file configuration reader class
"""

import json
import logging

from pybehave.utils.baseconfigreader import BaseConfigReader


class ConfigFileReader(BaseConfigReader):
    """
    File based config reader
    """

    def __init__(self, context):
        if context.test_settings.is_kv_config:
            self.config = json.loads(context.test_settings.config_file)
        else:
            with open(context.test_settings.config_file, encoding="utf-8") as file:
                self.config = json.load(file)

        logging.info("Loaded configuration from FILE %s", file)

    def get_environment(self):
        """returns the environment"""
        return self.config["environment"]

    def get_url(self):
        """returns the application url"""
        return self.config["url"]

    def get_credentials(self, usertype):
        """returns a user's credentials"""
        username = usertype[0]
        password = usertype[1]
        return {
            "username": username,
            "password": self.config[password],
        }

    def get_db_details(self):
        """returns the database details"""
        return {
            "server": self.config["database_server"],
            "database": self.config["database_name"],
            "username": self.config["database_username"],
            "password": self.config["database_password"],
        }

    def get_access_token(self):
        return {
            "api_url": self.config["rest_api_token_url"],
            "api_key": self.config["rest_api_token_key"],
        }

    def get_functionapps_url(self):
        """return the function apps url"""
        return "https://" + self.config["functionapps_dns_name"] + ":8443"

    def get_functionapps_domain(self):
        """return the function apps domain"""
        return self.config["functionapps_domain"]

    def get_resource_group(self):
        """return the resource group"""
        return self.config["resource_group"]

    def get_servicebus_namespace(self):
        """return the servicebus namespace"""
        return self.config["servicebus_namespace"]

    def get_topic(self):
        """return the integration topic"""
        return self.config["topic"]

    def get_sas_name(self):
        """return the sas name"""
        return self.config["sas_name"]

    def get_sas_value(self):
        """return the sas value"""
        return self.config["sas_value"]

    def get_version(self):
        """return app version"""
        return self.config["version"]
