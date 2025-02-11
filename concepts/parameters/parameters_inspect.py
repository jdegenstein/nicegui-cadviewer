import inspect
import logging
from dataclasses import dataclass
from re import compile

S_LOG_MSG_FORMAT = "%(asctime)s [%(levelname)-5.5s]  %(message)s"
logging.basicConfig(level=logging.DEBUG, format=S_LOG_MSG_FORMAT)

re_group = compile(r"ParameterGroup\(\s*(?P<object_name>name=\s*|)(?P<name>.+)")
re_parameter = compile(r"(?P<type>[A-z]+)Parameter\(\s*(?P<object_name>name=\s*|)(?P<name>['\"]{1}.+['\"]{1}),\s*(?P<value_name>value=\s*|)(?P<value>.+)\s*[,)]")

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
        self.code_context = code_context[0][0]
    
    def __init__(self, frame_info):
        self.file_name = frame_info.filename
        self.line_number = frame_info.lineno
        self.positions = frame_info.positions
        self.code_context = frame_info.code_context[0]
        
    def update_group_name(self, name):
        line = self.code_context
        
        if re_group.match(line):
            match = re_group.match(line)
            if match:
                line.replace(match.group('name'), f"{name}")

        return line
        

    def update_parameter_value(self, new_value):
        line = self.code_context
        print(f'>>> {line}')
        if re_parameter.match(line):
            match = re_parameter.match(line)
            if match:
                line.replace(match.group('value'), f"{new_value}")
            else:
                logging.error(f"Parameter not found in line: {line}")
        else:
            logging.error(f"Parameter not found in line: {line}")
        return line
    
    def __str__(self):
        return f"File: {self.file_name}:L{self.line_number}"

class CodeFile:
    def __init__(self, file_name):
        self.file_name = file_name
        self.data = None
        self._read_file()
    
    def _read_file(self):
        with open(self.file_name, 'r') as file:
            self.data = file.readlines()
    
    def update_line(self, line_number, new_line):
        self.data[line_number-1] = new_line
    
    def save_file(self):
        with open(self.file_name, 'w') as file:
            file.writelines(self.data)
    def __str__(self):
        return f"File: {self.file_name}"
    
    def __repr__(self):
        return self.__str__()
class ParameterGroup:
    """A context manager to capture file name and line number for the with block."""
    context = None
    
    @classmethod
    def get_context(classname):
        return classname.context

    @classmethod
    def set_context(classname, context):
        classname.context = context
        
    def __init__(self, name: str):
        self.name = name
        self.context = None
        self._file = None
        self._parameters = []

    def __enter__(self):
        """Capture file and line number of the calling script when entering the context."""
        ParameterGroup.set_context(self)
        stack = inspect.stack()
        stack_size = len(stack)
        caller_frame = None

        for i in range(stack_size):
            for context in stack[i].code_context:
                if context.find('ParameterGroup')>= 0:
                    caller_frame = stack[i]
                    break
                
        if caller_frame:
            self.context = CodeContext(caller_frame)
            self._file = CodeFile(self.context.file_name) 
            logging.info(f"Entered 'with' block in file: {self.context}")
        
        else:
            logging.error("Stack frame not found")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the context."""
        if self.context:
            logging.info(f"Exiting 'with' '{self.name}'\n    block in context {self.context}")
            
            line = self.context.update_group_name('one_1')
            line = line.replace(self.name, f"{self.name}_1")
            self._file.update_line(self.context.line_number, f"{line}")
            for parameter in self._parameters:
                print(f"Parameter: {parameter.name} = {parameter.value}")
                parameter.new_value = 42
                line = parameter.context.update_parameter_value(42)
                self._file.update_line(parameter.context.line_number, f"{line}")
            self._file.save_file()            


class IntegerParameter:
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
            for context in stack[i].code_context:
                if context.find('Parameter')>= 0:
                    caller_frame = stack[i]
                    break
                
        if caller_frame:
            self.context = CodeContext(caller_frame)
            ParameterGroup.get_context()._parameters.append(self)
            logging.info(f"Parameter '{self.name}'  context: {self.context}")
        
        else:
            logging.error("Stack frame not found")
        
        

def run_with_block():
    with ParameterGroup('A_1_1_1') as par_group:
        IntegerParameter(name='a', value=1)
        IntegerParameter(name='b', value=2)

if __name__ == '__main__':
    run_with_block()