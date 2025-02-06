"""

file:           scan_files.py
file-id:        56f807c7-9428-4d16-94d5-385bab9b7ccb

description: |
    Scan all files in the project.

"""
# [Imports]
from rich import print  #| [docs](https://rich.readthedocs.io/en/latest/)
from rich.pretty import pprint
from pathlib import Path #| [docs](https://docs.python.org/3/library/pathlib.html)
import hashlib        #| [docs](https://docs.python.org/3/library/hashlib.html)
from uuid import uuid4 #| [docs](https://docs.python.org/3/library/uuid.html)

# [Parameters]
P__debug = False
P__info = False
P__report = False

P__black_list = [
    ".DS_Store",
    ".git",
    ".venv",
    "__pycache__",	
    "nice123d.egg-info",
    "Z__archived",
]

P__binary_extensions = [
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".bmp",
    ".tiff",
    ".ico",
    ".svg",
    ".pdf",
    ".zip",
    ".7z",
    ".gz",
]

def generate_sha256(file_path: Path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as file:
        for byte_block in iter(lambda: file.read(4096), b""):
            sha256.update(byte_block)
    return sha256.hexdigest()

def find_file_uuid(file_path: Path):
    file_uuid = None
    if P__info:
        print(f"[bold]# Scanning {file_path}[/bold]")
    if not file_path.is_file():
        print(f"[yellow]Warning:[/yellow] {file_path} is not a file")
        return ''
    if not file_path.exists():
        print(f"[red]Error:[/red] {file_path} does not exist")
        return ''
    if file_path.suffix in P__binary_extensions:
        if P__debug:
            print(f"[blue]Info:[/blue] {file_path} is a binary file using sha256")
        return generate_sha256(file_path)

    with open(file_path, 'r', encoding="utf8") as file:
        for line in file.readlines():
            if "file-id:" in line:
                file_uuid = line.split(":")[1].strip()
                break
            if "file-id =" in line:
                file_uuid = line.split("=")[1].strip().replace('"', '')
                break
    return file_uuid

def load_template():
    readme_template = None
    if Path("./_templates/README.template.md").exists():
        with open("./_templates/README.template.md", 'r') as file:
            readme_template = file.read()
    return readme_template

def render_readme_template(template: str, data: dict):
    for key, value in data.items():
        template = template.replace(f"{{{{key}}}}", value)
    return template

def scan_files(path: Path, readme_template = None):
    file_counter = 0
    directory_counter = 0
    data = {'directories': {},
            'files': {}, 
            'file-ids': {},
            'total_files': 0, 'total_directories': 0}

    readme_data = {'folder': 'todo', 'uuid': 'todo', 'description': 'TODO: description', 'file_list': 'TODO: file_list'}

    for file in path.rglob("**"):
        is_blacklisted = False

        # Skip blacklisted files
        for black_list in P__black_list:
            if black_list in file.parts:
                is_blacklisted = True
        
        if is_blacklisted:
            continue
    
        if file.is_file():
            file_counter += 1
            file_uuid = find_file_uuid(file)
            data['files'][f'f-{file_counter:02}'] = [f'{file}', file_uuid]
            if file_uuid:
                if file_uuid in data['file-ids']:
                    print(f"[red]Warning: Duplicate UUID found in {file}[/red]")
                else:
                    data['file-ids'][file_uuid] = f'{file}'
            else:
                print(f"[yellow]Warning:[/yellow] No UUID found in {file}")
        elif file.is_dir():
            if readme_template:
                readme = file / "README.md"
                if not readme.exists():
                    readme_data['folder'] = str(file)
                    readme_data['uuid'] = str(uuid4())
                    readme_content = render_readme_template(readme_template, readme_data)
                    with open(readme, 'w') as file:
                        file.write(readme_content)
                else:
                    print(f"[blue]Info:[/blue] {readme} already exists!")
                    
            directory_counter += 1
            data['directories'][f'd-{directory_counter:02}'] = f'{file}'

    data['total_files'] = file_counter
    data['total_directories'] = directory_counter
    return data

P__run = True
if P__run:    
    if __name__ in {"__main__", "__mp_main__"}:
        readme_template = load_template()

        results = scan_files(Path("."), readme_template)
        if P__report:
            pprint(results)