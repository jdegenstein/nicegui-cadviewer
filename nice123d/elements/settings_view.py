from nicegui import ui
import logging

from pathlib import Path
import os
from app_logging import NiceGUILogHandler

# [Variables]


class SettingsView(ui.element):

    def __init__(self, path=Path('./settings'), **kwargs):
        super().__init__(**kwargs)
        self.settings_path = path
        with self:
            with ui.row():
                self.main = ui.label("Settings View")

    def set_logger(self, logger: logging.Logger):
        """Set the logger to use for logging."""
        self.logger = logger
        # self.logger.addHandler(NiceGUILogHandler(self.log))

    def set_visibility(self, visible):
        self.main.set_visibility(visible)
        return super().set_visibility(visible)