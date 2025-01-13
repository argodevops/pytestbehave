"""
Step definitions for database calls
"""

# pylint: skip-file

from behave import step, then, when
from pybehave.support.facades.example.databaseaction import DatabaseAction


@step('I have successfully logged onto the "{dbname}" database as "{dbuser}" user')
def login_to_database(context, dbname, dbuser):
    """login to the database with the given username"""
    context.scenario.database_action = DatabaseAction(context)
    db = {
        "server": "insert_server_name",
        "database": dbname,
        "username": dbuser,
        "password": "lookup_password",
    }
    context.scenario.database_action.login_with(db)


@when("I query the database version")
def query_database_version(context):
    """query the database version"""
    context.scenario.database_action = DatabaseAction(context)
    context.scenario.database_action.query_database_version()


@then('I can verify the database version is "{version}"')
def verify_database_version(context, version):
    """verify the database version"""
    context.scenario.database_action = DatabaseAction(context)
    context.scenario.database_action.verify_database_version(version)
