import ast
import operator as op
from math import sqrt, sin, cos, tan, log, exp

"""
    description:    This script is used to inspect the parameter definitions | 
                    and extract the class, name, value, calc, description, and help.
    
    Raises:
        ValueError: if the value is not the type defined by the class.
        ValueError: if the class is not recognized.
"""

# This will define the global variables in the model's script
m = 42 

# This will be the input from from the model's script file
parameter_definitions = [
    'a = IntegerParameter("one", calc=int(m/2))',
    "b = IntegerParameter('two', calc=sqrt(a*2))",
    'IntegerParameter(name="three", calc=a+b, description="This is the third parameter")',
    'IntegerParameter("four", value=4, description="This is the fourth parameter")',
    'StringParameter("five", value="alpha", help="This is the help")',
]

g__variables = {}

# Supported operators and functions
SAFE_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.BitXor: op.xor,
    ast.USub: op.neg,
    'sqrt': sqrt,
    'sin': sin,
    'cos': cos,
    'tan': tan,
    'log': log,
    'exp': exp,
    'int': int,
    'float': float,
    'str': str,
}

def safe_eval(node, variables):
    """Safely evaluate an AST node."""
    if isinstance(node, ast.Num):  # <number>
        return node.n
    elif isinstance(node, ast.Str):  # <string>
        return node.s
    elif isinstance(node, ast.Name):
        if node.id in variables:
            return variables[node.id]
        elif node.id in SAFE_OPERATORS:
            return SAFE_OPERATORS[node.id]
        else:
            raise ValueError(f"Use of undefined variable or function '{node.id}'")
    elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
        left = safe_eval(node.left, variables)
        right = safe_eval(node.right, variables)
        return SAFE_OPERATORS[type(node.op)](left, right)
    elif isinstance(node, ast.UnaryOp):  # <operator> <operand> e.g., -1
        operand = safe_eval(node.operand, variables)
        return SAFE_OPERATORS[type(node.op)](operand)
    elif isinstance(node, ast.Call):  # function call
        func = safe_eval(node.func, variables)
        args = [safe_eval(arg, variables) for arg in node.args]
        return func(*args)
    else:
        raise TypeError(node)

def evaluate_expression(expr):
    """Evaluate an expression using the globals() and g__variables dictionaries."""
    merged_globals = {**globals(), **g__variables}
    node = ast.parse(expr, mode='eval').body
    result = safe_eval(node, merged_globals)
    print(f'>>>> Expression: {expr}, Result: {result}')
    return result

def do_inspect(code):
    """Inspect the code object and return the class, name, value, calc, and variable name if assigned."""
    global g__variables
    
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            # Handle assignment
            variable_name = node.targets[0].id
            value_node = node.value
        else:
            variable_name = None
            value_node = node
            
        if isinstance(value_node, ast.Call):
            classname = value_node.func.id
            name = None
            value = None
            calc = None
            description = None
            help = None
            
            # Process named keywords
            for keyword in value_node.keywords:
                if keyword.arg == 'name':
                    name = keyword.value.s
                elif keyword.arg == 'value':
                    value = evaluate_expression(ast.unparse(keyword.value))
                elif keyword.arg == 'calc':
                    calc = ast.unparse(keyword.value)
                    value = evaluate_expression(calc)
                    print(f'>>>> Calc: {calc}, Value: {value}')    
                elif keyword.arg == 'description':
                    description = keyword.value.s
                elif keyword.arg == 'help':
                    help = keyword.value.s
                else:
                    print(f'Unknown keyword: {keyword.arg}')
                    
            # Process unnamed keywords    
            if not name:
                if len(value_node.args) > 0:
                    name = value_node.args[0].s
            
            if not value and not calc:
                if len(value_node.args) > 1:
                    value = evaluate_expression(ast.unparse(value_node.args[1]))
                
                print(f'{type(value)}')
            
            if not description:
                if len(value_node.args) > 2:
                    description = value_node.args[2].s
            
            if not help:
                if len(value_node.args) > 3:
                    help = value_node.args[3].s
                    
            # process type check from classname and value
            if classname == 'IntegerParameter':
                if not isinstance(value, int):
                    value = int(value)
                    if not isinstance(value, int):
                        raise ValueError(f'Value {value} is not an integer')
            elif classname == 'StringParameter':
                if not isinstance(value, str):
                    raise ValueError(f'Value {value} is not a string')
            else:
                raise ValueError(f'Unknown class: {classname}')
            
            if variable_name:
                g__variables[variable_name] = value
                if 0: # this would add the variables in the with block to the global namespace
                    globals()[variable_name] = value 
            
            return variable_name, classname, name, value, calc, description, help

class IntegerParameter:
    """Represents an integer parameter with an optional calculation expression."""

    def __init__(self, name: str, value: int = None, calc: str = None, description: str = None):
        self.name = name
        self.value = value
        self.calc = calc
        self.description = description

        if calc:
            self.value = evaluate_expression(calc)

# inspect the given lines as code
for line in parameter_definitions:
    print(f"Inspecting: {line}")
    result = do_inspect(line)
    if result:
        variable_name, classname, name, value, calc, description, help = result
        print(f'# Variable: {variable_name}, Class: {classname}, Name: {name}, Value: {value}, Calc: {calc}')
        print(f'- Description: {description}\n- Help: {help}')