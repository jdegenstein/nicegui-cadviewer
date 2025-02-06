"""
BaseButtonBar -> ui.element 
 +-> ui.button_group

file:           nice123d/base_button_bar.py
file-id:        77550f13-5b5d-4f7a-a9e7-3fb960f658e2
project:        nice123d
project-id:     e2bbd03f-0ac6-41ec-89ae-2ad52fa0652a
author:         felix@42sol.eu

description: |
    This class is used for a button bar controlling the view of the application on a specific panel.
"""

# [Imports]                                      #| description or links 
from nicegui import ui                           #| [docs](https://nicegui.readthedocs.io/en/latest/)   
from typing import Optional                      #| [docs](https://docs.python.org/3/library/typing.html)
from .constants import *

# [Main Class]
class BaseButtonBar(ui.element):
    _sibling_button: Optional['Button'] = None
    _view: Optional['View'] = None
    
    def __init__(self, icon, sibling_button_bar = None, view = None, **kwargs):
        self._button_bar = None
        self._sibling_button_bar = None
        self._icon = icon
        self._view = view
        # encapsulate the on_click function
        
        self._on_click = on_click

        super().__init__(text, on_click=self.toggle_on_click, **kwargs)
    
    def create(self):
        with self:
            with ui.column():
                if self._icon:
                    ui.icon(self._icon)
                self._button_group = ui.button_group()

    @property
    def sibling_button_bar(self):
        return self._sibling_button_bar
    
    @sibling_button.setter
    def sibling_button_bar(self, value):        
        self._sibling_button_bar = value

    @property
    def view(self):
        return self._view
    
    @view.setter
    def set_view(self, value):
        self._view = value

