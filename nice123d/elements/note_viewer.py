from nicegui import ui
import logging

from pathlib import Path
import os
from app_logging import NiceGUILogHandler

# [Variables]
models_path = Path(__file__).parent / ".." / ".." / "models"
code_file = models_path / "basic.py"
new_file = models_path / "new.py"


class NoteViewer(ui.element):

    def __init__(self, models_path=models_path, **kwargs):
        super().__init__(**kwargs)
        self.models_path = models_path
        self.models = [model for model in models_path.iterdir() if model.is_dir()]
        with self:
            with ui.row():
                self.main = ui.markdown("# Note Viewer")

    def set_logger(self, logger: logging.Logger):
        """Set the logger to use for logging."""
        self.logger = logger
        # self.logger.addHandler(NiceGUILogHandler(self.log))
