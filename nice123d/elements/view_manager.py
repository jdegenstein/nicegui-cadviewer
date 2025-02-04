"""
TODO: docs for this file
"""

# [Imports]                                      #| description or links
from nicegui import ui                           #| [docs](https://nicegui.readthedocs.io/en/latest/)   
from elements.base_button import BaseButton      #| Base class for all buttons
from elements.base_view import BaseView          #| Base class for all views
from .constants import *                         #| The application constants
from backend.path_manager import PathManager     #| Managing file and directory handling for the application

# [Variables]

# [Main Class]
class ViewManager():

    # [Variables]
    last_button_left  = None
    last_button_right = None

    # [Constructor]
    def __init__(self, pages = None, add_zoom=False):
        ui.colors(active='#00004f',accent='#3874a0', info='#555555')
        self.pages = pages
        self.add_zoom = add_zoom
        # TODO: move default to a yaml file

        if P__experimental:
            # TODO: needs to also change th g__views
            self.left_page   = 'Meta+3' # editor
            self.right_page  = 'Meta+4' # viewer
        else:
            self.left_page   = 'Ctrl+3' # editor, restricted to left
            self.right_page  = 'Alt+3'  # viewer, restricted to right

        self.views = None 

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
        #self.pages[]

    def setup_left_button_bar(self, views : list):
        views.reverse()

        with ui.button_group() as bar:	
            self.left_button_bar = bar
            for page in self.pages:
                
                if self.pages[page].is_left:
                    active = self.pages[page]
                    active.view = views.pop()
                    
                    if 'Meta' in active.short_cut:
                        short_cut = active.short_cut.replace('Meta', 'Ctrl')
                    else: 
                        short_cut = active.short_cut
                    
                    button = BaseButton('', icon=active.icon, on_click=self.map_button_to_views[short_cut])
                    button.tooltip(f'{active.title} `{short_cut}`')
                    
                    self.pages[page].button_left = button
                    button.props('fab color=accent')
                    # INFO: `inactive` is the color from the header background color                    

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
                    active.view = views.pop()
                    
                    if 'Meta' in active.short_cut:
                        short_cut = active.short_cut.replace('Meta', 'Alt')
                    else: 
                        short_cut = active.short_cut
                    
                    button = BaseButton('', icon=active.icon, on_click=self.map_button_to_views[short_cut])
                    button.tooltip(f'{active.title} {short_cut}')
                    
                    if self.pages[page].button_left:
                        button.sibling_button = self.pages[page].button_left
                        self.pages[page].button_left.sibling_button = button 

                    self.pages[page].button_right = button   
                    
                    button.props('fab color=accent')
                    # INFO: `inactive` is the color from the header background color 
            if self.add_zoom:
                z = ui.button('', icon='zoom_out_map', on_click=self.set_zoom_right).tooltip('Zoom right `Meta+0`')
                z.props('fab color=info')

        return self.right_button_bar


    def prepare_move(self, page, side):
        page_info = None 

        # find the correct page
        for view_data in self.pages.values():
            if view_data.view == page:
                page_info = view_data
                break

        # if found highlight the buttons
        if page_info is not None:
            if side == Side.LEFT:
                self.highlight_button(page_info.button_left, side)
            else:
                self.highlight_button(page_info.button_right, side)

    def highlight_button(self, button, side):
        if type(button) is not BaseButton:
            print(f'ERROR: highlight_button: button not of type BaseButton {button}')
            return # TODO: raise exception
        if type(side) is not Side:
            print(f'ERROR: highlight_button: side not of type Side {side}')
            return # TODO: raise exception
        if side not in (Side.LEFT, Side.RIGHT):
            print(f'ERROR: highlight_button: side not in (Side.LEFT, Side.RIGHT) {side}')
            return # TODO: raise exception


        if side == Side.LEFT:        
            if button != self.last_button_left:
                button.props('fab color=active')
                if self.last_button_left:
                    self.last_button_left.props('fab color=accent')
            # else: nothing to do - keep same button active

            self.last_button_left = button

        else: # side == Side.RIGHT:        
            if button != self.last_button_right:
                button.props('fab color=active')
                if self.last_button_right:
                    self.last_button_right.props('fab color=accent')
            # else: nothing to do - keep same button active
            self.last_button_right = button  

    def show_gallery_left(self, event):
        print(f'show_gallery_left')
        self.views.show_gallery()
        self.highlight_button(self.pages["Ctrl+1"].button_left, side=Side.LEFT)
            

    def show_notes_right(self, event):
        print(f'show_notes_right')
        self.views.show_notes()
        self.highlight_button(self.pages["Alt+1"].button_right, side=Side.RIGHT)

    def show_customizer_left(self, event):
        print(f'show_customizer_left')
        self.views.show_customizer(Side.LEFT)
        self.highlight_button(self.pages["Meta+2"].button_left, side=Side.LEFT)

    def show_customizer_right(self, event):
        print(f'show_customizer_right')
        self.views.show_customizer(Side.RIGHT)
        self.highlight_button(self.pages["Meta+2"].button_right, side=Side.RIGHT)

    def show_editor_left(self, event):
        print(f'show_editor_left')
        self.views.show_editor(Side.LEFT)
        if P__experimental:
            self.highlight_button(self.pages["Meta+3"].button_left, side=Side.LEFT)
        else:
            self.highlight_button(self.pages["Ctrl+3"].button_left, side=Side.LEFT)

    def show_editor_right(self, event):
        print(f'show_editor_right')
        self.views.show_editor(Side.RIGHT)
        self.highlight_button(self.pages["Meta+3"].button_right, side=Side.RIGHT)

    def show_viewer_left(self, event):
        print(f'show_viewer_left')
        self.views.show_viewer(Side.LEFT)
        self.highlight_button(self.pages["Meta+4"].button_left, side=Side.LEFT)
    
    def show_viewer_right(self, event):
        print(f'show_viewer_right')
        self.views.show_viewer(Side.RIGHT)
        if P__experimental:
            self.highlight_button(self.pages["Meta+4"].button_right, side=Side.RIGHT)
        else:
            self.highlight_button(self.pages["Alt+3"].button_right, side=Side.RIGHT)

    def show_console_left(self, event):
        print(f'show_console_left')
        self.views.show_console(Side.LEFT)
        if P__experimental:
            self.highlight_button(self.pages["Meta+5"].button_left, side=Side.LEFT)
        else:
            self.highlight_button(self.pages["Meta+4"].button_left, side=Side.LEFT)

    def show_console_right(self, event):
        print(f'show_console_right')
        self.views.show_console(Side.RIGHT)
        if P__experimental:
            self.highlight_button(self.pages["Meta+5"].button_right, side=Side.RIGHT)
        else:
            self.highlight_button(self.pages["Meta+4"].button_right, side=Side.RIGHT)


    def show_settings_left(self, event):
        print(f'show_settings_left')
        self.views.show_settings()
        if P__experimental:
            self.highlight_button(self.pages["Ctrl+6"].button_left, side=Side.LEFT)
        else:
            self.highlight_button(self.pages["Ctrl+5"].button_left, side=Side.LEFT)


    def show_help_right(self, event):
        print(f'show_help_right')
        self.views.show_help()
        if P__experimental:
            self.highlight_button(self.pages["Alt+6"].button_right, side=Side.RIGHT)
        else:
            self.highlight_button(self.pages["Alt+5"].button_right, side=Side.RIGHT)

    def set_zoom(self, value):
        self.size_splitter.value = value        

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
