"""
Step definitions for function apps API calls
"""

# pylint: skip-file

from behave import step
from pybehave.support.facades.example.apiaction import TokenApiAction


@step("I have a valid rest token")
def generate_valid_rest_api_token(context):
    """generate a valid rest api token"""
    context.scenario.api_action = TokenApiAction(context)
    context.scenario.api_action.generate_valid_rest_api_token()


@step('I call the api "{url}"')
def call_rest_api(context, url):
    """call the rest api"""
    context.scenario.api_action = TokenApiAction(context)
    context.scenario.api_action.call_rest_api(url)


@step("I have a valid access token for the REST endpoint api")
def generate_valid_access_token(context):
    """generate a valid rest api token"""
    context.scenario.api_action = TokenApiAction(context)
    context.scenario.api_action.generate_valid_access_token()


@step("I make a post call with the access token")
def post_request_with_access_token(context):
    """make a post call with access token"""
    context.scenario.api_action = TokenApiAction(context)
    context.scenario.api_action.post_request_with_access_token()


@step("I receive a valid OAuth 2.0 token")
def verify_token(context):
    """verify OAth token"""
    context.scenario.api_action = TokenApiAction(context)
    context.scenario.api_action.verify_oauth2_token()


@step('I receive a "{response}" response')
def verify_response(context, response):
    """verify the api response"""
    context.scenario.api_action = TokenApiAction(context)
    context.scenario.api_action.verify_response(response)


@step('I trigger the Azure function "{app_function_name}"')
def trigger_function_app(context, app_function_name):
    """Triggger a call to Azure Funtion"""
    context.scenario.api_action = TokenApiAction(context)
    context.scenario.api_action.trigger_function_app(app_function_name)
