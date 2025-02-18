"""
Parameter 
-> [n] Parameters

file:           nice123d/backend/parameters.py
file-id:        ed47d2f1-7046-4a40-972b-5f9ab271f48e
project:        nice123d
project-id:     e2bbd03f-0ac6-41ec-89ae-2ad52fa0652a
author:         felix@42sol.eu

description: |
    This class implements the parameter objects used in customizer.

"""

# [Imports]                                      #| description or links
from dataclasses import dataclass                #| [docs](https://docs.python.org/3/library/dataclasses.html)
from typing import Any                           #| [docs](https://docs.python.org/3/library/typing.html)
from rich import print                           #| [docs](https://rich.readthedocs.io/en/latest/)
from enum import Enum                            #| [docs](https://docs.python.org/3/library/enum.html)
from backend.parameter_group import ParameterGroup

# [Types]

class ParameterType(Enum):
    """
    Enum for the parameter types.
    """
    BOOL = "bool"
    INT = "int"
    FLOAT = "float"
    ENUM = "enum"
    STRING = "string"
    LIST = "list"
    DICT = "dict"

# [Base Class]


@dataclass
class Parameter():
    """
    Parameter keeps track of the parameters for the customizer.
    """
    name: str
    value: Any
    description: str = None
    help: str = None

    def __post_init__(self):
        if self.help:
            print(f"[INFO] {self.name} : {self.help}")
        else:
            print(f"[INFO] {self.name} : {self.description}")
            
    def __init__(self, name, parameter_type, value, description=None, help=None, validator=None):
        self._name = name
        self._value = value
        self._type = parameter_type
        self._description = description
        self._help = help
        self._validator = validator

        # Access the current ParameterGroup instance
        current_group = ParameterGroup.get_current_instance()
        if current_group:
            current_group.parameters.append(self)
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        if type(value) != self._type:
            raise ValueError(f"can not set value, because value for {name} is not a {parameter_type}")
        
        self._value = value
        
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name
        
    @property
    def the_type(self):
        return self._type
    
    @the_type.setter
    def the_type(self, a_type):
        if type(value) != a_type:
            raise ValueError(f"can not set type, because value for {name} is not a {type}")
        self._type = a_type
        
    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        if type(description) != str:
            raise ValueError(f"can not set description, because description for {name} is not a string")
        self._description = description
    
    @property
    def help(self):
        return self._help
    
    @help.setter
    def help(self, help):
        if type(help) != str:
            raise ValueError(f"can not set help, because help for {name} is not a string")
        self._help = help
    
    @property
    def validator(self):
        return self._validator

    @validator.setter
    def validator(self, validator):
        if not callable(validator):
            raise TypeError(f"can not set validator, because validator for {name} is not a function")
        
        self._validator = validator
    
    def __str__(self):
        return f"{self._name} : {self._value}"
    
class StringParameter(Parameter):
    """
    String parameter
    """
    def __init__(self, name, value, description=None, help=None, validator=None):
        if type(value) != str:
            raise ValueError(f"Value for {name} is not a string")

        super().__init__(name, ParameterType.STRING, value, description, help, validator)
    
class IntParameter(Parameter):
    """
    Int parameter
    """
    def __init__(self, name, value, description=None, help=None, validator=None):
        if type(value) != int:
            raise ValueError(f"Value for {name} is not an integer")
        
        super().__init__(name, ParameterType.INT, value, description, help, validator)
        
class FloatParameter(Parameter):
    """
    Float parameter
    """
    def __init__(self, name, value, description=None, help=None, validator=None):
        if type(value) != float:
            raise ValueError(f"Value for {name} is not a float")
        
        super().__init__(name, ParameterType.FLOAT, value, description, help, validator)

class BoolParameter(Parameter):
    """
    Bool parameter
    """
    def __init__(self, name, value, description=None, help=None, validator=None):
        if type(value) != bool:
            raise ValueError(f"Value for {name} is not a boolean")
        
        super().__init__(name, ParameterType.BOOL, value, description, help, validator)

class EnumParameter(Parameter):
    """
    Enum parameter
    """
    
    def __init__(self, name, value, enum_type, description=None, help=None):
        # check if a Enum class was passed in `enum_type`
        found_enum = False
        for base in enum_type.__bases__:
            print(f'{base=}')
            if base == Enum:
                found_enum = True
                break   # found the Enum class
        if not found_enum:
            raise TypeError(f"Enum type for {name} is not an Enum class {enum_type}")
        
        if value not in enum_type:
            raise ValueError(f"Value for {name} is not in the enum")
        super().__init__(name, ParameterType.ENUM, value, description, help)
        
        self.enum_type = enum_type
        
class ListParameter(Parameter):
    """
    List parameter
    """
    def __init__(self, name, value, description=None, help=None, validator=None):
        if type(value) != list:
            raise ValueError(f"Value for {name} is not a list")
        super().__init__(name, ParameterType.LIST, value, description, help, validator)

class DictParameter(Parameter):
    """
    Dict parameter
    """
    def __init__(self, name, value, description=None, help=None, validator=None):
        if type(value) != dict:
            raise ValueError(f"Value for {name} is not a dictionary")
        super().__init__(name, ParameterType.DICT, value, description, help, validator)

if __name__ == '__main__':
    a = StringParameter('test_string', 'test', 'test description', 'test help')
    b = IntParameter('test_int', 1, 'test description', 'test help')
    c = FloatParameter('test_float', 1.0, 'test description', 'test help')
    d = BoolParameter('test_string', True, 'test description', 'test help')
    e = EnumParameter('test_enum', 'bool', ParameterType, 'test description', 'test help')
    print(f'{a=}')
    print(f'{b=}')
    print(f'{c=}')
    print(f'{d=}')
    print(f'{e=}')