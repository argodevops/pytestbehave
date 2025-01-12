"""
Step definitions for example login to application
"""

from behave import step
from pybehave.support.facades.example.loginaction import LoginAction


@step('I have navigated to url "{url}"')
def navigate_to_url(context, url):
    """navigate to url"""
    context.scenario.login_action = LoginAction(context)
    context.scenario.login_action.navigate_to(url)


@step('I enter username "{username}" and password "{password}"')
def login_with_credentials(context, username, password):
    """login with username and password credentials"""
    context.scenario.login_action = LoginAction(context)
    context.scenario.login_action.login_with(username, password)


@step("I can verify the items are present")
def verify_items(context):
    """verify items are present on page"""
    context.scenario.login_action = LoginAction(context)
    for row in context.table:
        context.scenario.login_action.verify_item_is_displayed(row["item"])


@step("I logout")
def logout(context):
    context.scenario.login_action.logout()
