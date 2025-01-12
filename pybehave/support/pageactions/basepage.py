"""
Base class for any common page interactions.
"""

import logging
from typing import List

from pybehave.support.core.elementaction import ElementAction
from pybehave.support.locators.locator import Locator
from pybehave.support.pageactions.actionenum import Action
from pybehave.utils.assertutils import Assert


class BasePage:
    """
        All page classes must extend this class in order to use the core webdri=
    ver actions
    """

    def __init__(self, context):
        self.context = context
        self.element_action = ElementAction(context)

    def click_on(
        self,
        locator: Locator,
        replacement=None,
        click_using_java_script=False,
        delay=0.5,
    ):
        """Click on locator"""
        self.element_action.click(
            locator.get_formatted_locator(),
            replacement=replacement,
            click_using_java_script=click_using_java_script,
            delay=delay,
        )

    def element_present_and_click(self, locator, retry_refresh_browser=False, delay=0.5, timeout=None):
        """Checks if element is present before clicking"""
        if self.element_action.is_element_present(
            locator, retry_refresh_browser=retry_refresh_browser, timeout=timeout
        ):
            self.element_action.click(locator, delay=delay)

    def element_displayed_and_click(self, locator, retry_refresh_browser=False, delay=0.5, timeout=None):
        """Checks if element is displayed then clicks element"""
        if self.element_action.is_element_displayed(
            locator, retry_refresh_browser=retry_refresh_browser, timeout=timeout
        ):
            if not self.element_action.is_element_clickable(locator):
                self.element_action.refresh_browser()
            self.element_action.click(locator, delay=delay, click_using_java_script=True)
        else:
            logging.warning("Element is not displayed '%s'", locator)

    def is_element_displayed(
        self,
        locator: Locator,
        replacement=None,
        timeout=None,
        retry_refresh_browser=False,
    ):
        """Check that element is displayed"""
        isDisplayed = self.element_action.is_element_displayed(
            locator.get_formatted_locator(),
            replacement=replacement,
            timeout=timeout,
            retry_refresh_browser=retry_refresh_browser,
        )
        logging.debug(
            "isDisplayed %s for locator [%s]",
            isDisplayed,
            locator.get_formatted_locator(replacement=replacement),
        )
        return isDisplayed

    def is_element_present(
        self,
        locator: Locator,
        replacement=None,
        timeout=None,
        retry_refresh_browser=False,
    ):
        """Check that element is present"""
        return self.element_action.is_element_present(
            locator.get_formatted_locator(),
            replacement=replacement,
            timeout=timeout,
            retry_refresh_browser=retry_refresh_browser,
        )

    def type_in_locator(
        self,
        locator: Locator,
        text: str,
        delay: float = 0.5,
        sensitive=False,
    ):
        """Type in locator"""
        if sensitive:
            logging.debug("Typing in locator %s text *****", locator.get_formatted_locator())
        else:
            logging.debug("Typing in locator %s text %s", locator.get_formatted_locator(), text)
        self.assert_element_displayed_and_click(locator)
        self.element_action.type(locator.get_formatted_locator(), text=text, delay=delay, sensitive=sensitive)

    def type_using_action_chains(self, locator: Locator, text, delay: float = 0.5):
        """Type into locator using action chains"""
        logging.debug("Typing using action chains for locator %s", locator.get_formatted_locator())
        self.element_action.type_using_actionschains(locator.get_formatted_locator(), text=text, delay=delay)

    def user_action_on_element(
        self,
        locator: Locator,
        action: Action,
        replacement=None,
        delay=0.5,
        timeout: int = None,
    ):
        """User action on a particular element"""
        logging.info(
            "Action: [%s] on locator: %s",
            action.name,
            locator.get_formatted_locator(replacement=replacement),
        )
        locatorString = locator.get_formatted_locator(replacement=replacement)
        if action == Action.TAB_ON:
            self.element_action.user_tab_on_element(locatorString, delay=delay, replacement=replacement)
        elif action == Action.COPY:
            self.element_action.user_copy_text_from_element(locatorString)
        elif action == Action.PASTE:
            self.element_action.user_paste_text_from_element(locatorString)
        elif action == Action.RIGHT_CLICK:
            self.element_action.right_click_on_element(locatorString, delay=delay)
        elif action == Action.DELETE_TEXT:
            self.element_action.user_deletes_text_from_element(locatorString)
        elif action == Action.ENTER_KEY:
            self.element_action.user_enter_on_element(locatorString, delay=delay)
        elif action == Action.CLICK:
            self.element_action.click(locatorString, delay=delay)
        elif action == Action.JAVASCRIPT_CLICK:
            self.element_action.click(
                locatorString,
                delay=delay,
                click_using_java_script=True,
                timeout=timeout,
            )
        elif action == Action.DOUBLE_CLICK:
            self.element_action.double_click(locatorString)
        else:
            Assert.assert_fail("Unhandled Action or Action not supplied")

    def locator_error(self, locator: Locator, replacement=None):
        """Given a locator will format an appropriate error message"""
        return (
            locator.name
            + ": "
            + locator.get_strategy().value
            + ", "
            + locator.get_locator(replacement=replacement)
            + " [Locator Not Found] "
        )

    def assert_are_elements_present(self, locators: List[Locator], retry_refresh_browser=False):
        """Iterates over collection of locators to determine if present"""
        for locator in locators:
            self.assert_is_element_present(locator, retry_refresh_browser=retry_refresh_browser)

    def assert_is_element_present(
        self,
        locator: Locator,
        error: str = None,
        retry_refresh_browser=False,
        timeout=None,
        replacement=None,
    ):
        """Asserts whether an element is present"""
        logging.debug(
            "Asserting element is present for locator %s",
            locator.get_formatted_locator(),
        )
        if error is None:
            error = self.locator_error(locator=locator, replacement=replacement)
        Assert.assert_true(
            self.element_action.is_element_present(
                locator.get_formatted_locator(),
                retry_refresh_browser=retry_refresh_browser,
                timeout=timeout,
                replacement=replacement,
            ),
            error,
        )

    def assert_elements_not_present(self, locators: List[Locator], retry_refresh_browser=False):
        """Asserts if elements are not present"""
        for locator in locators:
            self.assert_element_not_present(locator, retry_refresh_browser=retry_refresh_browser)

    def assert_element_not_present(self, locator: Locator, error: str = None, retry_refresh_browser=False):
        """Asserts if an element is not present"""
        logging.debug(
            "Asserting element not present with locator %s",
            locator.get_formatted_locator(),
        )
        if error is None:
            error = self.locator_error(locator)
        Assert.assert_false(
            self.element_action.is_element_present(
                locator.get_formatted_locator(),
                retry_refresh_browser=retry_refresh_browser,
            ),
            error,
        )

    def assert_elements_displayed(self, locators: List[Locator], retry_refresh_browser=False, timeout=None):
        """Iterates over collection of locators to determine if displayed"""
        for locator in locators:
            self.assert_is_element_displayed(locator, retry_refresh_browser=retry_refresh_browser, timeout=timeout)

    def assert_is_element_displayed(
        self,
        locator: Locator,
        error: str = None,
        retry_refresh_browser=False,
        replacement=None,
        timeout=None,
    ):
        """Asserts if an element is visible/displayed"""
        logging.debug("Asserting element displayed %s", locator.get_formatted_locator())
        if error is None:
            error = self.locator_error(locator=locator, replacement=replacement)
        Assert.assert_true(
            self.element_action.is_element_displayed(
                locator.get_formatted_locator(),
                retry_refresh_browser=retry_refresh_browser,
                replacement=replacement,
                timeout=timeout,
            ),
            error,
        )

    def assert_is_element_not_displayed(
        self,
        locator: Locator,
        error: str = None,
        retry_refresh_browser=False,
        replacement=None,
        timeout=1,
    ):
        """Asserts if an element is not visible/displayed"""
        logging.debug("Asserting element is not displayed %s", locator.get_formatted_locator())
        if error is None:
            error = self.locator_error(locator=locator, replacement=replacement)
        Assert.assert_false(
            self.element_action.is_element_displayed(
                locator.get_formatted_locator(),
                retry_refresh_browser=retry_refresh_browser,
                replacement=replacement,
                timeout=timeout,
            ),
            error,
        )

    def is_element_clickable(self, locator: Locator):
        """Checks if the element is clickable"""
        return self.element_action.is_element_clickable(locator.get_formatted_locator())

    def assert_elements_are_clickable(self, locators: List[Locator]):
        """Iterates over collection of locators and fails if any not clickable"""
        for locator in locators:
            self.assert_is_element_clickable(locator)

    def assert_is_element_clickable(self, locator: Locator):
        """Asserts that element is clickable"""
        Assert.assert_true(
            self.is_element_clickable(locator),
            f"Unable to click on {locator.get_formatted_locator()}",
        )

    def assert_element_displayed_and_click(
        self,
        locator: Locator,
        retry_refresh_browser=False,
        delay=0.5,
        timeout=None,
        replacement=None,
    ):
        """Checks element is displayed before clicking"""
        self.assert_is_element_displayed(
            locator,
            retry_refresh_browser=retry_refresh_browser,
            timeout=timeout,
            replacement=replacement,
        )
        if not self.element_action.is_element_clickable(locator.get_formatted_locator(replacement=replacement)):
            self.element_action.refresh_browser()
        self.click_on(locator, delay=delay, click_using_java_script=True, replacement=replacement)

    def assert_element_present_and_click(self, locator: Locator, retry_refresh_browser=False, delay=0.5, timeout=None):
        """Checks, via Assert, if element is present then clicks"""
        self.assert_is_element_present(locator, retry_refresh_browser=retry_refresh_browser, timeout=timeout)
        self.click_on(locator, delay=delay)

    def assert_element_contains_text(self, locator: Locator, expected_text: str):
        """Asserts whether the element contains the passed in text"""
        self.assert_is_element_displayed(locator)
        actual_text = self.element_action.get_text(locator.get_formatted_locator()).lower()
        Assert.assert_contains(
            actual_text,
            expected_text.lower(),
            f"{locator.name} did not contain {expected_text}",
        )

    def assert_element_not_contain_text(self, locator: Locator, expected_text: str):
        """Asserts whether an element does not contain text"""
        self.assert_is_element_displayed(locator)
        actual_text = self.element_action.get_text(locator.get_formatted_locator()).lower()
        Assert.assert_does_not_contain(
            actual_text,
            expected_text.lower(),
            f"{locator.name} did contain {expected_text}",
        )

    def get_element_text(self, locator: Locator, replacement=None):
        return self.element_action.get_text(locator.get_formatted_locator(), replacement=replacement)

    def assert_element_present_get_text(self, locator: Locator, replacement=None):
        """Asserts if element is present and returns text"""
        self.assert_is_element_present(locator, replacement=replacement)
        return self.element_action.get_text(locator.get_formatted_locator(replacement=replacement))

    def assert_element_text_equals(self, locator: Locator, text: str, equality: bool = True):
        """Asserts element is present and then asserts texts or do not match based on equality value passed"""
        actual_text = self.assert_element_present_get_text(locator).lower()
        logging.info(
            "Locator [%s] text equals for [%s]",
            locator.get_formatted_locator(),
            actual_text,
        )
        logging.debug(
            "Asserting [%s] that actual text [%s] equals expected text [%s]",
            equality,
            actual_text,
            text,
        )
        Assert.assert_equals(actual_text == text.lower(), equality, self.locator_error(locator))

    def assert_element_text_is_present(self, locator: Locator, text_to_check: str, timeout=None):
        """Asserts element has text present"""
        is_text_present = self.element_action.is_text_present(locator.get_formatted_locator(), text_to_check, timeout)
        Assert.assert_true(
            is_text_present,
            f"Text {text_to_check} is not present in locator {locator.get_formatted_locator()}",
        )

    def assert_present_and_type(self, locator: Locator, text: str, delay=0.5):
        """Assert whether element is present then type in text"""
        self.assert_is_element_present(locator)
        self.element_action.type(locator.get_formatted_locator(), text, delay=delay)

    def close_any_other_tabs(self):
        """closes other tabs"""
        logging.info("Closing any other tabs")
        self.element_action.close_other_tabs()

    def retry_until_element_displayed(self, locator: Locator, timeout=0.5, max_count=2, replacement=None):
        """Retry until the element is displayed"""
        return self.element_action.retry_until_displayed(
            locator.get_formatted_locator(),
            timeout=timeout,
            max_count=max_count,
            replacement=replacement,
        )

    def type_using_loop(self, locator: Locator, text: str, delay=1.0):
        """Type text char by char in a loop to control typing speed"""
        self.element_action.type_using_loop(locator.get_formatted_locator(), text=text, delay=delay)

    def assert_contains_all_text(self, locator: Locator, texts: List[str]):
        """Asserts whether all the text passed in the list
        is contained within the locator content text"""
        if isinstance(texts, str):
            raise TypeError("texts param not a list")
        body_text = self.element_action.get_text(locator.get_formatted_locator()).lower()
        for text in texts:
            Assert.assert_contains(
                body_text,
                text.lower(),
                f"{locator.name} does not contain {text}",
            )

    def checkbox_status_to(self, locator: Locator, checked: bool):
        """sets a checkbox to the value provided"""
        logging.info("Set checkbox %s to status %s", locator, checked)
        checkbox = self.element_action.fetch_element(locator.get_formatted_locator())
        if checkbox.get_attribute("value") != checked:
            self.element_action.execute_java_script("arguments[0].click();", checkbox)

    def fetch_element(
        self,
        locator: Locator,
        is_list_of_elements=False,
        timeout=None,
        retry_refresh_browser=False,
        replacement=None,
    ):
        """returns the element identified by the locator"""
        # not element_action.fetch_element has named element_timeout
        return self.element_action.fetch_element(
            locator.get_formatted_locator(replacement=replacement),
            is_list_of_elements=is_list_of_elements,
            element_timeout=timeout,
            retry_refresh_browser=retry_refresh_browser,
        )

    def click_element(self, element, delay=0.5):
        """performs click action on the given element"""
        self.element_action.click_element(element, delay=delay)

    def clear_modal_if_displayed(self, locator, timeout):
        """performs click action on the given element"""
        self.element_action.clear_modal_if_displayed(locator, timeout)

    def switch_to_default_content(self, assert_it=True, delay=0.5):
        """Switch to parent window"""
        self.element_action.switch_to_default_content(assert_it=assert_it, delay=delay)

    def switch_to_indexed_window(self, index):
        """Switch to indexed window"""
        self.element_action.switch_to_indexed_window(index=index)

    def refresh_browser(self):
        """Refresh of the browser"""
        self.element_action.refresh_browser()

    def close_other_tabs(self, delay=0.5):
        """closes other open tabs"""
        self.element_action.close_other_tabs(delay=delay)

    def window_count(self, delay=0.5):
        """Count the number of open windows"""
        return self.element_action.window_count(delay=delay)

    def switch_to_new_window(self, count=0, expected_window_url=None, validate_url=False, delay=0.5):
        """Switch to new window"""
        return self.element_action.switch_to_new_window(
            count=count,
            expected_window_url=expected_window_url,
            validate_url=validate_url,
            delay=delay,
        )

    def until_element_displayed(self, locator: Locator, iterator=30, wait=1, replacement=None):
        """Repeats the step to check if element is
        displayed while a page is rendering"""
        return self.element_action.until_element_displayed(
            locator.get_formatted_locator(replacement=replacement),
            iterator=iterator,
            wait=wait,
        )

    def go_to(self, app):
        """goes to app"""
        self.element_action.go_to(app)

    def get_element_count(self, locator: Locator, replacement=None):
        """Get number of elements"""
        return self.element_action.get_element_count(locator.get_formatted_locator(replacement=replacement))

    def drag_and_drop_with_offset_to_the_left(self, locator: Locator, xoffset):
        """user performs drag and drop with offset to the left"""
        return self.element_action.drag_and_drop_with_offset_to_the_left(locator.get_formatted_locator(), xoffset)

    def drag_and_drop_with_offset_to_the_right(self, locator: Locator, xoffset):
        """user performs drag and drop with offset to the right"""
        return self.element_action.drag_and_drop_with_offset_to_the_right(locator.get_formatted_locator(), xoffset)

    def is_text_present(self, locator: Locator, text: str, timeout=None):
        return self.element_action.is_text_present(locator=locator.get_formatted_locator(), text=text, timeout=timeout)

    def upload(self, locator: Locator, text):
        """upload file"""
        self.element_action.upload(locator.get_formatted_locator(), text)

    def javascript_click(self, locator: Locator, replacement=None):
        element = self.fetch_element(locator, replacement=replacement)
        self.element_action.execute_java_script("arguments[0].click();", element)

    def find_current_url(self):
        """Find current URL"""
        return self.element_action.find_current_url()

    def user_deletes_text_from_element(self, locator):
        """user performs ctl+a and delete keystroke"""
        return self.element_action.user_deletes_text_from_element(locator)
