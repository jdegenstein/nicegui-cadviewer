import pytest
from parameter_group import ParameterGroup
from parameters import *

def test_parameter_creation():
    param = Parameter(name="test_param", parameter_type="string", value="test_value")
    assert param.name == "test_param"
    assert param.the_type == "string"
    assert param.value == "test_value"

def test_parameter_group_with_block():
    with ParameterGroup('P') as pg:
        param1 = Parameter(name="param1", parameter_type="string", value="value1")
        param2 = Parameter(name="param2", parameter_type="int", value=42)
        assert param1 in pg.parameters
        assert param2 in pg.parameters
        assert ParameterGroup.get_current_instance() is pg
    
    assert ParameterGroup.get_current_instance() is None
    
    

def test_parameter_group_outside_with_block():
    pg = ParameterGroup()
    param = Parameter(name="param_outside", parameter_type="string", value="value_outside")
    assert param not in pg.parameters

if __name__ == '__main__':
    pytest.main()