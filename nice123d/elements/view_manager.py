"""
TODO: docs for this file
"""

# [Imports]                                      #| description or links
from nicegui import ui                           #| [docs](https://nicegui.readthedocs.io/en/latest/)   
from elements.base_view import BaseView #| Base class for all views
from .constants import *                          #| The application constants
from backend.path_manager import PathManager   #| Managing file and directory handling for the application

# [Variables]


# [Main Class]
class ViewManager():

    # [Variables]
    
    # [Constructor]
    def __init__(self, pages = None, add_zoom=False):
        ui.colors(accent='#00006A', info='#555555')
        self.pages = pages
        self.add_zoom = add_zoom
        # TODO: move default to a yaml file

        if P__experimental:
            # TODO: needs to also change th g__pages
            self.left_page   = 'Meta+3' # editor
            self.right_page  = 'Meta+4' # viewer
        else:
            self.left_page   = 'Ctrl+3' # editor, restricted to left
            self.right_page  = 'Alt+3'  # viewer, restricted to right

        self.views = None 
        self.size_splitter = 50 # % of the screen

        if P__experimental:
            self.map_button_to_views = {
                'Ctrl+1': self.show_gallery_left,	
                'Alt+1':  self.show_notes_right,
                'Ctrl+2': self.show_customizer_left,
                'Ctrl+3': self.show_editor_left,
                'Ctrl+4': self.show_viewer_left,
                'Ctrl+5': self.show_console_left,
                'Ctrl+6': self.show_settings_left,
                'Alt+2':  self.show_customizer_right,
                'Alt+3':  self.show_editor_right,
                'Alt+4':  self.show_viewer_right,
                'Alt+5':  self.show_console_right,
                'Alt+6':  self.show_help_right,
            }
        else:
            self.map_button_to_views = {
                'Ctrl+1': self.show_gallery_left,	
                'Ctrl+2': self.show_customizer_left,
                'Ctrl+3': self.show_editor_left,
                'Ctrl+4': self.show_console_left,
                'Ctrl+5': self.show_settings_left,
                'Alt+1':  self.show_notes_right,
                'Alt+2':  self.show_customizer_right,
                'Alt+3':  self.show_viewer_right,
                'Alt+4':  self.show_console_right,
                'Alt+5':  self.show_help_right,
            }
  
    def setup(self, views):
        self.views = views

    def setup_left_button_bar(self, views : list):
        views.reverse()

        with ui.button_group() as bar:	
            self.left_button_bar = bar
            for page in self.pages:
                print(page)
                if self.pages[page].is_left:
                    active = self.pages[page]
                    active.page = views.pop()
                    
                    if 'Meta' in active.short_cut:
                        short_cut = active.short_cut.replace('Meta', 'Ctrl')
                    else: 
                        short_cut = active.short_cut
                    
                    button = ui.button('', icon=active.icon, on_click=self.map_button_to_views[short_cut])
                    button.tooltip(f'{active.title} `{short_cut}`')

                    if active.title == self.left_page:
                        button.props('fab color=accent')
            if self.add_zoom:
                z = ui.button('', icon='zoom_out_map', on_click=self.set_zoom_left).tooltip('Zoom left `Meta+0`')
                z.props('fab color=info')

        return self.left_button_bar

    def setup_right_button_bar(self, views : list):
        views.reverse()
        
        with ui.button_group() as bar:	
            self.right_button_bar = bar
            for page in self.pages:
                if self.pages[page].is_right:
                    active = self.pages[page]                    
                    active.page = views.pop()
                    
                    if 'Meta' in active.short_cut:
                        short_cut = active.short_cut.replace('Meta', 'Alt')
                    else: 
                        short_cut = active.short_cut
                    
                    button = ui.button('', icon=active.icon, on_click=self.map_button_to_views[short_cut])
                    button.tooltip(f'{active.title} {short_cut}')
                    
                    
                    if active.title == self.right_page:
                        button.props('fab color=accent')
        
            if self.add_zoom:
                z = ui.button('', icon='zoom_out_map', on_click=self.set_zoom_right).tooltip('Zoom right `Meta+0`')
                z.props('fab color=info')

        return self.right_button_bar

    def show_gallery_left(self, event):
        print(f'show_gallery_left')
        self.views.show_gallery()

    def show_notes_right(self, event):
        print(f'show_notes_right')
        self.views.show_notes()

    def show_customizer_left(self, event):
        print(f'show_customizer_left')
        self.views.show_customizer(Side.LEFT)

    def show_customizer_right(self, event):
        print(f'show_customizer_right')
        self.views.show_customizer(Side.RIGHT)

    def show_editor_left(self, event):
        print(f'show_editor_left')
        self.views.show_editor(Side.LEFT)

    def show_editor_right(self, event):
        print(f'show_editor_right')
        self.views.show_editor(Side.RIGHT)
    
    def show_viewer_left(self, event):
        print(f'show_viewer_left')
        self.views.show_viewer(Side.LEFT)
    
    def show_viewer_right(self, event):
        print(f'show_viewer_right')
        self.views.show_viewer(Side.RIGHT)

    def show_console_left(self, event):
        print(f'show_console_left')
        self.views.show_console(Side.LEFT)

    def show_console_right(self, event):
        print(f'show_console_right')
        self.views.show_console(Side.RIGHT)


    def show_settings_left(self, event):
        print(f'show_settings_left')
        self.views.show_settings()

    def show_help_right(self, event):
        print(f'show_help_right')
        self.views.show_help()

    def set_zoom_left(self):
        if self.size_splitter.value == 100:
            self.size_splitter.value = 50
        elif self.size_splitter.value < 50:
            self.size_splitter.value = 50
        else: # self.size_splitter.value >= 50:
            self.size_splitter.value = 100

    def set_zoom_right(self):
        if self.size_splitter.value == 0:
            self.size_splitter.value = 50
        elif self.size_splitter.value > 50:
            self.size_splitter.value = 50
        else: # self.size_splitter.value <= 50:
            self.size_splitter.value = 0

    def left(self):
        if self.size_splitter.value < 50:
            self.size_splitter.value = 50
        elif self.size_splitter.value < 100:
            self.size_splitter.value = 100
        else:
            self.size_splitter.value = 50

    def right(self):
        if self.size_splitter.value > 50:
            self.size_splitter.value = 50
        elif self.size_splitter.value == 50:
            self.size_splitter.value = 0
        else:
            self.size_splitter.value = 50

    def ensure_left_visible(self):
        if self.size_splitter.value < 50:
            self.size_splitter.value = 50

    def ensure_right_visible(self):
        if self.size_splitter.value > 50:
            self.size_splitter.value = 50
