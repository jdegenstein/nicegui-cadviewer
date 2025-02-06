"""
SettingsView -> BaseView -> ui.element

file:           nice123d/elements/settings_view.py
file-id:        0561e45d-2fc2-41ed-b5b2-b07db7977885
project:        nice123d
project-id:     e2bbd03f-0ac6-41ec-89ae-2ad52fa0652a
author:         felix@42sol.eu

description: |
    This class implements the application settings editor.
    It is a place to view all the application settings in the applications `settings` directory.
"""

# [Imports]                                      #| description or links
from nicegui import ui                           #| [docs](https://nicegui.readthedocs.io/en/latest/)   
from elements.base_view import BaseView #| Base class for all views
from .constants import *                          #| The application constants
from backend.path_manager import PathManager   #| Managing file and directory handling for the application

# [Variables]

# [Main Class]
class SettingsView(BaseView):

    # [Variables]

    # [Constructor]
    def __init__(self, path_manager=None, **kwargs):
        super().__init__(path_manager, **kwargs)
        self.settings_path = self.paths.settings_path
        
        with self:
            with ui.row() as main:
                ui.label("Settings View")

        self.main = main

    # [API]
    # [Event Handlers]

