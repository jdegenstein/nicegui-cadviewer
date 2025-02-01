from nicegui import ui
from datetime import datetime
import time

class Console(ui.element):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.time_start()
        # TODO:           self.logger = NiceGUILogHandler(self.logger_ui)

        with self:
            with ui.row().classes('w-full h-full'):
                self.logger = ui.log(max_lines=40).classes('w-full h-full')
    
        self.push(self.info('init', 'Code editor initialized'))

    def time_start(self):
        self.start_time = time.time()

    def info(self, function, message, do_time=True):
        timestamp = datetime.now().strftime('%X.%f')[:-5]
        use_time = ''
        if do_time:
            used_time = f'in {time.time() - self.start_time:0.2}s'
        return f'{timestamp}: [{function}] {message} {used_time}'

    def push(self, message):
        self.logger.push(message)

