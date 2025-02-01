from nicegui import ui
from nicegui.events import KeyEventArguments
import logging

from app_logging import NiceGUILogHandler
from project_gallery import ProjectGallery, models_path, code_file, new_file
from code_editor import CodeEditor
from ocp_viewer import OcpViewer

import platform
active_os = platform.system()       # get the operating system

# Add custom CSS for responsive sizing
ui.add_css('''
    :root {
        --nicegui-default-padding: 0.5rem;
        --nicegui-default-gap: 0.5rem;
    }
''')

class MainWindow(ui.element):
    
    def __init__(self, app, models_path=models_path, code_file=code_file, new_file=new_file):
        self.app = app
        self.width =1800
        self.height= 900
        self.title="nicegui-cadviewer"

        self.model_path = models_path
        self.code_file = models_path / code_file
        self.new_file = models_path / new_file

        ui.add_css('''
            :root {
                --nicegui-default-padding: 0.5rem;
                --nicegui-default-gap: 0.5rem;
            }
        ''')
                

        # connect logger to sub elements
        self.gallery.set_logger(self.logger)
        self.editor.set_logger(self.logger)
        self.viewer.set_logger(self.logger)

    @property
    def size(self):
        return (self.width, self.height)

    def startup(self):
        self.viewer.startup()
        ui.keyboard(on_key=self.handle_key)

    def handle_key(self, e: KeyEventArguments):
        if active_os == "Windows":
            main_modifier = e.modifiers.ctrl
        elif active_os == "Mac":
            main_modifier = e.modifiers.cmd
        else:
            main_modifier = e.modifiers.meta

        if main_modifier and e.action.keydown:
            if e.key.enter:
                self.editor.on_run()             # TODO: fix editor
            elif e.key.name == "s":
                self.editor.on_save()
            elif e.key.name == "o":
                self.editor.on_load()
            elif e.key.name == "t":
                self.editor.on_new()

    def on_close_window(self, event):
        self.viewer.shutdown()
        self.editor.on_save()
        self.close()
        self.app.shutdown()



