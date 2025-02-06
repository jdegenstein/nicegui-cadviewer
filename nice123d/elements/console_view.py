"""
ConsoleView -> BaseView -> ui.element

file:           nice123d/elements/consol_view.py
file-id:        6a848c30-083d-4343-a323-3325552dff86
project:        nice123d
project-id:     e2bbd03f-0ac6-41ec-89ae-2ad52fa0652a
author:         felix@42sol.eu

description: |
    This class implements the project console view.
    It collects all the log messages from the different views.
"""

# [Imports]                                      #| description or links
from nicegui import ui                           #| [docs](https://nicegui.readthedocs.io/en/latest/)   
from elements.base_view import BaseView #| Base class for all views
from .constants import *                          #| The application constants
from backend.path_manager import PathManager   #| Managing file and directory handling for the application

# [Variables]

# [Main Class]
class ConsoleView(BaseView):
    """
    Keeping a common ui element for logging messages from the different views.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.time_start('init_console_view')
        # TODO:           self.logger = NiceGUILogHandler(self.logger_ui)

        with self:
            with ui.row().classes('w-full h-full') as main:
                self.logger = ui.log(max_lines=40).classes('w-full h-full')
        
        self.main = main

        super().define_logger(self.logger)

        self.push(self.info('init', 'Code editor initialized', call_id='init_console_view'))

    def push(self, message):
        self.logger.push(message)

