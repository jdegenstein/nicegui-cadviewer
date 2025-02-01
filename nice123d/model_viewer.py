"""
# Model viewer element for nice123d.

This module provides a model viewer based on `OCP_vscode` for nice123d.


"""

from nicegui import ui
import logging
from ocp_vscode import *

import subprocess
from app_logging import NiceGUILogHandler

class ModelViewer(ui.element):

    def __init__(self, ip_address= '127.0.0.1', port=3939, **kwargs):
        super().__init__(**kwargs)
        self.port = port

        with self:
            with ui.row().classes('w-full h-full'):
                self.ocpcv = (
                                ui.element("iframe")
                                .props(f'src="http://{ip_address}:{port}/viewer"')
                                .classes("w-full h-[calc(100vh-5rem)]")
                            )

    def set_logger(self, logger: logging.Logger):
        """Set the logger to use for logging."""
        self.logger = logger
        # self.logger.addHandler(NiceGUILogHandler(self.log))

    # run ocp_vscode in a subprocess
    def startup(self):
        # spawn separate viewer process
        self.ocpcv_proc = subprocess.Popen(["python", "-m", "ocp_vscode", "--port", str(self.port)])
        # pre-import build123d and ocp_vscode in main thread
        exec("from build123d import *\nfrom ocp_vscode import *")

    def shutdown(self):
        self.ocpcv_proc.kill()
        # ocpcv_proc.terminate() # TODO: investigate best cross-platform solution

