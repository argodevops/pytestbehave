"""
Base configuration reader class
"""

from abc import ABC, abstractmethod


class BaseConfigReader(ABC):
    """
    Abstract config reader class
    """

    @abstractmethod
    def get_environment(self):
        """returns the environment"""

    @abstractmethod
    def get_url(self):
        """returns the app url"""

    @abstractmethod
    def get_credentials(self, usertype):
        """return user credentials"""

    @abstractmethod
    def get_db_details(self, dbtype):
        """return the db details"""

    @abstractmethod
    def get_access_token(self):
        """return access token"""

    @abstractmethod
    def get_functionapps_url(self):
        """return the function apps url"""

    @abstractmethod
    def get_functionapps_domain(self):
        """return the function apps domain"""

    @abstractmethod
    def get_resource_group(self):
        """return the resource group"""

    @abstractmethod
    def get_servicebus_namespace(self):
        """return the servicebus namespace"""

    @abstractmethod
    def get_topic(self):
        """return the integration topic"""

    @abstractmethod
    def get_sas_name(self):
        """return the sas name"""

    @abstractmethod
    def get_sas_value(self):
        """return the sas value"""

    @abstractmethod
    def get_version(self):
        """return version"""
