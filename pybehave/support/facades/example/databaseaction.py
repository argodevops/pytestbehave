"""
Perform actions on the database to support step definitions
"""

import logging
import pyodbc

from pybehave.utils.assertutils import Assert


class DatabaseAction:
    """
    Action class to perform operations on the database
    """

    def __init__(self, context):
        self.context = context

    def login_with(self, details):
        """Login to the database"""
        server = details["server"]
        database_name = details["database"]
        username = details["username"]
        password = details["password"]
        database = {}
        logging.info("Login to %s:%s database with username %s", server, database_name, username)

        # ENCRYPT defaults to yes starting in ODBC Driver 18.
        # Good to always specify ENCRYPT=yes on the client side to avoid MITM attacks.

        database.update(
            conn=pyodbc.connect(
                "DRIVER={ODBC Driver 18 for SQL Server};SERVER=tcp:"
                + server
                + ";DATABASE="
                + database_name
                + ";ENCRYPT=yes;UID="
                + username
                + ";PWD="
                + password
            )
        )
        self.context.database = database

    def query_database_version(self):
        """Query the database version to check basic connectivity"""
        cursor = self.context.database.get("conn").cursor()
        cursor.execute("SELECT @@version;")
        row = cursor.fetchone()
        self.context.database.update(version=row[0])

    def verify_database_version(self, version):
        """Verify the database version"""
        actual_version = self.context.database.get("version")
        Assert.assert_true(
            version in actual_version,
            f"Unexpected database version, expected {version} to be found in {actual_version}",
        )
