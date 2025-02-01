# [Imports]
from enum import Enum
import platform

# [Types]
class Side(Enum):
    LEFT = 1
    RIGHT = 2


# [Constants]
Yes = True
No  = False

active_os = platform.system()       # get the operating system

left = True, False 
right = False, True
both = True, True
none = False, False

# [Parameters]
P__experimental = Yes or No

