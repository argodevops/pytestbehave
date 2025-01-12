"""
Interacts with UI driver to interact with the login page
"""

import logging

from pybehave.support.locators.example.loginlocator import LoginLocator
from pybehave.support.pageactions.basepage import BasePage
from pybehave.utils.assertutils import Assert


class LoginPage(BasePage):
    """
    Action class to perform different example actions page
    Usage: page = LoginPage(context)
    """

    def navigate_to(self, app):
        """navigate to the application"""
        self.go_to(app)

    def enter_username_and_password(self, username, password):
        """enter username and password"""
        logging.info("Login user %s - start", username)
        self.assert_is_element_displayed(LoginLocator.USERNAME)
        self.type_in_locator(LoginLocator.USERNAME, username)
        self.assert_is_element_displayed(LoginLocator.PASSWORD)
        self.type_in_locator(LoginLocator.PASSWORD, password, sensitive=True)
        self.assert_element_displayed_and_click(LoginLocator.LOGIN_BUTTON)

    def login_with(self, username, password):
        """enter credentials to login"""
        self.enter_username_and_password(username, password)
        logging.info("Login user %s - complete", username)
        # Wait until `about` menu has been displayed, meaning the application has mostly loaded
        logged_in = self.until_element_displayed(LoginLocator.LOGGED_IN_USER)
        Assert.assert_true(logged_in, f"Failed to login as user '{username}'")

    def verify_item_is_displayed(self, item):
        """verify an item is displayed"""
        logging.info("Verifying %s item is displayed", item)
        self.assert_element_contains_text(LoginLocator.HEADER_H6, item)

    def logout(self):
        """Logout"""
        self.click_on(LoginLocator.LOGOUT_BUTTON)
