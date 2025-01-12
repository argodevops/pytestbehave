"""Provides locators enum for the example login page"""

from pybehave.support.locators.locator import Locator
from pybehave.support.locators.locatortype import LocatorType


class LoginLocator(Locator):
    """
    Locators for the Example Login Page.
    """

    USERNAME = (LocatorType.XPATH, "//input[@id='username']")
    PASSWORD = (LocatorType.XPATH, "//input[@id='password']")
    LOGIN_BUTTON = (LocatorType.XPATH, "//a[@id='log-in']")
    LOGOUT_BUTTON = (LocatorType.XPATH, "//a[@id='log-out']")
    LOGGED_IN_USER = (LocatorType.XPATH, "//div[@class='logged-user-w']")
    HEADER_H6 = (LocatorType.XPATH, "//h6[@class='element-header']")
