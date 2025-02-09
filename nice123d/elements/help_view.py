"""
HelpViewer -> BaseView -> ui.element

file:           nice123d/elements/help_viewer.py
file-id:        adc949b8-0f6a-4cc5-925b-a6a68b64805d
project:        nice123d
project-id:     e2bbd03f-0ac6-41ec-89ae-2ad52fa0652a
author:         felix@42sol.eu

description: |
    This class implements the project help view.
    It is a place to view all the articles in the applications `help` directory.
"""

# [Imports]                                      #| description or links
from nicegui import ui                           #| [docs](https://nicegui.readthedocs.io/en/latest/)   
from elements.base_view import BaseView #| Base class for all views
from .constants import *                          #| The application constants
from backend.path_manager import PathManager   #| Managing file and directory handling for the application

# [Variables]


# [Main Class]
class HelpView(BaseView):
    """"
    Help view keeps track of the help files.
    They leverage the NiceGUI elements to generate a interactive help view.
    """
    # [Variables]

    # [Constructor]
    def __init__(self, path_manager=None, **kwargs):
        super().__init__(path_manager, **kwargs)
        self.help_path = self.paths.help
        with self:
            with ui.row() as main:
                ui.label("Help View")
                ui.input(placeholder="Search")
                ui.button("Load Help")
        self.main = main
    
    # [API]

    # [Event Handlers]
