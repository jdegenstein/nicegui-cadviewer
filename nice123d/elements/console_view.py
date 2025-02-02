"""
TODO: docs for this file
"""

# [Imports]                                      #| description or links
from nicegui import ui                           #| [docs](https://nicegui.readthedocs.io/en/latest/)   
from nice123d.elements.base_view import BaseView #| Base class for all views
from constants import *                          #| The application constants
from ..backend.path_manager import PathManager   #| Managing file and directory handling for the application

# [Main Class]
class ConsoleView(BaseView):
    """
    Keeping a common ui element for logging messages from the different views.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.time_start()
        # TODO:           self.logger = NiceGUILogHandler(self.logger_ui)

        with self:
            with ui.row().classes('w-full h-full') as main:
                self.logger = ui.log(max_lines=40).classes('w-full h-full')
        
        self.main = main

        super().define_logger(self.logger)

        self.push(self.info('init', 'Code editor initialized'))

    def push(self, message):
        self.logger.push(message)

