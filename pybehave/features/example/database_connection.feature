@smoketest
@dev

Feature: Database Connectivity

  Scenario: Connect to Example database
    Given I have successfully logged onto the "Example" database as "dbuser" user
    When I query the database version
    Then I can verify the database version is "12"
