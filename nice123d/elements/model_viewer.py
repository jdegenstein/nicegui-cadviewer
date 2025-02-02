"""
# Model viewer element for nice123d.

This module provides a model viewer based on `OCP_vscode` for nice123d.

"""

# [Imports]                                       #| description or links
from nicegui import ui                            #| [docs](https://nicegui.readthedocs.io/en/latest/)   
from elements.base_view import BaseView           #| Base class for all views
from .constants import *                          #| The application constants
from backend.path_manager import PathManager      #| Managing file and directory handling for the application
import subprocess                                 #| [docs](https://docs.python.org/3/library/subprocess.html)
from ocp_vscode import *                          #| [docs](https://ocp_vscode.readthedocs.io/en/latest/)


# [Variables]


# [Main Class]
class ModelViewer(BaseView):
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
        self.time_start('model_viewer')
        with self:
            self.ocpcv = (
                            ui.element("iframe")
                            .props(f'src="http://{ip_address}:{port}/viewer"')
                            .classes("w-full h-[calc(100vh-5rem)]")
                        )
            self.info('ModelViewer', f'init src="http://{ip_address}:{port}/viewer"', call_id='model_viewer')
        self.main = self.ocpcv

    # [API]
    def startup(self):
        """
        run ocp_vscode in a subprocess
        """
        self.time_start('model_viewer')
        # spawn separate viewer process
        self.ocpcv_proc = subprocess.Popen(["python", "-m", "ocp_vscode", "--port", str(self.port)])
        # pre-import build123d and ocp_vscode in main thread
        exec("from build123d import *\nfrom ocp_vscode import *")
        self.info('ModelViewer', f'started {self.ocpcv_proc}', call_id='model_viewer')

    def shutdown(self):
        """"
        kill the ocp_vscode process
        """
        self.info(f'Model Viewer', f'shutdown {self.ocpcv_proc}', call_id='model_viewer')
        self.ocpcv_proc.kill()
        # ocpcv_proc.terminate() # TODO: investigate best cross-platform solution

    # [Event Handlers]
