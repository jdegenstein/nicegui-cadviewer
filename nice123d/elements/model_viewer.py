"""
# Model viewer element for nice123d.

This module provides a model viewer based on `OCP_vscode` for nice123d.

"""

# [Imports]                                      #| description or links
from nicegui import ui                           #| [docs](https://nicegui.readthedocs.io/en/latest/)   
from nice123d.elements.base_view import BaseView #| Base class for all views
from constants import *                          #| The application constants
from ..backend.path_manager import PathManager   #| Managing file and directory handling for the application
from ocp_vscode import *                         #| [docs](https://ocp_vscode.readthedocs.io/en/latest/)

import subprocess                                #| [docs](https://docs.python.org/3/library/subprocess.html)


# [Variables]


# [Main Class]
class ModelViewer(ui.element):
    """"
    Model viewer element keeps track of the model files.
    Using:
    - OCP_vscode for viewing the models.
    - pywebview for the GUI.
    """
    # [Variables]
    # [Constructor]
    def __init__(self, ip_address= '127.0.0.1', port=3939, **kwargs):
        super().__init__(**kwargs)
        self.port = port

        with self:
            with ui.row().classes('w-full h-full') as main:
                self.ocpcv = (
                                ui.element("iframe")
                                .props(f'src="http://{ip_address}:{port}/viewer"')
                                .classes("w-full h-[calc(100vh-5rem)]")
                            )
        self.main = main

    # [API]
    # run ocp_vscode in a subprocess
    def startup(self):
        # spawn separate viewer process
        self.ocpcv_proc = subprocess.Popen(["python", "-m", "ocp_vscode", "--port", str(self.port)])
        # pre-import build123d and ocp_vscode in main thread
        exec("from build123d import *\nfrom ocp_vscode import *")

    def shutdown(self):
        self.ocpcv_proc.kill()
        # ocpcv_proc.terminate() # TODO: investigate best cross-platform solution

    # [Event Handlers]
