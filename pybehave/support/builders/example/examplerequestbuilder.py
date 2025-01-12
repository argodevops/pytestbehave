"""
Builders for XML messages
"""

import logging

from faker import Faker
from jinja2 import Environment, FileSystemLoader


class XMLMessageBuilder:
    """
    Builder for XML messages
    """

    def __init__(self, context):
        self.faker = Faker("en_GB")
        self.context = context
        self.environment = Environment(loader=FileSystemLoader("templates/"), autoescape=True)

    def header(self, auth_token):
        """builds request header for a message"""
        header = {
            "Authorization": auth_token,
            "Content-Type": "application/atom+xml;type=entry;charset=utf-8",
        }
        return header

    def create_body(self, unit_id):
        """builds request body for a message"""
        template = self.environment.get_template("example.xml.j2")

        xml = template.render(ActKey1=unit_id)

        logging.info("XML: %s", xml)
        return xml
