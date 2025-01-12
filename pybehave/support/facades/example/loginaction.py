"""
Perform actions on users to support step definitions
"""

from pybehave.support.pageactions.example.loginpage import LoginPage


class LoginAction:
    """
    Action class to perform login actions
    """

    def __init__(self, context):
        self.context = context
        self.login_page = LoginPage(self.context)

    def navigate_to(self, app_url):
        """navigate to application url"""
        self.login_page.navigate_to(app_url)

    def login_with(self, username, password):
        """login with username and password"""
        self.login_page.login_with(username, password)

    def verify_item_is_displayed(self, item):
        self.login_page.verify_item_is_displayed(item)

    def logout(self):
        """logout"""
        self.login_page.logout()
