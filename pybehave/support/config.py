"""
Manage settings and configuration.
"""

import json
import logging
import os


class Settings:
    """Simple singleton class for managing and accessing settings"""

    def __init__(self):
        settings_file = os.environ.get("SETTINGS_FILE_PATH")
        if not settings_file:
            settings_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test-settings.json")

        with open(settings_file, encoding="utf-8") as file:
            setting = json.load(file)

        self.test_runner = setting.get("test_runner", "GRID")
        self.browser = setting["browser"]
        self.browser_version = setting.get("browser_version", "131.0")
        self.browser_platform = setting.get("browser_platform", "linux")
        self.selenium_grid_endpoint = setting.get("selenium_grid_endpoint", None)
        self.driver_executable_path = setting.get("driver_executable_path", None)
        self.driver_timeout = int(setting["driver_timeout"])
        self.wait_time = setting["wait_time"]
        self.environment = setting["environment"]
        self.is_testdata_keyvault = setting["is_kv_config"]
        self.is_headless_browser = setting.get("is_headless_browser", False)

        logging.basicConfig(
            format="%(asctime)s %(levelname)-8s %(message)s",
            level=logging.INFO,
            datefmt="%Y-%m-%d %H:%M:%S",
        )


settings = Settings()
