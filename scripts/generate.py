"""
file:           generate.py
file-id:        d0e47a6e-ea29-465a-a0b6-6d71093b72d9

description: |
    Scan all files in the project.
    
"""

import yaml                             #| [docs](https://pyyaml.org/wiki/PyYAMLDocumentation)
from dataclasses import make_dataclass  #| [docs](https://docs.python.org/3/library/dataclasses.html)	
from typing import Any, Dict            #| [docs](https://docs.python.org/3/library/typing.html)
import click                            #| [docs](https://click.palletsprojects.com/en/8.0.x/)
from pathlib import Path                #| [docs](https://docs.python.org/3/library/pathlib.html)

def create_dataclass(class_name: str, data: Dict[str, Any]):
    """Dynamically create a dataclass from a dictionary."""
    fields = [(key, type(value), value) for key, value in data.items()]
    return make_dataclass(class_name, fields)

def filter_dictionary(data: Dict[str, Any], prefix: str, flatten=False):
    """Filter a dictionary by prefix and flatten the hierarchy."""
    result = {}
    for key in list(data.keys()):
        if key.startswith('_'):
            data.pop(key)
            continue
    
    if flatten:    
        for key in list(data.keys()):
            data = data[key]
            if type(data) == dict:
                for sub_key in data.keys():
                    yaml_data[f'{key}__{sub_key}'] = data[sub_key]
                data.pop(key)

    return data
    

def create_dataclass_from_yaml(yaml_file: str, class_name: str):
    """Create a dataclass from a YAML file."""
    with open(yaml_file, "r", encoding="utf-8") as file:
        yaml_data = yaml.safe_load(file)


    # remove the keys with `_` in the yaml
    # and flatten hierarchy
    yaml_data = filter_dictionary(yaml_data, '_', flatten=True)
        
    # Generate dataclass dynamically
    class_test = create_dataclass(class_name, yaml_data)
    config = class_test(**yaml_data)
    return config


@click.command()
@click.argument("file",   type=click.Path(exists=True))
@click.argument("output", type=click.Path())
def main(file, output):    
    """Scan all files in the project.
    
    param file:   The file to work with.
    param output: The output folder, names will be defined from the input file name.
    
    """
    print(f"Scanning files in {file} and writing output to {output}")
    for file in Path(file).rglob("*.yaml"):
        print(f'Processing {file}')
        class_data = create_dataclass_from_yaml(file, f'{file.stem}Config')
        
        with( Path(output) / f'{file.stem}_config.py').open('w') as f:
            f.write(f'from dataclasses import dataclass\n\n')
            f.write(class_data)

if __name__ == "__main__":
    main()