
# [Imports]                                      #| description or links
from nicegui import ui                           #| [docs](https://nicegui.readthedocs.io/en/latest/)   
from elements.base_view import BaseView          #| Base class for all views
from .constants import *                         #| The application constants
from backend.path_manager import PathManager     #| Managing file and directory handling for the application

# [Variables]

# [Main Class]
class ProjectGallery(BaseView):

    # [Variables]

    # [Constructor]
    def __init__(self, path_manager=None, **kwargs):
        super().__init__(path_manager, **kwargs)
        self.models_path = self.paths.models_path
        self.models = [model for model in self.models_path.iterdir() if model.is_dir()]

        with self:
            with ui.row() as main   :
                ui.label("Project Gallery")
        
        self.main = main

    # [API]
    # [Event Handlers]