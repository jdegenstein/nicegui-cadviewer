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
class HelpView(ui.element):
    """"
    Help view keeps track of the help files.
    They leverage the NiceGUI elements to generate a interactive help view.
    """
    # [Variables]

    # [Constructor]
    def __init__(self, path=Path('./help'), **kwargs):
        super().__init__(**kwargs)
        self.help_path = path
        with self:
            with ui.column() as main:
                with ui.row():
                    ui.label("Help View")
                    ui.input(placeholder="Search")
                    ui.button("Load Help")
        self.main = main
    
    # [API]

    # [Event Handlers]
