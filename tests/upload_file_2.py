from nicegui import app, ui

async def choose_file():
    files = await app.native.main_window.create_file_dialog(allow_multiple=True)
    for file in files:
        ui.notify(file)

ui.button('choose file', on_click=choose_file)

ui.run(native=True)