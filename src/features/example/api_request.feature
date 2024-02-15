@smoketest
@dev

Feature: Example API Request

  Scenario: Call API Endpoint
    Given I call the api "https://official-joke-api.appspot.com/random_joke"
    Then I receive a "punchline" response