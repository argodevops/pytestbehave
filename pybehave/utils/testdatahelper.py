"""
Helper for managing config
"""

import logging
import os

from pybehave.utils.assertutils import Assert
from pybehave.utils.configfilereader import ConfigFileReader


class TestDataHelper:
    """
    A helper class used for managing test config
    """

    def __init__(self, context):
        logging.info("Loading configuration from FILE")
        self.config = ConfigFileReader(context)
        self.context = context
        self.context.temp_folder_path = os.path.join(os.getcwd(), "temp_folder")

        if not os.path.exists(self.context.temp_folder_path):
            os.mkdir(self.context.temp_folder_path)
            logging.info("Created temporary folder %s", self.context.temp_folder_path)
        else:
            logging.info("Temporary folder already exists: %s", self.context.temp_folder_path)

    def get_environment(self):
        """return the environment"""
        return self.config.get_environment()

    def get_url(self):
        """return url"""
        return self.config.get_url()

    def get_credentials(self):
        """return credentials for user type"""
        return self.config.get_credentials()

    def get_db_details(self):
        """return the database details"""
        return self.config.get_db_details()

    def get_access_token(self):
        """return access token"""
        return self.config.get_access_token()

    def get_functionapps_url(self):
        """return the function apps url"""
        return self.config.get_functionapps_url()

    def get_functionapps_domain(self):
        """return the function domain"""
        return self.config.get_functionapps_domain()

    def get_servicebus_namespace(self):
        """return the servicebus namespace"""
        return self.config.get_servicebus_namespace()

    def get_sas_name(self):
        """return the sas name"""
        return self.config.get_sas_name()

    def get_sas_value(self):
        """return the sas value"""
        return self.config.get_sas_value()

    def get_topic(self):
        """return the integration topic"""
        return self.config.get_topic()

    def get_admin_username(self):
        """return the admin username"""
        return self.config.get_admin_username()

    def get_version(self):
        """return app version"""
        return self.config.get_version()

    def get_function_app(self, function_name):
        """return function app details"""
        Assert.assert_fail(f"The app function {function_name} is not defined ")
