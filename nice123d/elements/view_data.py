"""
TODO: docs for this file
"""

# [Imports]
from nicegui import ui
from typing import Callable, Optional, Tuple

# [Variables]

# [Main Class]
class ViewData:
    """
    A class for managing the view data.
    """
    def __init__(self, title: str, icon: str, position: Tuple[bool, bool], short_cut: str = ""):

        # - Type checks:
        if title == "":
            raise ValueError("The title must not be empty.")
        elif type(title) is not str:
            raise TypeError("The title must be a string.")
        if icon == "":
            raise ValueError("The icon must not be empty.")
        elif type(icon) is not str:
            raise TypeError("The icon must be a string (name of material icon).")
        elif icon.find(" ") != -1:
            print("Warning: The icon name contains spaces. Replacing spaces with underscores.")
            icon = icon.replace(" ", "_")

        # - Assigning values:
        self.title: str = title
        self.icon: str = icon
        self.is_left: bool = position[0]
        self.is_right: bool = position[1]
        self.short_cut: str = short_cut
        self.view: Optional[str] = None
        self.button_left: Optional[ui.button]  = None
        self.button_right: Optional[ui.button] = None

    def __str__(self):
        return f'''
        title: {self.title}
        icon: {self.icon}
        is_left: {self.is_left}
        is_right: {self.is_right}
        short_cut: {self.short_cut}
        view: {self.view}
        button_left: {self.button_left}
        button_right: {self.button_right}
        '''

