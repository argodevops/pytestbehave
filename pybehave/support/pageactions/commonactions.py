"""
Common Actions is a pre-set collection of actions to achieve a repeated bit of functionality.
"""

from pybehave.support.locators.locator import Locator
from pybehave.support.pageactions.actionenum import Action
from pybehave.support.pageactions.basepage import BasePage


class CommonActions(BasePage):
    """
    Collection of commonly used actions
    """

    def select_option_from_dropdown(self, locator: Locator, text: str, delay=0.5):
        """utility method that will check locator displayed, enter text with action chains, and then press enter"""
        self.select_option_with_action(locator=locator, text=text, action=Action.ENTER_KEY, delay=delay)

    def select_option_with_action(self, locator: Locator, text: str, action: Action = Action.ENTER_KEY, delay=0.5):
        """utility method that will check locator displayed, enter text with action chains, and then press enter"""
        self.assert_element_displayed_and_click(locator)
        self.user_action_on_element(locator, action=Action.DELETE_TEXT)
        self.type_using_action_chains(locator, text=text, delay=delay)
        self.user_action_on_element(locator, action=action)
