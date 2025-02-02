"""
TODO: docs for this file
"""

# [Imports]                                      #| description or links
from nicegui import ui                           #| [docs](https://nicegui.readthedocs.io/en/latest/)   
from nice123d.elements.base_view import BaseView #| Base class for all views
from constants import *                          #| The application constants
from ..backend.path_manager import PathManager   #| Managing file and directory handling for the application


# [Variables]
# TODO: consider separate editor execution thread from nicegui thread


# [Main Class]
class CodeEditor(BaseView):
    """
    A Python code editor component.
    """

    # [Variables]
    font_size = 18   # todo: use font size for the editor

    # [Constructor]
    def __init__(self, code_file=None, new_file=None, **kwargs):
        """Initialize the Python editor component."""
        super().__init__(**kwargs)
        
        self.file_name = ''
        self.model_path = ''
        
        with self:
            with ui.row().classes('w-full h-full'):
                # Setup editor
                self.editor = ui.codemirror(language='python', theme='dracula')
                self.editor.classes('w-full h-full')
                
                self.new_file = None 
                if new_file and new_file.exists():
                    self.new_file = new_file
    
        if code_file and code_file.exists():
            with code_file.open() as f:
                code = f.read()
                self.editor.value = code
                self.file_name = code_file.name
                self.model_path = code_file.parent

        else:
            self.new_file = new_file
            self.on_new()
            self.model_path = Path('../../models')

    # [API]
    def set_file_name(self, event):
        self.file_name = event.value

    def prepare_move(self):
        """Prepare to move the editor to a new location."""
        self.code = self.editor.value

    def finish_move(self):
        """Finish moving the editor to a new location."""
        self.editor.value = self.code
        self.editor.update()

    def execute_code(self, code: str):
        """Execute the Python code in the editor."""
        # TODO: look into `RestrictedPython` or  `Jupyter` for security 
        try:
            exec(code)
            return "Code executed successfully"
        except Exception as e:
            return f"Error: {str(e)}"

    # [Event Handlers]
    def on_save(self):
        """Save the current code to a file."""
        self.time_start()
        content = self.editor.value
        file_path = Path(self.model_path, self.file_name)
        with file_path.open('w') as f:
            f.write(content)
        self.info('file', 'saved successfully')

    def on_load(self):
        """Load code from a file into the editor."""
        self.time_start()

        def handle_upload(e: events.UploadEventArguments):
            text = e.content.read().decode('utf-8')
            self.editor.value = text
            self.file.value = e.name 
            
            upload_bar.delete()
            
        upload_bar = ui.upload(auto_upload=True, on_upload=handle_upload).props('accept=.py').classes('max-w-full')        
        # TODO: ^ for now we need a second click to upload the file
        
        self.logger.push(self.info('file', 'loaded successfully'))
        
    def on_new(self):
        """Clear the editor."""
        self.time_start()
        if self.new_file:
            with self.new_file.open('r') as f:
                self.editor.value = f.read()
            if self.logger:    # TODO: move logging registration ealier in main window ?
                self.logger.push(self.info('file', f'loaded template {self.new_file}'))
        else:
            if self.logger:    # TODO: move logging registration ealier in main window ?
                self.logger.push(self.info('file', 'No template file specified (`new.py` in `models`). Using minimal default code'))
            self.editor.set_value('from build123d import *\nfrom ocp_vscode import *\n\n\nshow_all()')

    def on_run(self):
        """Execute the code from the editor."""
        self.time_start()
        result = self.execute_code(self.editor.value)
        self.logger.push(self.info('on_run', result))
        
        
