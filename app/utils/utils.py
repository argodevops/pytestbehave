"""
Utilities module
"""

import random
import re
import string
import uuid

from behave import register_type
from faker import Faker


class Utils:
    """
    Utility class
    """

    faker = Faker("en_GB")

    @staticmethod
    def is_valid(text):
        """function for validating string"""
        res = re.match(r"^[_A-Za-z]\w+$", text)
        return res

    @staticmethod
    def parse_number(text):
        """function for parsing string to integer"""
        return int(text)

    @staticmethod
    def random_choice():
        """return random 8 character string"""
        return "".join(random.choices(string.ascii_lowercase, k=8))

    @staticmethod
    def random_number():
        """return random 8 digit number"""
        return "".join(random.choices(string.digits, k=8))

    @staticmethod
    def truncated_uuid4():
        """return first 8 characters of uuid"""
        return str(uuid.uuid4())[:8]

    register_type(Number=parse_number)
