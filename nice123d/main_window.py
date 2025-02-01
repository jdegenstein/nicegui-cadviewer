from nicegui import ui
from nicegui.events import KeyEventArguments
import logging

from app_logging import NiceGUILogHandler
from nice123d.elements.project_gallery import ProjectGallery, models_path, code_file, new_file
from nice123d.elements.code_editor import CodeEditor


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

    def on_close_window(self, event):
        self.viewer.shutdown()
        self.editor.on_save()
        self.close()
        self.app.shutdown()



