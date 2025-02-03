from nicegui import ui

def handle_upload(files):
    for file in files:
        ui.notify(f'Uploaded file: {file.name}')

def open_file_dialog():
    file_input = ui.file_input(on_change=lambda e: handle_upload(e['files']))
    file_input.click()

ui.button('Load File', on_click=open_file_dialog)

ui.run()