@smoketest
@dev

Feature: Example Login

  Scenario: Login to demo site
    Given I have navigated to url "https://demo.applitools.com"
    When I enter username "Operator" and password "Password"
    Then I can verify the items are present
      | item                |
      | Financial Overview  |
    And I logout

