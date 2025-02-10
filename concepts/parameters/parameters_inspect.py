import inspect
import logging

S_LOG_MSG_FORMAT = "%(asctime)s [%(levelname)-5.5s]  %(message)s"
logging.basicConfig(level=logging.DEBUG, format=S_LOG_MSG_FORMAT)

class ParameterGroup:
    """A context manager to capture file name and line number for the with block."""

    def __init__(self):
        self.filename = None
        self.line_number = None

    def __enter__(self):
        """Capture file and line number of the calling script when entering the context."""
        stack = inspect.stack()
        caller_frame = stack[1]  # The caller of __enter__ is the 'with' statement
        self.filename = caller_frame.filename
        self.line_number = caller_frame.lineno
        logging.info(f"Entered 'with' block in file: {self.filename} at line {self.line_number}")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the context."""
        logging.info(f"Exiting 'with' block in file: {self.filename} at line {self.line_number}")


class Parameter:
    """Represents a parameter inside the 'with' block. Captures file and line number."""

    def __init__(self, name: str, value: int):
        self.name = name
        self.value = value
        self.filename = None
        self.line_number = None
        self._capture_calling_context()

    def _capture_calling_context(self):
        """Capture the file name and line number where the Parameter instance is created."""
        stack = inspect.stack()
        caller_frame = stack[1]  # The caller of __init__ is where Parameter is instantiated
        self.filename = caller_frame.filename
        self.line_number = caller_frame.lineno
        logging.info(f"Parameter '{self.name}'  file: {self.filename} at line {self.line_number}")


def run_with_block():
    with ParameterGroup() as par_group:
        Parameter(name='a', value=1)
        Parameter(name='b', value=2)

if __name__ == '__main__':
    run_with_block()