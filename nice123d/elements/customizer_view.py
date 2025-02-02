"""
TODO: docs for this file
"""

# [Imports]                                      #| description or links
from nicegui import ui                           #| [docs](https://nicegui.readthedocs.io/en/latest/)   
from elements.base_view import BaseView          #| Base class for all views
from .constants import *                         #| The application constants
from backend.path_manager import PathManager     #| Managing file and directory handling for the application

# [Variables]


# [Main Class]
class CustomizerView(BaseView):
    """
    Customizer view keeps track of parameters defined in the code editor.
    Able to update them in the file itself.
    Used to customize the model parameters for showing.
    """
    # [Variables]

    # [Constructor]
    def __init__(self, path_manager=None, **kwargs):
        super().__init__(path_manager, **kwargs)

        self.models_path = self.paths.models_path

        # TODO: extract this to a method
        self.models = [model for model in self.models_path.iterdir() if model.is_dir()]
        with self:
            with ui.row() as main:
                ui.label("Customizer")
        
        self.main = main

    # [API]

    # [Event Handlers]
    def on_load_data(self):
        self.info("Data loaded")
    
    def on_save_data(self):
        self.info("Data saved")

    def on_validate_data(self):
        self.info("Data validated")
