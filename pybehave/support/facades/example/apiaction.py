"""
Perform function apps API actions to support step definitions
"""

import logging

from pybehave.support.apiclientactions.apiclient import ApiClient
from pybehave.utils.assertutils import Assert


class TokenApiAction:
    """
    Action class to perform operations related to token calls
    """

    def __init__(self, context):
        self.context = context
        self.api_client = ApiClient(self.context)

    def generate_valid_rest_api_token(self):
        """generate valid rest api token"""
        token = self.api_client.get_valid_rest_api_token()
        Assert.assert_not_none(token, "Rest API token was not generated")

    def call_rest_api(self, url):
        """call the rest api"""
        response = self.api_client.call_rest_api(url)
        self.context.api_response = response

    def verify_response(self, response):
        """verify the response message"""
        Assert.assert_not_none(self.context.api_response, "Received empty response")
        logging.info("Expected response: %s", response)
        logging.info("Received response: %s", self.context.api_response)

    def generate_valid_access_token(self):
        """generate valid access token"""
        self.context.access_token = self.api_client.get_valid_access_token()
        logging.info("Access token: {self.context.access_token}")
        Assert.assert_none(self.context.access_token, "Access token was not generated")

    def post_request_with_access_token(self):
        """post a request using an access token"""
        self.context.oauth2_token = self.api_client.call_start_session_rest_api(self.context.access_token)

    def verify_oauth2_token(self):
        """verify an OAuth2 token was generated"""
        logging.info("OAuth2.0 token: {self.outh2_token}")
        Assert.assert_none(self.context.oauth2_token, "OAuth2.0 token was not generated")

    def trigger_function_app(self, function_app_name):
        """trigger function app"""
        function_app = self.context.test_config.get_function_app(function_app_name)
        logging.info("%s Function App details retrieved", function_app_name)
        self.api_client.trigger_azure_function(function_app)
