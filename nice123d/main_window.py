"""
MainWindow

file:           nice123d/main_window.py
file-id:        964fad81-110b-4d8d-a034-9c9a539415b5
project:        nice123d
project-id:     e2bbd03f-0ac6-41ec-89ae-2ad52fa0652a
author:         jdegenstein, felix@42sol.eu

description: |
    This class implements the main window of the application.
"""

# [Include]                                      #| Description      
from nicegui import ui                           #| [docs](https://nicegui.readthedocs.io/en/latest/)   
from nicegui.events import KeyEventArguments     #| [docs](https://nicegui.readthedocs.io/en/latest/events.html)
from main_views import MainViews                 #| All views collected in main
from backend.path_manager import PathManager     #| Path manager
from elements.constants import *                 #| Constants
# Add custom CSS for responsive sizing
ui.add_css('''
    :root {
        --nicegui-default-padding: 0.5rem;
        --nicegui-default-gap: 0.5rem;
    }
''')

class MainWindow(ui.element):
    
    def __init__(self, app):
        self.app = app
        self.width =1800
        self.height= 900
        self.title="nice123d"
        self.path_manager = PathManager()
        self.views = MainViews(self.path_manager)    

    def run(self):
        self.views.setup()


        # Run the NiceGUI app
        if P__native_window:
            ui.run(
                native      = P__native_window,
                window_size = (1800, 900),
                title       = "nice123d",
                fullscreen  = False,
                # reload      = False
            )
        else:
            ui.run(
                title       = "nice123d",
                fullscreen  = False,
                # reload      = False
            )
                
    @property
    def size(self):
        return (self.width, self.height)

    def startup(self):
        self.views.viewer.startup()

    def on_close_window(self, event):
        self.views.viewer.shutdown()
        self.views.editor.on_save()
        self.app.shutdown()

