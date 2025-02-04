"""
TODO: docs for this file
"""

# [Imports]                                      #| description or links 
from nicegui import ui                           #| [docs](https://nicegui.readthedocs.io/en/latest/)   
from typing import Optional                      #| [docs](https://docs.python.org/3/library/typing.html)
from .constants import *

# [Main Class]
class BaseButton(ui.button):
    _sibling_button: Optional['Button'] = None
    _view: Optional['View'] = None
    
    def __init__(self, text, icon, on_click, sibling_button = None, view = None, **kwargs):
        self._sibling_button = sibling_button
        self._view = view
        # encapsulate the on_click function
        
        self._on_click = on_click

        super().__init__(text, on_click=self.toggle_on_click, **kwargs)
        super().set_icon(icon)

    @property
    def sibling_button(self):
        return self._sibling_button
    
    @sibling_button.setter
    def sibling_button(self, value):        
        self._sibling_button = value

    @property
    def view(self):
        return self._view
    
    @view.setter
    def view(self, value):
        self._view = value

    def toggle_on_click(self, event=None):
        if self._sibling_button is not None:
            self._sibling_button.props('fab color=accent')
        self.props('fab color=active')
        self._on_click(event)
    
