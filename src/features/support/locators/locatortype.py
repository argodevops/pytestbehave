"""Pythons enum imports"""

from enum import Enum, EnumMeta, unique


# believe v3.12 __contains__ is both name and values check.
def overriden__contains__(cls, member):
    """to override contains method to match on values too"""
    return (
        isinstance(member, cls)
        and member.name in cls._member_map_
        or any(m._value_ == member for m in cls._member_map_.values())
    )


EnumMeta.__contains__ = overriden__contains__


@unique
class LocatorType(Enum):
    """Enumeration of the locator types"""

    XPATH = "XPATH"
    ID = "ID"
    NAME = "NAME"
    CLASS_NAME = "CLASS_NAME"
    LINK_TEXT = "LINK_TEXT"
    CSS_SELECTOR = "CSS_SELECTOR"
    PARTIAL_LINK_TEXT = "PARTIAL_LINK_TEXT"
    TAG_NAME = "TAG_NAME"
