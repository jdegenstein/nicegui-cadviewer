"""
TODO: docs for this file
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

