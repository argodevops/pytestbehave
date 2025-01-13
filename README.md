## **PyBehave Selenium Test Automation Framework**

![GitHub actions workflow status](https://img.shields.io/github/actions/workflow/status/argodevops/pybehave-selenium-test-framework/main.yml)
![GitHub language count](https://img.shields.io/github/languages/count/argodevops/pybehave-selenium-test-framework)
![GitHub Downloads](https://img.shields.io/github/downloads/argodevops/pybehave-selenium-test-framework/total)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pybehave-selenium-test-framework)
![PyPI - License](https://img.shields.io/pypi/l/pybehave-selenium-test-framework)
![PyPI - Version](https://img.shields.io/pypi/v/pybehave-selenium-test-framework)

```
 ____          ____         _                                 ____         _               _
|  _ \  _   _ | __ )   ___ | |__    __ _ __   __  ___        / ___|   ___ | |  ___  _ __  (_) _   _  _ __ ___
| |_) || | | ||  _ \  / _ \| '_ \  / _` |\ \ / / / _ \ _____ \___ \  / _ \| | / _ \| '_ \ | || | | || '_ ` _ \
|  __/ | |_| || |_) ||  __/| | | || (_| | \ V / |  __/|_____| ___) ||  __/| ||  __/| | | || || |_| || | | | | |
|_|     \__, ||____/  \___||_| |_| \__,_|  \_/   \___|       |____/  \___||_| \___||_| |_||_| \__,_||_| |_| |_|
        |___/
```

**PyBehave-Selenium-Test-Framework** is a powerful test automation framework designed to provide a comprehensive solution for testing user interfaces and APIs. It leverages the power of `Behave` framework, `Python` programming language and `Selenium` `WebDriver` to allow the creation robust and maintainable automated tests.

### Highlights
1. **Behaviour-Driven Development (BDD) Support** - allows testers to write tests in a human-readable format using `Gherkin` syntax, making it easier to collaborate with stakeholders and ensure test coverage.

2. **UI and API Testing** - supports testing both UIs and APIs, using `Selenium` `WebDriver` to interact with web browsers and `Python` `requests` library to send API requests and validate responses.

3. **Robustness** - when user interfaces are not 100% reliable, sometimes laggy, rendering speed varies, the core test logic will identify if elements are not present or clickable, back-off and attempt to retry a configurable number of times, and even perform browser refreshes if configured, to ensure the best attempt to execute the behaviour is performed.

4. **Cross-browser Support** - compatible with various web browsers, including Chrome and Edge; allowing tests to run across multiple browsers ensuring application compatibility and consistent behaviour. Note: the version of the web driver used must be compatible with the browser version installed.

5. **Test Data Management** - supports data-driven testing, allowing tests to read test data from external `template` files and use `Jinja2` templating engine to substitute in test specific data.

6. **Test Reporting and Logging** - support generating `allure` and `behavex` test reports to provide insight into test failures, captures screenshots of test failures for analysis; outputs clear log messages for every test action to aid debugging and troubleshooting.

7. **Extensibility and Customisation** - designed to be extensible and provides a simple, but flexible design for further customisation and integration of further third-party libraries.

### Design Overview

The design is split into two sections - **Test Suite** and **Framework Layer**.

* Test Suite - where the Gherkin style features are written with supporting step definitions calling down to page actions which orchestrate the test behaviour. This is where most business behaviour will be developed, making use of the framework layer.
* Framework Layer - contains the common re-usable functionality which drives the browser, contains common libs, provides logging and reporting.

<img src="overview.png" alt="drawing" style="width:400px;"/>

### Directory Structure

| Directory / File | Description |
|-----------|-------------|
| **features** | The `Gherkin` style feature files for defining BDD tests |
| **features/steps** | The step definitions backing the `Gherkin` tests |
| **features/environment.py** | Default test environment, can be overridden and customised |
| **support/facades** | Test logic facade actions potentially interacting across one or more pages |
| **support/pageactions** | The specific page actions, inheriting common actions from the `BasePage` |
| **support/core** | The core `ElementAction` which performs all the lower level selenium functionality |
| **support/locators** | Locator descriptors and types used for identifying web elements |
| **support/builder** | The templating builders to create supporting test data |
| **support/test-settings.json** | Default test settings, can be overridden and customised |
| **drivers** | The web drivers for supported browsers |
| **reports** | The json files generated with Allure reports |
| **screenshots** | The screenshots taken from failed tests |
| **requirements.txt** | File containing all the Python package dependencies |

## **Running the Tests**

### Pre-requisites

Install the required system dependencies. `sudo apt-get install requirements.system`.

Install the required Python module dependencies. `sudo pip install -r requirements.txt`.

Install the latest stable version of the web drivers you wish to use in `drivers`.

### Running the Example Test

An example test `login.feature` has been created to demonstrate a simple working test. It provides a username and password to login to a website, verifies the login and attempts to log the user out.

`behave features/example/login.feature`

Note: A compatible web driver will need to be available in the `drivers` folder and configured in the `test-settings.json` file.

The example login highlights the test suite and framework layers - a user defined `Gherkin` test with backing test logic; interacting with the web browser through the framework `BasePage`.

    +---------------+     +---------------+     +----------------+     +--------------+    +------------------+
    | login.feature | <-> | loginsteps.py | <-> | loginaction.py | <-> | loginpage.py | -> | loginlocators.py |
    +---------------+     +---------------+     +----------------+     +--------------+    +------------------+
                                                                              |
                                                                       +-------------+     +------------------+     +-------------+
                                                                       | basepage.py | <-> | elementaction.py | <-> | Web Browser |
                                                                       +-------------+     +------------------+     +-------------+

There are also example tests for `database` connectivity and `API` requests.

### Logging Output

When running tests each step is logged in a format to assist with understanding the execution and with debugging issues.

```
Feature: Example Login # features/example/login.feature:4
2024-02-14 18:17:13 INFO     Scenario <Scenario "Login to demo site"> - starting
2024-02-14 18:17:13 INFO     Edge browser
2024-02-14 18:17:13 INFO     Web driver: drivers/msedgedriver

  Scenario: Login to demo site                                  # features/example/login.feature:6
    Given I have navigated to url "https://demo.applitools.com" # features/steps/example/login_steps.py:9 0.342s
    When I enter username "Operator" and password "Password"    # features/steps/example/login_steps.py:16
2024-02-14 18:17:20 INFO     Login user Operator - start
2024-02-14 18:17:20 INFO     Checking element '//input[@id='username']' (XPATH) is clickable
2024-02-14 18:17:20 INFO     Clicked on element 'XPATH, //input[@id='username']'
2024-02-14 18:17:22 INFO     Typed text Operator on element XPATH, //input[@id='username']
2024-02-14 18:17:22 INFO     Checking element '//input[@id='password']' (XPATH) is clickable
2024-02-14 18:17:22 INFO     Clicked on element 'XPATH, //input[@id='password']'
2024-02-14 18:17:24 INFO     Typed text ***** on element XPATH, //input[@id='password']
2024-02-14 18:17:24 INFO     Checking element '//a[@id='log-in']' (XPATH) is clickable
2024-02-14 18:17:24 INFO     Clicked on element 'XPATH, //a[@id='log-in']'
2024-02-14 18:17:25 INFO     Login user Operator - complete
2024-02-14 18:17:25 INFO     Repeat until locator 'XPATH, //div[@class='logged-user-w']' is displayed
2024-02-14 18:17:25 INFO     Locator 'XPATH, //div[@class='logged-user-w']' displayed
    Then I can verify the items are present                     # features/steps/example/login_steps.py:23 0.134s
      | item               | Get text returned Financial Overview for element XPATH, //h6[@class='element-header']
      | Financial Overview | Completed step <then "I can verify the items are present">
    And I logout                                                # features/steps/example/login_steps.py:31
2024-02-14 18:17:26 INFO     Checking element '//a[@id='log-out']' (XPATH) is clickable
2024-02-14 18:17:31 WARNING  Unable to click on element 'XPATH, //a[@id='log-out']'
2024-02-14 18:17:31 INFO     Pausing for 5 seconds
2024-02-14 18:17:36 INFO     Retry clicking on element 'XPATH, //a[@id='log-out']'
2024-02-14 18:17:41 WARNING  Unable to click on element 'XPATH, //a[@id='log-out']'
2024-02-14 18:17:42 INFO     Scenario <Scenario "Login to demo site"> - complete

1 feature passed, 0 failed, 0 skipped
1 scenario passed, 0 failed, 0 skipped
4 steps passed, 0 failed, 0 skipped, 0 undefined
Took 0m22.608s
```

## Pre-commit checks

Runs hooks on every commit to automatically point out issues in code. Run ` $ pre-commit install` to setup the git hook scripts

https://pre-commit.com/

### black

Black is the uncompromising Python code formatter. Run `black **/*.py`

https://pypi.org/project/black/

### pylint

Pylint is a static code analyser for Python. Run `pylint *.py`

https://pypi.org/project/pylint/

### Run example test without allure reporting
`behave features/example/login.feature`

### Run example test with allure reporting
`behave -f allure_behave.formatter:AllureFormatter -o reports/ features/example/login.feature`

## **Running the Tests from Docker**

Build the docker image: `docker build -t [IMAGE_NAME]:[IMAGE_TAG] .`

To execute tests in a docker container, run the following. `docker run -it -v /tmp/reports:/src/reports [IMAGE_NAME]:[IMAGE_TAG] behave features/example/login.feature`

### View Test Reports
To view Allure test reports, run the command: `allure serve /tmp/reports`.

Note: You will need to install Allure Report from https://allurereport.org/.

## Selenium Grid (currently not fully implemented)

Selenium Grid will be used with Azure Kubernetes Service (AKS) to auto-scale when running the tests. Using AKS and KEDA (Kubernetes Event-driven Autoscaling) will monitor the Selenium test queue and scale nodes accordingly.

<img src="selenium-grid-overview.png" alt="drawing" style="width:600px;"/>

### Running tests against Selenium Grid
To run tests against Selenium Grid you need to be able to access the Hub UI. At the moment this has to be done using Kubernetes port-forwarding but in the future can be updated to expose the hub via a load balancer. Run `kubectl -n selenium port-forward svc/selenium-hub 4444` to port forward the Hub to localhost:4444

To use Selenium Grid update the settings.json to use the 'GRID' test runner by setting the property `"test_runner": "GRID"`. Once this has been set, the tests will try and run against a remote browser. You'll also need to set `"selenium_grid_endpoint": "http://localhost:4444/wd/hub"` to tell it where the Hub is.

To run the tests, you can run the exact same commands as described in the previous section. This won't however make use of the multiple worker feature of Selenium Grid. To run the tests in parallel, run the below command.

## Future Feature Enhancements

- [ ] Support concurrent running against multiple browser types
- [ ] Selenium Grid
- [ ] Integration with Azure keyvault

## References

https://behave.readthedocs.io/en/stable/

https://www.selenium.dev/documentation/webdriver/

https://github.com/Azure-Samples/selenium-grid-aks-keda

https://allurereport.org/
