from nicegui import ui
from nicegui import app
from pathlib import Path 

def load_directory(path='.'):
    items = Path(path).iterdir()
    table.rows = [{"name": i.name, "type": "Folder" if i.is_dir() else "File", "path": str(i)} for i in items]
    table.update()

def on_row_clicked(event):
    row_index = event[-1]
    ui.notify(f"Cell clicked: {row_index}")
    # get the row data
    if table.row[row_index][1] == 'Folder':
        path = path / table.row[row_index][0]
        table.clear()
        table.columns = columns
        load_directory( path)
        
    else:
        ui.notify(f"File clicked: {table.row[row_index][0]}")

ui.button('Load directory', on_click=lambda: load_directory('.'))
ui.label('Files:')

columns = [
        {"headerName": "Name", "field": "name", 'filter': 'agTextColumnFilter', 'floatingFilter': True},
        {"headerName": "Type", "field": "type", 'filter': 'agTextColumnFilter', 'floatingFilter': True},
    ]

rows = []

table = ui.table(columns=columns, rows=rows, row_key='name') \
    .on('rowClick', on_row_clicked)

ui.run(native=True, title='Browse', favicon='📂')
