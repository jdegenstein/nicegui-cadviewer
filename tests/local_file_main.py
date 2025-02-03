#!/usr/bin/env python3
from nicegui import ui
from local_file_picker import local_file_picker
from pathlib import Path

# TODO: integrate this to be used on file_load 
# TODO: integrate light/dark mode to be used on main view
dark_mode = False

async def toggle_dark_mode() -> None:
    global dark_mode
    if dark_mode:
        await set_light_mode()
        toggle_mode.icon = 'lightbulb'
        toggle_mode.text = 'dark mode'
    else:
        await set_dark_mode()
        toggle_mode.icon = 'light_mode'
        toggle_mode.text = 'light mode'

    dark_mode = not dark_mode
    # ui.set_theme('dark' if dark_mode else 'light')

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
    active_model = relative_paths[0].replace('\\', ' / ')
    file_button.text = f'{active_model}'
    ui.notify(f'You chose {relative_paths}')

with ui.row():
    ui.icon('file').style('color: #888')
    file_button = ui.button('<no file selected>', icon='folder', on_click=pick_file).classes('text-xl font-bold').style('background: none; border: none; padding: 21px; cursor: pointer;')

file_label = ui.label('No file selected')
file_button.bind_text_to(file_label, forward=lambda text: text.replace(' / ', '\\'))

toggle_mode = ui.button('Dark mode', icon='lightbulb', on_click=toggle_dark_mode).style('margin-left: auto')
ui.run()