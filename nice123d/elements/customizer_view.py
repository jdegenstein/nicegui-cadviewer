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
class CustomizerView(ui.element):
    """
    Customizer view keeps track of parameters defined in the code editor.
    Able to update them in the file itself.
    Used to customize the model parameters for showing.
    """
    # [Variables]

    # [Constructor]
    def __init__(self, models_path=models_path, **kwargs):
        super().__init__(**kwargs)
        # TODO: check usage of model path 
        self.models_path = models_path
        self.models = [model for model in models_path.iterdir() if model.is_dir()]
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
