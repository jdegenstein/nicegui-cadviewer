
"""
generate_code

file:           scripts/generate_code.py
file-id:        ab805102-0d4a-4126-8b40-862cb9560d39
project:        nice123d
project-id:     e2bbd03f-0ac6-41ec-89ae-2ad52fa0652a
author:         felix@42sol.eu

description: |
    This script can generate dataclasses from yaml files.  It is used to generate the settings data classes.
    call hint:
        python scripts/generate_code.py {input_folder} {output_folder}
"""

import yaml
from pathlib import Path
import click
from typing import Any, Dict
from rich import  print 



P__file_head_defaults = {
    "class_name": "TOOD: Add class name",
    "file": "TODO: add file name",
    "file-id": "TODO: add uuid",
    "project": "nice123d",
    "project-id": "e2bbd03f-0ac6-41ec-89ae-2ad52fa0652a",
    "author": "felix@42sol.eu"
}

def generate_file_head(data: Dict[str, Any]) -> str:
    """Generate the file head."""    
    file_head = '"""\n'
    
    # check for necessary keys
    for key in P__file_head_defaults.keys():
        if key not in data:
            data[key] = P__file_head_defaults[key]
    
    file_head += f"  {data.pop('class_name')} -> @dataclass \n\n"
    
    for key, value in data.items():
        file_head += f"{key:20}: {value}\n"
    file_head += '"""\n\n'
    
    return file_head

def filter_dictionary(data: Dict[str, Any], prefix: str, flatten : bool=False) -> Dict[str, Any]:
    """Filter a dictionary by prefix and flatten the hierarchy."""
    result = {}
    file_head = '"""\n'
    file_data = {}
        
    class__name = 'Config'
    for key in list(data.keys()):
        if key.startswith('_'):
            if key == '_class_name':
                class_name = data[key]
                file_data[key[1:]] = data[key]
            else:   
                file_data[key[1:]] = data[key]
            data.pop(key)
            continue
        
    file_head = generate_file_head(file_data)
    
    if flatten:    
        for key in list(data.keys()):
            element = data[key]
            if type(element) == dict:
                for sub_key in element.keys():
                    data[f'{key}__{sub_key}'] = element[sub_key]
                data.pop(key)

    return data, file_head, class_name


def create_dataclass_from_yaml(yaml_file):
    with open(yaml_file, 'r') as file:
        yaml_data = yaml.safe_load(file)
    
    yaml_data, file_head, class_name = filter_dictionary(yaml_data, '_', flatten=True)
    
    fields = "\n".join([f"    {key}: {type(value).__name__}" for key, value in yaml_data.items()])
    class_data = f"@dataclass\nclass {class_name}:\n{fields}\n"
    return class_data, file_head, class_name

def file_name(class_name):
    
    for position, character in enumerate(class_name):
        if character.isupper() and position != 0:
            class_name = class_name.replace(character, f"_{character}")
            
    return class_name.lower()


def create_dataclass_source_file(yaml_file, output_dir):
    class_data, file_head, class_name = create_dataclass_from_yaml(yaml_file)
    
    output_file = Path(output_dir) / f"{file_name(class_name)}.py"
    with output_file.open('w') as f:
        f.write(file_head)
        f.write('from dataclasses import dataclass\n\n')
        f.write(class_data)

@click.command()
@click.argument("file",   type=click.Path(exists=True))
@click.argument("output", type=click.Path(), default="./out")
def main(file, output):
    if not Path(output).exists():
        Path(output).mkdir(parents=True)
    
    for file in Path(file).rglob("*.yaml"):
        print(f'Processing {file}')
        create_dataclass_source_file(file, output)
        
if __name__ == "__main__":
    main()