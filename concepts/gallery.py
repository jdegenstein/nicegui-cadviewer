"""
file: tests/*/gallery.py
file-id: efecaa60-c9ab-4bf1-a2d1-6de8ca39bec2
project:  nicegui
project-id: 56fd25a2-bb47-4f15-9f36-ca712d10743c

description: | 
    Display a gallery of images from the folder `_gallery`.
    Also generate thumbnails of 100px, 200px, and 400px.
"""
from nicegui import ui
from nicegui import app
from rich import print
from pathlib import Path
import PIL

ui.label('Gallery').classes('h1')
folder = Path(__file__).parent / '_gallery'
app.add_static_files("/temp", folder)
files = [f.name for f in folder.glob('*.png')]

def thumbnails(size):
  for file in files:
    image = PIL.Image.open(folder / file)
    # get the image size
    width, height = image.size
    print(f'{file}: {width}x{height}')
    image.thumbnail((size, size))
    (folder / f"{size}px").mkdir(exist_ok=True)
    image.save(folder / f"{size}px" / file)

thumbnails(100)
thumbnails(200)
thumbnails(400)

def show(size):
  image_container.clear()
  with image_container:
    for file in files:
      with ui.card().style('width: {size*1.2}px height: {size*1.2}px'):
        ui.image(f'/temp/{size}px/{file}').style(f'width: {size}px')
        ui.label(file)


ui.label(f'Current folder: {folder}')
with ui.row():
  ui.button('100px', on_click=lambda: show(100))
  ui.button('200px', on_click=lambda: show(200))
  ui.button('400px', on_click=lambda: show(400))

image_container = ui.row().classes('full flex items-center')
show(200)

print('running [bold blue]gallery.py[/bold blue]!')
# ui.run(native=True,title='Gallery', favicon='📸')	