"""
TODO: docs for this file
"""

# [Imports]                                      #|
from enum import Enum  # | [docs](https://docs.python.org/3/library/enum.html)
import platform  # | [docs](https://docs.python.org/3/library/platform.html)


# [Types]
class Side(Enum):
    """
    Enum for defining the side in the view.
    """

    NONE = 0
    LEFT = 1
    RIGHT = 2
    BOTH = 3


# [Constants]
Yes = True
No = False

active_os = platform.system()  # get the operating system

# TODO: check if still used
left = True, False
right = False, True
both = True, True
none = False, False

# [Parameters]
P__experimental = Yes # or No
P__native_window = Yes
P__use_splitter_buttons = No
