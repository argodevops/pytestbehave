"""
Manage settings.
"""

import json
import logging
import os
from art import text2art

from pybehave.utils.assertutils import Assert
from pybehave.utils.keyvaultreader import KeyvaultReader


class Settings:
    """Class for reading the base settings from the test settings file"""

    def __init__(self):
        logging.basicConfig(
            format="%(asctime)s %(levelname)-8s %(message)s",
            level=logging.INFO,
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        settings_file = os.environ.get("SETTINGS_FILE_PATH")
        if not settings_file:
            settings_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test-settings.json")

        Art = text2art("PyBehave-Selenium")
        print(Art)

        logging.info("Settings file: %s", settings_file)

        with open(settings_file, encoding="utf-8") as file:
            setting = json.load(file)

        self.browser = setting.get("browser", "chrome")
        self.browser_version = setting.get("browser_version", "131.0")
        self.browser_platform = setting.get("browser_platform", "linux")
        self.driver_executable_path = setting.get("driver_executable_path", "drivers/chromedriver")
        self.driver_timeout = int(setting.get("driver_timeout", "5"))
        self.wait_time = setting.get("wait_time", "30")
        self.autoretry_attempts = setting.get("autoretry_attempts", "1")
        self.is_kv_config = setting.get("is_kv_config", False)
        self.env = setting.get("environment", "dev")
        self.config_file = self.get_env_config(self.env)
        self.is_headless_browser = setting.get("is_headless_browser", False)
        logging.info("Test config setting is successfully loaded")

    def get_env_config(self, test_env):
        """get environment config file"""
        logging.info("Use KeyVault test config" if self.is_kv_config else "Use local test config")
        if self.is_kv_config:
            config = os.environ.get("CONFIG")
            if not config:
                logging.info("Getting config from keyvault for %s environment", test_env)
                kv_client = KeyvaultReader().get_keyvault_client("https://vault.azure.net/")
                keys_list = [key.name for key in kv_client.list_properties_of_secrets()]

                if test_env.lower() in keys_list:
                    logging.info("Environment %s is recognised", test_env)
                    config = kv_client.get_secret(test_env.lower()).value
                else:
                    Assert.assert_fail(f"No matching config found for {test_env} environment")
            else:
                logging.info("Reading config from CONFIG env variable")
            return config
        else:
            config = os.environ.get("CONFIG")
            if config:
                logging.info("Getting config from %s file", config)
                return config
            else:
                logging.info("Getting config from default config file")
                return "./pybehave/configuration/default-config.json"


settings = Settings()
