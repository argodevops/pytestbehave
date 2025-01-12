"""
Manages the environment config.
"""

import logging
import os
import shutil
from datetime import datetime

from behave.contrib.scenario_autoretry import patch_scenario_with_autoretry
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from pybehave.support.settings import settings
from pybehave.utils.testdatahelper import TestDataHelper

PRIMARY_DEV_ENV = "dev"
SECONDARY_DEV_ENVS = ["int1", "int2", "int3"]


def before_all(context):
    """runs before all tests and sets the settings"""
    context.test_settings = settings
    context.test_config = TestDataHelper(context)


def before_scenario(context, scenario):
    """define before scenario"""
    if context.test_settings.env not in scenario.effective_tags:
        if PRIMARY_DEV_ENV in scenario.effective_tags and context.test_settings.env in SECONDARY_DEV_ENVS:
            logging.info("Mapping primary development env to secondary envs")
        else:
            scenario.skip(
                f"Scenario {scenario} - skipping, test not defined for {context.test_settings.env} environment"
            )

    logging.info("Scenario %s - starting", scenario)

    if "api" not in context.tags and "database" not in context.tags:
        if settings.browser.lower() == "chrome":
            logging.info("Chrome browser")
            options = webdriver.ChromeOptions()
            options.add_argument("--no-sandbox")
            options.add_argument("--start-maximized")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--allow-running-insecure-content")
            options.add_argument("--ignore-certificate-errors")
            if settings.is_headless_browser:
                # https://www.selenium.dev/blog/2023/headless-is-going-away/
                logging.info("Chrome running in headless mode")
                options.add_argument("--headless=new")
            logging.info("Web driver: %s", settings.driver_executable_path)
            service = Service(settings.driver_executable_path)
            context.driver = webdriver.Chrome(service=service, options=options)
        elif settings.browser.lower() == "edge":
            logging.info("Edge browser")
            options = webdriver.EdgeOptions()
            options.add_argument("--no-sandbox")
            options.add_argument("--start-maximized")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--allow-running-insecure-content")
            options.add_argument("--ignore-certificate-errors")
            if settings.is_headless_browser:
                # https://www.selenium.dev/blog/2023/headless-is-going-away/
                logging.info("Edge running in headless mode")
                options.add_argument("--headless=new")
            logging.info("Web driver: %s", settings.driver_executable_path)
            service = Service(settings.driver_executable_path)
            context.driver = webdriver.Edge(service=service, options=options)
        else:
            logging.error("Browser %s is not supported", settings.browser)
            raise ValueError("Browser is not supported")


def after_scenario(context, scenario):
    """runs after scenario and quits the driver"""
    logging.info("Scenario %s - complete", scenario)
    if hasattr(context, "driver"):
        context.driver.quit()


def before_tag(context, tag):
    """runs before a section tagged with the given name"""
    if "auto" in tag.lower():
        logging.info("Executing %s", tag)
        # set the AUTO test reference in the context
        context.test_id = tag


def before_feature(context, feature):
    """runs before a feature"""
    for scenario in feature.scenarios:
        if "autoretry" in scenario.effective_tags:
            patch_scenario_with_autoretry(scenario, max_attempts=int(settings.autoretry_attempts))


def after_step(context, step):
    """save screenshot if step fails"""
    logging.info("Completed step %s", step)
    if hasattr(context, "driver"):
        if step.status == "failed":
            logging.info(step.status)
            if not hasattr(context, "test_id"):
                context.test_id = ""
            logging.info("Saving screenshot for failed test %s", context.test_id)
            step_name = step.name.replace(" ", "_").lower()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"{context.test_id}_{step_name}_{timestamp}.png"

            screenshot_dir = "screenshots"
            if not os.path.exists(screenshot_dir):
                os.makedirs(screenshot_dir)

            screenshot_path = os.path.join(screenshot_dir, file_name)
            if context.driver:
                context.driver.save_screenshot(screenshot_path)


def after_all(context):
    """runs after all tests have finished"""
    if os.path.exists(context.temp_folder_path):
        shutil.rmtree(context.temp_folder_path)
        logging.info("Temp folder deleted...")
