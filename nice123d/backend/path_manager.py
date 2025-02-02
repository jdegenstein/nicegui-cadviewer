"""
TODO: docs for this file
"""

# [Imports]
from pathlib import Path
import os
from app_logging import NiceGUILogHandler

# [Variables]

# [Main Class]
class PathManager():
    """
    Path manager keeps track of the paths for the models and the help files.
    """
    # [Variables]
    models_path = Path(__file__).parent / ".." / ".." / "models"
    help_path = Path('./help')
    
    # [Constructor]
    def __init__(self, models_path=models_path, help_path=help_path):
        self.models_path = models_path
        self.help_path = help_path

    # [API]
    def get_models_path(self):
        return self.models_path

    def get_help_path(self):
        return self.help_path

    # [Event Handlers]
    def on_load_data(self):
        self.info("Data loaded")
    
    def on_save_data(self):
        self.info("Data saved")
    
    def on_validate_data(self):
        self.info("Data validated")