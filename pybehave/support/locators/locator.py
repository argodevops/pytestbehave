"""pythons Enum"""

from enum import Enum

from pybehave.support.locators.locatortype import LocatorType


class Locator(Enum):
    """Loctator Enum base class providing functionality to inherit"""

    def __init__(self, strategy: LocatorType, locator: str):
        assert locator != "", "locator value is empty"
        self.locator = locator
        self.strategy = strategy

    def get_locator(self, replacement=None):
        """returns the locator string, optional replacement"""
        return self.locator if replacement is None else self.locator.replace("$value", str(replacement))

    def get_formatted_locator(self, replacement=None):
        """Returns a pre-formatted locator string"""
        return self.strategy.value + ", " + self.get_locator(replacement=replacement)

    def get_strategy(self):
        """returns the LocatorType - use .name or .value of returned item"""
        return self.strategy
