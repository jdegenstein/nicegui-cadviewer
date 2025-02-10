import inspect
import logging
from dataclasses import dataclass

S_LOG_MSG_FORMAT = "%(asctime)s [%(levelname)-5.5s]  %(message)s"
logging.basicConfig(level=logging.DEBUG, format=S_LOG_MSG_FORMAT)

@dataclass
class CodeContext:
    file_name = None
    line_number = None
    positions = None
    code_context = None
    
    def __init__(self, file_name, line_number, positions, code_context):
        self.file_name = file_name
        self.line_number = line_number
        self.positions = positions
        self.code_context = code_context
    
    def __init__(self, frame_info):
        self.file_name = frame_info.filename
        self.line_number = frame_info.lineno
        self.positions = frame_info.positions
        self.code_context = frame_info.code_context
        
    def extract_code_context(self):
        return self.code_context[self.positions[0]:self.positions[1]]
    
    def __str__(self):
        return f"File: {self.file_name}:L{self.line_number}: {self.extract_code_context()}"

class ParameterGroup:
    """A context manager to capture file name and line number for the with block."""

    def __init__(self):
        self.context = None

    def __enter__(self):
        """Capture file and line number of the calling script when entering the context."""
        stack = inspect.stack()
        stack_size = len(stack)
        caller_frame = None

        for i in range(stack_size):
            print(stack[i].code_context)
            for context in stack[i].code_context:
                if context.find('ParameterGroup')>= 0:
                    caller_frame = stack[i]
                    break
                
        if caller_frame:
            self.context = CodeContext(caller_frame)
            logging.info(f"Entered 'with' block in file: {self.context}")
        
        else:
            logging.error("Stack frame not found")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the context."""
        if self.context:
            logging.info(f"Exiting 'with' block in context {self.context}")


class Parameter:
    """Represents a parameter inside the 'with' block. Captures file and line number."""

    def __init__(self, name: str, value: int):
        self.name = name
        self.value = value
        self.context = None
        self._capture_calling_context()

    def _capture_calling_context(self):
        """Capture the file name and line number where the Parameter instance is created."""
        stack = inspect.stack()
        stack_size = len(stack)
        caller_frame = None
        for i in range(stack_size):    
            print(stack[i].code_context)
            for context in stack[i].code_context:
                if context.find('Parameter')>= 0:
                    caller_frame = stack[i]
                    break
                
        if caller_frame:
            self.context = CodeContext(caller_frame)
            logging.info(f"Parameter '{self.name}'  context: {self.context}")
        
        else:
            logging.error("Stack frame not found")
        
        

def run_with_block():
    with ParameterGroup() as par_group:
        Parameter(name='a', value=1)
        Parameter(name='b', value=2)

if __name__ == '__main__':
    run_with_block()