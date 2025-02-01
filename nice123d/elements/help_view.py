from nicegui import ui
import logging

from pathlib import Path
import os
from app_logging import NiceGUILogHandler

# [Variables]


class HelpView(ui.element):

    def __init__(self, path=Path('./help'), **kwargs):
        super().__init__(**kwargs)
        self.help_path = path
        with self:
            with ui.row():
                self.main = ui.label("Help View")

    def set_logger(self, logger: logging.Logger):
        """Set the logger to use for logging."""
        self.logger = logger
        # self.logger.addHandler(NiceGUILogHandler(self.log))

