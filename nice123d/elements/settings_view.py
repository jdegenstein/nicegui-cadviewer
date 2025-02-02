"""
TODO: docs for this file
"""

# [Imports]                                      #| description or links
from nicegui import ui                           #| [docs](https://nicegui.readthedocs.io/en/latest/)   
from nice123d.elements.base_view import BaseView #| Base class for all views
from constants import *                          #| The application constants
from ..backend.path_manager import PathManager   #| Managing file and directory handling for the application

# [Variables]

# [Main Class]
class SettingsView(ui.element):

    # [Variables]

    # [Constructor]
    def __init__(self, path=Path('./settings'), **kwargs):
        super().__init__(**kwargs)
        self.settings_path = path
        with self:
            with ui.row() as main:
                ui.label("Settings View")

        self.main = main

    # [API]
    # [Event Handlers]

