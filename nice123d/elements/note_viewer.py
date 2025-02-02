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
class NoteViewer(ui.element):
    # [Variables]
    # [Constructor]
    def __init__(self, models_path=models_path, **kwargs):
        super().__init__(**kwargs)
        self.models_path = models_path
        self.models = [model for model in models_path.iterdir() if model.is_dir()]
        with self:
            with ui.row() as main:
                ui.markdown("# Note Viewer")
        
        self.main = main

    # [API]
    # [Event Handlers]