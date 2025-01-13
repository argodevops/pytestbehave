"""
Element action class
"""

import getpass
import io
import logging
import os
import random
from time import sleep
from xmlrpc.client import boolean

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select, WebDriverWait

from pybehave.support.settings import settings
from pybehave.support.locators.locatortype import LocatorType
from pybehave.utils.assertutils import Assert


class ElementAction:
    """
    Action class to perform basic operations (click, type, select ...) on webpage elements
    """

    def __init__(self, context):
        """init function"""
        self.context = context

    def fetch_element(
        self,
        locator,
        is_list_of_elements=False,
        element_timeout=None,
        retry_refresh_browser=False,
    ):
        """Fetch the WebElement
        Find the web element based the specified locator. Before attempting to find the element,
        check if presence and visibility of it is found.
        :param locator: element locator
        :param is_list_of_elements: in case the locator returns multiple elements, set this to true
        :param element_timeout: By default webdriver will wait for the 'element_fetch_timeout' seconds defined in
        config file. It will be overridden if you specify a different timeout to this function
        :return: WebElement, raise exception in case no such element is found
        """
        strategy = locator.split(",")[0].strip()
        actual_locator = locator.replace(strategy + ",", "")

        if element_timeout is None:
            element_timeout = int(settings.wait_time)

        try:
            if strategy not in LocatorType:
                raise KeyError(
                    "Unsupported locator strategy - "
                    + strategy
                    + "! "
                    + "Supported locator strategies are 'XPATH', 'ID', 'NAME', "
                    "'CSS_SELECTOR', 'TAG_NAME', 'LINK_TEXT' and 'PARTIAL_LINK_TEXT'"
                )

            try:
                WebDriverWait(self.context.driver, element_timeout).until(
                    ec.visibility_of_element_located((getattr(By, strategy), actual_locator))
                )
            except (TimeoutException, StaleElementReferenceException):
                logging.debug(
                    "Timed out after %s seconds waiting for element %s to be present!",
                    str(element_timeout),
                    str(actual_locator),
                    exc_info=True,
                )

            if is_list_of_elements:
                return self.context.driver.find_elements(getattr(By, strategy), actual_locator)

            try:
                element = self.context.driver.find_element(getattr(By, strategy), actual_locator)
                return element
            except TypeError:
                return False

        except NoSuchElementException as ex:
            if retry_refresh_browser:
                try:
                    self.context.driver.refresh()
                    self.fetch_element(
                        locator,
                        is_list_of_elements,
                        element_timeout,
                        retry_refresh_browser=False,
                    )
                    return True
                except NoSuchElementException:
                    return False
            raise NoSuchElementException(
                "Unable to locate element on page: {'strategy': ' "
                + str(strategy)
                + "', 'locator': '"
                + str(actual_locator)
                + "'}"
            ) from ex

    def is_element_present(self, locator, replacement=None, timeout=None, retry_refresh_browser=False):
        """Verify if element is present on page
        :param locator: element locator
        :param replacement: if locator contains dynamic part, i.e. '$value',
        it will be replaced by replacement variable
        :param timeout: By default webdriver will wait for the 'element_fetch_timeout' seconds defined in
        config.yml, It will be overridden if you specify a different timeout to this function
        :return: Boolean value specifying if element is present!
        """
        if replacement is not None:
            locator = locator.replace("$value", str(replacement))
        try:
            self.fetch_element(locator, False, timeout, retry_refresh_browser)
            return True
        except NoSuchElementException:
            return False

    def scroll_down_javascript(self, locator, pixel=0):
        """Scrolls down javascript element"""
        try:
            self.execute_java_script(f"document.querySelector('{locator}').scrollTop={pixel}")
            logging.info("Scrolling on element '%s' using JavaScript", locator)
        except Exception:
            Assert.assert_fail(f"Unable to scroll on element with locator {locator}")

    def is_element_displayed(self, locator, replacement=None, timeout=None, retry_refresh_browser=False):
        """Verify if element is present on page
        :param locator: element locator
        :param replacement: if locator contains dynamic part, i.e. '$value',
        it will be replaced by replacement variable
        :param timeout: By default webdriver will wait for the 'element_fetch_timeout' seconds defined
        in config.yml. It will be overridden if you specify a different timeout to this function
        :return: Boolean value specifying if element is displayed
        """
        if replacement is not None:
            locator = locator.replace("$value", replacement)
        try:
            if not self.fetch_element(locator, False, timeout, retry_refresh_browser):
                logging.info("Unable to find element '%s'", locator)
                return False
            return self.fetch_element(locator, False, timeout, retry_refresh_browser).is_displayed()
        except Exception:
            return False

    def is_text_present(self, locator, text, timeout=None):
        """Verify is text is present on webpage
        :param locator: element locator
        :param text to search for in locator
        :param timeout: By default webdriver will wait for the 'element_fetch_timeout' seconds defined in config.yml.
         It will be overridden if you specify a different timeout to this function
        :return: Boolean value specifying if text is present
        """
        try:
            if timeout is None:
                timeout = int(settings.wait_time)

            if not self.fetch_element(locator, True, timeout):
                logging.info("Unable to find element '%s' to find text", locator)
                return False

            try:
                strategy = locator.split(",")[0].strip()
                actual_locator = locator.replace(strategy + ",", "")

                logging.info("Waiting for text '%s' to be present in '%s'", text, locator)
                WebDriverWait(self.context.driver, timeout).until(
                    ec.text_to_be_present_in_element((getattr(By, strategy), actual_locator), text)
                )
                logging.info("Found text '%s' present in '%s'", text, locator)
                return True
            except (TimeoutException, StaleElementReferenceException):
                logging.debug(
                    "Timed out after %s seconds waiting for text %s to be present!",
                    str(timeout),
                    text,
                    exc_info=True,
                )
        except Exception as ex:
            logging.error(
                "Unable to find presence of text '%s' on page. Error: %s",
                text,
                ex,
                exc_info=True,
            )
        logging.info("Failed to find text '%s' present in '%s'", text, locator)
        return False

    def is_element_checked(self, locator, replacement=None, timeout=None, retry_refresh_browser=False):
        """Verify is element is checked
        :param locator: element locator
        :param replacement: if locator contains dynamic part, i.e. '$value',
        it will be replaced by replacement variable
        :param timeout: By default webdriver will wait for the 'element_fetch_timeout' seconds defined in config.yml
         It will be overridden if you specify a different timeout to this function
        :return: Boolean value specifying if element is checked
        """
        if replacement is not None:
            locator = locator.replace("$value", replacement)

        try:
            is_element_checked = self.fetch_element(locator, False, timeout, retry_refresh_browser).is_selected()
            logging.info(
                "Checked status for element '%s' is '%s'",
                locator,
                str(is_element_checked),
            )
            return is_element_checked
        except Exception as ex:
            logging.error(
                "Unable to check checked status for element '%s'. Error: %s",
                locator,
                ex,
                exc_info=True,
            )
            return False

    def is_element_clickable(self, locator):
        """Verify is element is clickable
        :param locator: element locator
        :return: Boolean value specifying if element is clickable
        """
        try:
            strategy = locator.split(",")[0].strip()
            actual_locator = locator.replace(strategy + ",", "").strip()
            timeout = int(settings.wait_time)

            logging.info("Checking element '%s' (%s) is clickable", actual_locator, strategy)
            WebDriverWait(self.context.driver, timeout).until(
                ec.element_to_be_clickable((getattr(By, strategy), actual_locator))
            )
            return True
        except Exception as ex:
            logging.warning("Element is unclickable '%s'", locator)
            logging.debug(ex)
            return False

    def click_element(self, element, delay=0.5):
        """Click directly on element
        :param element: element to click
        :param delay: pause in seconds before and after click
        """
        try:
            sleep(delay)
            logging.info("Clicking on element '%s'", element.text)
            element.click()
            logging.info("Clicked on element '%s'", element.text)
            sleep(delay)
        except Exception as ex:
            logging.warning("Unable to click on element '%s'", element.text)
            logging.debug(ex)

    def click(
        self,
        locator,
        replacement=None,
        click_using_java_script=False,
        delay=0.5,
        timeout: int = None,
    ):
        """Click on element
        :param locator: locator on which to click
        :param replacement: if locator contains dynamic part, i.e. '$value',
        it will be replaced by replacement variable
        :param click_using_java_script: whether to click using java script
        :param delay: pause in seconds before and after click
        :return: None
        """
        sleep(delay)
        if replacement:
            locator = locator.replace("$value", replacement)

        try:
            strategy = locator.split(",")[0].strip()
            actual_locator = locator.replace(strategy + ",", "").strip()
            if timeout is None:
                timeout = int(settings.wait_time)

            logging.info("Checking element '%s' (%s) is clickable", actual_locator, strategy)
            WebDriverWait(self.context.driver, timeout).until(
                ec.element_to_be_clickable((getattr(By, strategy), actual_locator))
            )
            logging.info("Clicking on element '%s'", locator)
            element = self.fetch_element(locator)
            element.click()
            logging.info("Clicked on element '%s'", locator)
        except Exception as ex:
            logging.warning("Unable to click on element '%s'", locator)
            logging.debug(ex)
            try:
                logging.info("Pausing for %s seconds", timeout)
                sleep(timeout)
                logging.info("Retry clicking on element '%s'", locator)
                element = self.fetch_element(locator)
                element.click()
                logging.info("Retry clicked on element '%s'", locator)
            except Exception as reex:
                logging.warning("Unable to click on element '%s'", locator)
                logging.debug(reex)

            if click_using_java_script:
                try:
                    logging.info("Clicking on element '%s' using JavaScript", locator)
                    element = self.fetch_element(locator)
                    self.execute_java_script("arguments[0].click();", element)
                    logging.info("Clicked on element '%s' using JavaScript", locator)
                except Exception as ex1:
                    logging.warning("Unable to click on element '%s' using JavaScript", locator)
                    logging.debug(ex1)

                    try:
                        logging.info("Clicking on element '%s' using ActionChains", locator)
                        element = self.fetch_element(locator)
                        actions = ActionChains(self.context.driver)
                        actions.move_to_element(element)
                        actions.click(element)
                        actions.perform()
                        logging.info("Clicked on element '%s' using ActionChains", locator)
                    except Exception as ex2:
                        logging.warning(
                            "Unable to click on element '%s' using ActionChains",
                            locator,
                        )
                        logging.debug(ex2)
                        Assert.assert_fail("Unable to click on element '" + locator + "'")
        # Adding a small delay after a click increases test reliability
        sleep(delay)

    def upload(self, locator, text):
        """upload file"""
        self.fetch_element(locator).send_keys(text)

    def type(self, locator, text, delay: float = 0.2, sensitive: boolean = False):
        """Type text in locator
        :param locator: locator in which to type
        :param text: text to type
        :param delay: pause after typing text
        :return: None
        """
        try:
            element = self.fetch_element(locator)
            element.clear()
            element.send_keys(text)
            sleep(delay)

            if sensitive:
                logging.info("Typed text ***** on element %s", locator, exc_info=True)
            else:
                logging.info("Typed text %s on element %s", text, locator, exc_info=True)
        except Exception:
            logging.error("Unable to type text %s on element %s.", text, locator)
            Assert.assert_fail("Unable to type text '" + text + "' on element '" + locator + "'")

    def type_using_actionschains(self, locator, text, delay: float = 0.5):
        """Type text in locator
        :param locator: locator in which to type
        :param text: text to type
        :param delay: pause before typing text
        :return: None
        """
        try:
            element = self.fetch_element(locator)

            actions = ActionChains(self.context.driver)
            actions.move_to_element(element)
            actions.click(element)
            actions.pause(delay)
            actions.send_keys(text)
            actions.perform()
            logging.info(
                "Action Chains - sent text %s to element %s",
                text,
                locator,
            )
            sleep(delay)

        except Exception:
            logging.error(
                "Unable to type text %s on element %s.",
                text,
                locator,
                exc_info=True,
            )
            Assert.assert_fail("Unable to type text '" + text + "' on element '" + locator + "'")

    def user_tab_on_element(self, locator=None, delay=0.5, replacement=None):
        """user performs tab keystroke
        :param locator: locator in which to click before tabbing
        :param delay: pause before sending tab
        :param replacement: if locator contains dynamic part, i.e. '$value'=
        it will be replaced by replacement variable
        :return: None
        """
        logging.info("Tabbed on element %s", locator)
        if replacement:
            locator = locator.replace("$value", replacement)

        action = ActionChains(self.context.driver)
        if locator:
            self.fetch_element(locator)
        action.pause(delay)
        action.send_keys(Keys.TAB)
        action.perform()

    def user_deletes_text_from_element(self, locator):
        """user performs ctl+a and delete keystroke"""
        element = self.fetch_element(locator)
        action = ActionChains(self.context.driver)
        action.click(element)
        action.key_down(Keys.CONTROL)
        action.send_keys("a")
        action.key_up(Keys.CONTROL)
        action.send_keys(Keys.DELETE)
        action.perform()

    def user_copy_text_from_element(self, locator):
        """user performs ctl+c keystroke"""
        element = self.fetch_element(locator)
        action = ActionChains(self.context.driver)
        action.double_click(element)
        action.key_down(Keys.CONTROL)
        action.send_keys("c")
        action.key_up(Keys.CONTROL)
        action.perform()

    def user_paste_text_from_element(self, locator):
        """user performs ctl+v keystroke"""
        self.fetch_element(locator)
        action = ActionChains(self.context.driver)
        action.key_down(Keys.CONTROL)
        action.send_keys("v")
        action.key_up(Keys.CONTROL)
        action.perform()

    def user_enter_on_element(self, locator, delay=0.5):
        """user performs enter keystroke"""
        self.fetch_element(locator)
        action = ActionChains(self.context.driver)
        action.pause(delay)
        action.send_keys(Keys.ENTER)
        action.perform()

    def right_click_on_element(self, locator, delay=0.5):
        """user performs right click keystroke"""
        self.fetch_element(locator)
        action = ActionChains(self.context.driver)
        action.pause(delay)
        action.move_to_element(locator)
        action.context_click(locator)
        action.perform()

    def user_enter_on_element_pdf(self, delay=0.5):
        """user performs enter keystroke"""
        action = ActionChains(self.context.driver)
        action.pause(delay)
        action.send_keys(Keys.ENTER)
        action.perform()

    def drag_and_drop_with_offset_to_the_right(self, locator, xoffset):
        """user performs drag and drop with offset to the right"""
        element = self.fetch_element(locator)
        action = ActionChains(self.context.driver)
        action.drag_and_drop_by_offset(element, xoffset, 0)
        action.perform()

    def drag_and_drop_with_offset_to_the_left(self, locator, xoffset):
        """user performs drag and drop with offset to the left"""
        element = self.fetch_element(locator)
        action = ActionChains(self.context.driver)
        action.drag_and_drop_by_offset(element, xoffset, 0)
        action.perform()

    def user_press_right_arrow_key_on_element(self, locator):
        """user performs right arrow key keystroke"""
        self.fetch_element(locator)
        action = ActionChains(self.context.driver)
        action.send_keys(Keys.ARROW_DOWN)
        action.perform()

    def user_press_down_arrow_key_on_element(self, locator):
        """user performs right arrow key keystroke"""
        self.fetch_element(locator)
        action = ActionChains(self.context.driver)
        action.send_keys(Keys.ARROW_RIGHT)
        action.perform()

    def user_press_left_arrow_key_on_element(self, locator):
        """user performs left arrow key keystroke"""
        element = self.fetch_element(locator)
        action = ActionChains(self.context.driver)
        action.click(element)
        action.send_keys(Keys.ARROW_LEFT)
        action.perform()

    def close_windows(self, windows, locator_popup, locator_button, delay=0.5):
        """close windows"""
        sleep(delay)
        if self.window_count(delay) > windows:
            self.switch_to_default_content()
            self.close_other_tabs()
            if self.is_element_displayed(locator_popup):
                self.click(locator_button)
                self.close_other_tabs()

    def submit(self, locator, replacement=None):
        """Submit a form
        :param locator: input submit button
        :param replacement: if locator contains dynamic part, i.e. '$value'=
        it will be replaced by replacement variable
        :return: None
        """
        if replacement:
            locator = locator.replace("$value", replacement)

        try:
            _element = self.fetch_element(locator)
            _element.submit()
            logging.info("Submitted form'")
        except Exception as ex:
            logging.error("Unable to submit form! Error: %s", ex, exc_info=True)
            Assert.assert_fail("Unable to submit form!")

    def get_text(self, locator, replacement=None):
        """Return text from locator
        :param locator: locator from which to fetch text
        :param replacement: if locator contains dynamic part, i.e. '$value',
        it will be replaced by replacement variable
        :return: element text, None in case no text could be fetched
        """
        if replacement:
            locator = locator.replace("$value", replacement)
        try:
            element_text = self.fetch_element(locator).text
            logging.info(
                "Get text returned %s for element %s",
                element_text,
                locator,
            )
            return element_text
        except Exception:
            logging.error(
                "Unable to get text from element + %s + ",
                locator,
                exc_info=True,
            )
            return None

    def check(self, locator, replacement=None):
        """Check element
        :param locator: element locator
        :param replacement: if locator contains dynamic part, i.e. '$value',
        it will be replaced by replacement variable
        :return: None
        """
        if replacement is not None:
            locator = locator.replace("$value", replacement)

        try:
            element = self.fetch_element(locator)
            if not element.is_selected():
                element.click()
                logging.info("Checked checkbox having element + %s + ", locator)
        except Exception:
            logging.error(
                "Unable to check locator + %s + ",
                locator,
                exc_info=True,
            )
            Assert.assert_fail("Unable to check locator " + locator + "")

    def uncheck(self, locator, replacement=None):
        """Uncheck element
        :param locator: element locator
        :param replacement: if locator contains dynamic part, i.e. '$value',
        it will be replaced by replacement variable
        :return: None
        """
        if replacement is not None:
            locator = locator.replace("$value", replacement)

        try:
            element = self.fetch_element(locator)
            if element.is_selected():
                element.click()
                logging.info("Unchecked checkbox having element + %s + ", locator)
        except Exception:
            logging.error(
                "Unable to uncheck locator + %s + ",
                locator,
                exc_info=True,
            )
            Assert.assert_fail("Unable to uncheck locator " + locator + "")

    def get_title(self):
        """Return browser title
        :return: browser title, None in case of exception
        """
        try:
            logging.info("Get title returned + %s + ", self.context.driver.title)
            return self.context.driver.title
        except Exception as ex:
            logging.error("Unable to get browser title! Error: %s", ex, exc_info=True)
            return None

    def get_element_count(self, locator, replacement=None):
        """Return the number of elements matching the element locator
        :param locator: element locator
        :param replacement: if locator contains dynamic part, i.e. '$value',
        it will be replaced by replacement variable
        :return: length of elements matching, None in case no match found
        """
        if replacement is not None:
            locator = locator.replace("$value", replacement)

        try:
            elements = self.fetch_element(locator, is_list_of_elements=True)

            logging.info(
                "Element count for locator %s returned %s",
                locator,
                str(len(elements)),
            )

            return len(elements)
        except Exception:
            logging.error(
                "Unable to get element count for locator %s",
                locator,
                exc_info=True,
            )
            return None

    def hover(self, locator, replacement=None):
        """Mouse over on element
        :param locator: element locator
        :param replacement: if locator contains dynamic part, i.e. '$value',
        it will be replaced by replacement variable
        :return: None
        """
        if replacement is not None:
            locator = locator.replace("$value", replacement)

        try:
            element = self.fetch_element(locator)

            mouse_hover = ActionChains(self.context.driver).move_to_element(element)
            mouse_hover.perform()
        except Exception:
            logging.error(
                "Unable to hover on locator + %s + ",
                locator,
                exc_info=True,
            )
            Assert.assert_fail("Unable to hover on locator '" + locator + "'")

    def execute_java_script(self, script, element=None):
        """Execute raw java script statements
        :param script: java script to execute
        :param element: webdriver element on which to execute the java script
        :return: None
        """
        try:
            self.context.driver.execute_script(script, element)
        except Exception:
            logging.error(
                "Unable to execute java script + %s +",
                script,
                exc_info=True,
            )
            Assert.assert_fail("Unable to execute java script '" + script + "'")

    def select_by_visible_text(self, locator, option_text, replacement=None):
        """Select an option by visible option text
        :param locator: locator of select element
        :param replacement: if locator contains dynamic part, i.e. '$value',
        it will be replaced by replacement variable
        :param option_text: option text by which to select the option
        :return: None
        """
        if replacement:
            locator = locator.replace("$value", replacement)

        try:
            select = Select(self.fetch_element(locator))
            select.select_by_visible_text(option_text)

            logging.info("Selected element + %s+ by visible text + %s+ ", locator, option_text)
        except Exception:
            logging.error(
                "Unable to select option + %s +",
                option_text,
                exc_info=True,
            )
            Assert.assert_fail("Unable to select option '" + option_text + "'")

    def switch_to_frame(self, frame_number, assert_it=True):
        """Switch to a frame
        :param frame_number: frame number to switch to
        :param assert_it: whether to assert switching to frame or not
        :return: None
        """
        try:
            self.context.driver.switch_to.frame(frame_number)
            logging.info("Successfully switched frame")
        except Exception:
            logging.info("Frame not loaded yet! Waiting for another 10 seconds for frame to load...")
            sleep(int(settings.wait_time))

            try:
                self.context.driver.switch_to.frame(frame_number)
                logging.info("Successfully switched to frame numbered + %s+ ", str(frame_number))
            except Exception:
                logging.error(
                    "Unable to locate frame numbered + %s+ ",
                    str(frame_number),
                    exc_info=True,
                )
                if assert_it:
                    Assert.assert_fail("Unable to locate frame numbered '" + str(frame_number) + "' ")

    def switch_to_default_content(self, assert_it=True, delay=0.5):
        """Switch to parent window
        :return: None
        """
        sleep(delay)
        try:
            self.context.driver.switch_to.default_content()
            logging.info("Successfully switched to default frame")
        except Exception as ex:
            logging.error("Unable to switch to default content! Error: %s", ex, exc_info=True)
            if assert_it:
                Assert.assert_fail("Unable to switch to default content!")

    def switch_to_new_window(self, count=0, expected_window_url=None, validate_url=False, delay=0.5):
        """switch to the new window"""
        sleep(delay)
        tabs = self.context.driver.window_handles
        opened_urls = []

        if count > 0:
            self.context.driver.switch_to.window(tabs[count])
            opened_urls.append(self.context.driver.current_url)
        else:
            for tab in tabs:
                self.context.driver.switch_to.window(tab)
                logging.info("Switching to tab URL: %s", self.context.driver.current_url)
                opened_urls.append(self.context.driver.current_url)
            return opened_urls

        actual_window_url = self.context.driver.current_url
        logging.info("CURRENT URL: %s", actual_window_url)
        if validate_url is True:
            Assert.assert_true(
                expected_window_url in actual_window_url,
                "The expected and actual new window url do not match",
            )
        return opened_urls

    def switch_to_indexed_window(self, index, delay=0.5):
        """Switch window by index"""
        tabs = self.context.driver.window_handles
        self.context.driver.switch_to.window(tabs[index])
        sleep(delay)

    def find_current_url(self):
        """Find current URL"""
        return self.context.driver.current_url

    def window_count(self, delay=0.5):
        """counts the number of opened windows"""
        sleep(delay)
        return len(self.context.driver.window_handles)

    def close_other_tabs(self, delay=0.5):
        """function allows closing other tabs and keeps the focus on the specified"""
        sleep(delay)
        driver_len = len(self.context.driver.window_handles)
        logging.info("Length of Driver = %s ", driver_len)
        if driver_len > 1:
            for i in range(driver_len - 1, 0, -1):
                self.context.driver.switch_to.window(self.context.driver.window_handles[i])
                self.context.driver.close()
                print("Closed Tab No. ", i)
            self.context.driver.switch_to.window(self.context.driver.window_handles[0])
        else:
            print("Found only Single tab.")

    def go_to(self, app):
        """goes to app"""
        self.context.driver.get(app)

    def press_key(self, locator, key, replacement=None):
        """Press keyboard key in locator
        :param locator: locator in which to type
        :param key: key to press
        :param replacement: this should replace the dynamic part in locator
        it will refresh the browser and try to find the element again
        :return: None
        """
        if replacement:
            locator = locator.replace("$value", replacement)
        try:
            self.fetch_element(locator).send_keys(key)
            logging.info("Pressed key + %s + on element + %s +", key, locator)
        except Exception:
            logging.error(
                "Unable to press key + %s+ on element + %s+ ",
                key,
                locator,
                exc_info=True,
            )
            Assert.assert_fail("Unable to press key '" + key + "' on element '" + locator + "' ")

    def input_attachment_1(self, locator, filename):
        """Add attachment"""
        self.fetch_element(locator)
        action = ActionChains(self.context.driver)
        action.send_keys(filename)
        action.perform()

    def input_attachment(self, locator, filename):
        """Add attachment"""
        element = self.fetch_element(locator)
        action = ActionChains(self.context.driver)
        action.move_to_element(element)
        action.click(element)
        action.send_keys(filename)
        action.perform()

    def double_click(self, locator, delay=0.5):
        """user performs double click"""
        element = self.fetch_element(locator)
        action = ActionChains(self.context.driver)
        action.double_click(element)
        action.pause(delay)
        action.perform()

    def user_enters_text_then_tabs(self, text, delay=0.5):
        """user enters text and performs tab keystroke
        :param delay: pause before sending tab
        :return: None
        """
        logging.info("Enter text '%s' and tab", text)

        action = ActionChains(self.context.driver)
        action.pause(delay)
        action.send_keys(text)
        action.send_keys(Keys.TAB)
        action.perform()

    def type_using_loop(self, locator, text, delay=1.0):
        """User types one character at a time"""
        for i in text:
            self.fetch_element(locator)
            action = ActionChains(self.context.driver)
            action.send_keys(i)
            action.perform()
            sleep(random.uniform(0.1, delay))

    def retry_until_displayed(self, locator, timeout=10, max_count=2, replacement=None):
        """Look for element on a loop"""
        if replacement:
            locator = locator.replace("$value", replacement)

        while max_count > 0:
            if not self.is_element_displayed(locator):
                logging.info("Element with %s is not displayed", locator)
                sleep(timeout)
            else:
                logging.info("Element is displayed")
                return True

            max_count = max_count - 1
        return False

    def convert_pdf_to_txt(self, path):
        """convert pdf to txt file"""
        rsrcmgr = PDFResourceManager()
        retstr = io.StringIO()
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos = set()
        with open(path, "rb") as filep:
            for page in PDFPage.get_pages(
                filep,
                pagenos,
                maxpages=maxpages,
                password=password,
                caching=caching,
                check_extractable=True,
            ):
                interpreter.process_page(page)

            text = retstr.getvalue()

        filep.close()
        device.close()
        retstr.close()
        return text

    def extract_text_by_page(self, pdf_path):
        """extract text by page"""
        with open(pdf_path, "rb") as file_handle:
            for page in PDFPage.get_pages(file_handle, caching=True, check_extractable=True):
                resource_manager = PDFResourceManager()
                fake_file_handle = io.StringIO()

                converter = TextConverter(resource_manager, fake_file_handle)

                page_interpreter = PDFPageInterpreter(resource_manager, converter)

                page_interpreter.process_page(page)
                text = fake_file_handle.getvalue()

                yield text

                # close open handles
                converter.close()
                fake_file_handle.close()

    def extract_text(self, pdf_path):
        """extract text"""
        for page in self.extract_text_by_page(pdf_path):
            print(page)
            print()

    def switch_window_click_enter(self):
        """switch window handle and click enter"""
        self.context.driver.switch_to.window(self.context.driver.window_handles[-1])
        sleep(int(settings.wait_time))
        active_element = self.context.driver.switch_to.active_element
        active_element.send_keys(Keys.ENTER)
        sleep(int(settings.wait_time))

    def find_user(self):
        """obtain user to construct default download directory"""
        return getpass.getuser()

    def delete_pdfs_from_target_dir(self, target):
        """Check dir for pdf's and delete"""
        files = os.listdir(target)
        for file in files:
            if not os.path.isdir(file) and ".pdf" in file:
                pdf_path = target + file
                os.remove(pdf_path)

    def prepare_text_file(self, text):
        """Process text file to compare with PDF"""
        result = text.replace("\n", "")
        result = result.replace(" ", "")
        return result

    def refresh_browser(self, timeout=settings.wait_time):
        """Refresh browser"""
        logging.info("Refreshing browser")
        self.context.driver.refresh()
        sleep(int(timeout))
        logging.info("Refreshed browser")

    def clear_modal_if_displayed(self, locator, timeout):
        """Clear modal when first logging in"""
        if self.retry_until_displayed(locator, timeout=timeout):
            logging.info("Modal displayed")
            self.click("XPATH, //*[@id='toggle-offer-to-open']")
            self.click("XPATH, //*[@class='ui-button primary-button']")
            logging.info("Closing modal")

    def until_element_displayed(self, locator, iterator=30, wait=1):
        """Repeats the step to check if element is displayed while a page is rendering"""
        logging.info("Repeat until locator '%s' is displayed", locator)
        iteration_loop = iterator
        while iteration_loop > 0:
            if not self.is_element_displayed(locator, timeout=wait):
                sleep(wait)
            else:
                logging.info("Locator '%s' displayed", locator)
                return True
            iteration_loop -= 1
        return False

    def until_element_displayed_click(self, locator, iterator=30, wait=1):
        """Repeats the step to check if element is present while a page is rendering"""
        logging.info("Repeating wait/click for locator '%s'", locator)
        iteration_loop = iterator
        while iteration_loop > 0:
            if not self.is_element_displayed(locator, timeout=wait):
                sleep(wait)
            else:
                self.click(locator)
                return True
            iteration_loop -= 1
        return False
