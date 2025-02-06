#!/usr/bin/env python3
from nicegui import ui
from local_file_picker import local_file_picker
from pathlib import Path

dark_mode = False
grid = None 

async def toggle_dark_mode() -> None:
    global dark_mode
    global grid
    dark_mode = not dark_mode
    if dark_mode:
        await set_dark_mode()
        toggle_mode.icon = 'light_mode'
        toggle_mode.text = 'light mode'
        ui.query('body').classes('dark')
        grid.classes('dark-mode-grid')
    else:
        await set_light_mode()
        toggle_mode.icon = 'lightbulb'
        toggle_mode.text = 'dark mode'
        ui.query('body').remove_class('dark')
        grid.remove_class('dark-mode-grid')

async def set_dark_mode():
    ui.run_javascript('''
        Quasar.Dark.set(true);
        tailwind.config.darkMode = 'class';
        document.documentElement.classList.add('dark');
                            
        ''', timeout=1000)
    
async def set_light_mode():
    ui.run_javascript('''
        Quasar.Dark.set(false);
        tailwind.config.darkMode = 'class';
        document.documentElement.classList.add('dark');
                        
        ''', timeout=1000)

async def pick_file() -> None:
    base_path = Path(__file__).parent.parent
    result = await local_file_picker(str(base_path), multiple=True)
    relative_paths = [str(Path(file).relative_to(base_path)) for file in result]
    active_model = relative_paths[0].replace('\\', '/')
    file_label.text = f'{active_model}'
    ui.notify(f'You chose {relative_paths}')

ui.button('Choose file', on_click=pick_file, icon='folder')
file_label = ui.label('No file chosen').classes('text-2xl font-bold')
toggle_mode = ui.button('Toggle dark mode', on_click=toggle_dark_mode, icon='lightbulb')



# ui.run()