"""
ParameterGroup 
-> [n] Parameters

file:           nice123d/backend/parameter_groups.py
file-id:        b312b568-57c4-489a-9f0c-8f6caf7ad998
project:        nice123d
project-id:     e2bbd03f-0ac6-41ec-89ae-2ad52fa0652a
author:         felix@42sol.eu

description: |
    This class implements the group for the parameter objects used in customizer.

"""
# [Imports]                                      #| description or links 
from pathlib import Path                         #| [docs](https://docs.python.org/3/library/pathlib.html)
import os 

# [Variables]

# [Main Class]

class ParameterGroup:
    """
    ParameterGroup keeps track of the parameters for the customizer using a with block statement.
    """
    
    _current_instance = None

    def __init__(self, name: str = 'P', parameters: list = None) -> 'ParameterGroup':
        self.name = name
        self.parameters = parameters or []
        globals()[self.name] = self  # Add the parameter group as a global variable
        

    def __enter__(self):
        # Code to execute when entering the with block
        print("Entering the with block")
        ParameterGroup._current_instance = self
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Code to execute when exiting the with block
        print("Exiting the with block")
        ParameterGroup._current_instance = None
        # Handle exceptions if necessary
        if exc_type:
            print(f"An exception occurred: {exc_value}")
        return False  # Do not suppress exceptions

    def add_parameter(self, parameter):
        self.parameters.append(parameter)
        setattr(self, parameter.name, parameter.value)
        print(f">>>> Added parameter {parameter.name} to {self.name}")	

    def __getattr__(self, name):
        for parameter in self.parameters:
            if parameter.name == name:
                
                return parameter.value
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    @classmethod
    def get_current_instance(cls):
        return cls._current_instance

# Example usage
if __name__ == '__main__':
    from parameters import Parameter                         #| [local](./parameters.py)

    with ParameterGroup('P') as pg:
        param1 = Parameter(name="param1", parameter_type="string", value="value1")
        param2 = Parameter(name="param2", parameter_type="int", value=42)
        pg.add_parameter(param1)
        pg.add_parameter(param2)
    print(P.param1)  # Output: value1
    print(P.param2)  # Output: 42
    print(dir(P))  # Access via global variable
    print(globals())  # Output: value1