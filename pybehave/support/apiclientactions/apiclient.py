"""
Performs API client calls
"""

import base64
import hashlib
import hmac
import logging
import time
import urllib
import urllib.parse

import requests

from pybehave.support.config import settings
from pybehave.utils.testdatahelper import TestDataHelper


class ApiClient:
    """
    Api Action class to perform operations related to api
    """

    def __init__(self, context):
        self.testdata_helper = TestDataHelper(context)

    def get_valid_rest_api_token(self):
        """get valid rest api token"""
        token = self.testdata_helper.get_access_token()
        url = token["api_url"]
        key = token["api_key"]

        params = {"code": key}
        response = requests.get(url, params=params, verify=False, timeout=int(settings.wait_time))
        if response.status_code != 200:
            logging.warning("Request {url} returned response code: {response.status_code}")
        return response.text

    def call_rest_api(self, url):
        """call rest api"""
        response = requests.get(
            url,
            verify=False,
            timeout=int(settings.wait_time),
        )
        return response.json()

    def get_auth_token(self, sb_name, sas_name, sas_value, eh_name=""):
        """
        Returns an authorization token dictionary
        for making calls to Event Hubs REST API.
        """
        uri = urllib.parse.quote_plus("https://{}.servicebus.windows.net/{}".format(sb_name, eh_name))
        sas = sas_value.encode("utf-8")
        expiry = str(int(time.time() + 10000))
        string_to_sign = (uri + "\n" + expiry).encode("utf-8")
        signed_hmac_sha256 = hmac.HMAC(sas, string_to_sign, hashlib.sha256)
        signature = urllib.parse.quote(base64.b64encode(signed_hmac_sha256.digest()))
        return {
            "sb_name": sb_name,
            "eh_name": eh_name,
            "token": "SharedAccessSignature sr={}&sig={}&se={}&skn={}".format(uri, signature, expiry, sas_name),
        }
