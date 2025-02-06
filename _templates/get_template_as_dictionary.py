"""
file:        _templates/get_template_as_dictionary.py
file-id:     72e195ed-55b1-4ec3-be2b-b0ad9f5c887b
project:     nice123d
project-id:  e2bbd03f-0ac6-41ec-89ae-2ad52fa0652a
description: Get a template as a dictionary.

"""
# [Imports]
from pathlib import Path

# [Parameters]

# [Functions]
def main(file: Path):
    template = {}
    with open(file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            while line.find('{{')>=0 and line.find('}}')>0:
                key = line.split('{{')[1].split('}}')[0]
                line = line.split('}}')[1]
                template[key] = 'todo'

    with open('README.dictionary.py', 'w') as f:
        f.write(str(template))
    return template

P__run = False
if P__run:
    if __name__ in {"__main__", "__mp_main__"}:
        main(Path('./README.template.md'))