"""
TODO: docs for this file
"""

# [Imports]
from nicegui import ui      #| [docs](https://nicegui.readthedocs.io/en/latest/)   
from .constants import *
from datetime import datetime
import time
from typing import Optional #| [docs](https://docs.python.org/3/library/typing.html)


# [Main Class]
class BaseView(ui.element):
    
    # [Variables]
    logger_available = False    # Whether the logger is available
    main = None                 # The main ui element
    
    # [Constructor]
    def __init__(self, path_manager=None, **kwargs):
        super().__init__(**kwargs)

        if path_manager is not None:
            self._paths = path_manager

        self.start_time = {}

    # [API]

    @property
    def paths(self):
        return self._paths

    def define_logger(self, logger):
        """Set the logger to use for logging."""

        if type(logger) is not ui.log   :
            raise TypeError('The logger must be of type logging.Logger')
        
        self.logger = logger
        self.logger_available = True
        self.time_start(call_id='default')

    def time_start(self, call_id):
        """Start the timer for the logger."""
        self.start_time[call_id] = time.time()

    def info(self, function, message, call_id = 'default', do_time=True):
        """Log an info message with the current time."""
        timestamp = datetime.now().strftime('%X.%f')[:-5]
        used_time = ''
        if do_time:
            used_time = f'in {time.time() - self.start_time[call_id]:0.2}s'
        return f'{timestamp}: [{function}] {message} {used_time}'

    # [Event Handlers]
    def set_visibility(self, visible):
        if self.main:
            self.main.set_visibility(visible)

        return super().set_visibility(visible)
    
    def move(self,
            target_container: Optional[ui.element] = None ) -> None:

        if self.main:
            self.main.move(target_container)

        return super().move(target_container)