"""
TODO: docs for this file
"""

# [Imports]
from nicegui import ui      # [docs](https://nicegui.readthedocs.io/en/latest/)   
from constants import *
from datetime import datetime
import time

# [Main Class]
class BaseView(ui.element):
    
    # [Variables]
    logger_available = False    # Whether the logger is available
    main = None                 # The main ui element
    
    # [Constructor]
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_time = {}

    # [API]
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
