import ast

parameter_definitions = [
    'a = IntegerParameter("one", 12)',
    "IntegerParameter('two', value=2*a)",
    'IntegerParameter(name="three", value=3)',
    'IntegerParameter("four", value=4, description="This is the fourth parameter")',
    'StringParameter("five", value="12", help="This is the help")',
]

variables = {}

def do_inspect(code):
    """Inspect the code object and return the class, name, value, and variable name if assigned."""
    global variables
    
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            # Handle assignment
            variable_name = node.targets[0].id
            node = node.value
        else:
            variable_name = None
            
        if isinstance(node, ast.Call):
            classname = node.func.id
            name = None
            value = None
            description = None
            help = None
            
            # Process named keywords
            for keyword in node.keywords:
                if keyword.arg == 'name':
                    name = keyword.value.s
                elif keyword.arg == 'value':
                    value = keyword.value.n
                elif keyword.arg == 'description':
                    description = keyword.value.s
                elif keyword.arg == 'help':
                    help = keyword.value.s
                else:
                    print(f'Unknown keyword: {keyword.arg}')
                    
            # Process unnamed keywords    
            if not name:
                if len(node.args) > 0:
                    name = node.args[0].s
            
            if not value:
                if len(node.args) > 1:
                    value = node.args[1].n
                
                print(f'{type(value)}')
            
            if not description:
                if len(node.args) > 2:
                    description = node.args[2].s
            
            if not help:
                if len(node.args) > 3:
                    help = node.args[3].s
                    
            # process type check from classname and value
            if classname == 'IntegerParameter':
                if not isinstance(value, int):
                    raise ValueError(f'Value {value} is not an integer')
            elif classname == 'StringParameter':
                if not isinstance(value, str):
                    raise ValueError(f'Value {value} is not a string')
            else:
                raise ValueError(f'Unknown class: {classname}')
            
            if variable_name:
                variables[variable_name] = value
            
            return variable_name, classname, name, value, description, help

# inspect the given lines as code
for line in parameter_definitions:
    print(f"Inspecting: {line}")
    result = do_inspect(line)
    if result:
        variable_name, classname, name, value, description, help = result
        print(f'# Variable: {variable_name}, Class: {classname}, Name: {name}, Value: {value}')
        print(f'- Description: {description}\n- Help: {help}')