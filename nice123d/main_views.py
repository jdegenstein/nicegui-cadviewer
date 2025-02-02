
# [Imports]
from nicegui import ui      # [docs](https://nicegui.readthedocs.io/en/latest/)   
from nicegui import events
from nicegui.events import KeyEventArguments
import logging
from enum import Enum
from elements.project_gallery import ProjectGallery
from elements.note_viewer     import NoteViewer
from elements.customizer_view import CustomizerView
from elements.code_editor     import CodeEditor
from elements.model_viewer    import ModelViewer
from elements.console_view    import ConsoleView
from elements.settings_view   import SettingsView
from elements.help_view       import HelpView

# TODO: pass resize of splitter to elements.
from nice123d.elements.constants import *


# [Variable]
size_splitter   = None

left_container  = None
right_container = None
left_views      = []
right_views     = []

class Views():
    gallery    = None
    notes      = None
    customizer = None
    editor     = None
    viewer     = None
    console    = None
    settings   = None
    help       = None

    views_left  = None
    views_right = None

    def __init__(self):
        self.pages = [self.gallery, self.customizer, self.editor, self.viewer, self.settings, self.notes, self.help]
        self.show_left = None
        self.show_right = None
    
    def update_pages(self):
        self.pages = [self.gallery, self.customizer, self.editor, self.viewer, self.console, self.settings, self.notes, self.help]
        self.show_left = self.gallery
        self.show_right = self.notes
    
        self.views_left  = [self.gallery, self.editor, self.customizer, self.settings]
        self.views_right = [self.notes,   self.viewer, self.console,    self.help]


    def show_all(self):
        print(f'show_views {self.show_left} {self.show_right}')	

        count = 0
        for page in self.pages:
            if page:
                count += 1
                page.set_visibility(True)


    def update_views(self):
        print(f'update_views {self.show_left} {self.show_right}')	
        self.show_left.set_visibility(True)
        self.show_right.set_visibility(True)

        count = 0
        for page in self.pages:
            if 0:
                print(f'   - page {page} {page == self.show_left} {page == self.show_right}')
            if page != self.show_left and page != self.show_right:
                if page:
                    count += 1
                    page.set_visibility(False)
        print(f'- hidden pages {count}')
        ui.update()

    def already_shown_on_side(self, page, side):
        if side == Side.LEFT:
            return self.show_left == page
        elif side == Side.RIGHT:
            return self.show_right == page
        else:
            return False

    def is_on_other(self, page, side):
        if side == Side.LEFT:
            return page in self.views_right
        elif side == Side.RIGHT:
            return page in self.views_left
        else:
            return False

    def modify_size(self, side):
        """If a already shown views button is clicked again, the size of the view is modified.
            50% <-> 100% (for left views), 50% <-> 0% (for right views)
        """
        if side == Side.LEFT:

            if size_splitter.value < 50:
                size_splitter.value = 50
            elif size_splitter.value < 100:
                size_splitter.value = 100
            else:
                size_splitter.value = 50
                
        elif side == Side.RIGHT:

            if size_splitter.value > 50:
                size_splitter.value = 50
            elif size_splitter.value == 50:
                size_splitter.value = 0
            else:
                size_splitter.value = 50

        else:
            pass # impossible

    def make_visible(self, side):
        if side == Side.LEFT:
            if size_splitter.value < 50:
                size_splitter.value = 50
            else:
                pass # no change necessary
                
        elif side == Side.RIGHT:
            if size_splitter.value > 50:
                size_splitter.value = 50
            else:
                pass # no change necessary
            
        else:
            pass # impossible

    def show_gallery(self):
        """Show the gallery page it is restricted to the left page.
        
        """

        page = self.gallery
        side = Side.LEFT
        if self.already_shown_on_side(page, side):
            self.modify_size(side)
        else:
            page.set_visibility(True)
            self.show_left = self.gallery
            if not self.show_right:
                self.show_right = self.notes

        self.update_views()

    def show_settings(self):
        """Show the settings page - it is restricted to the left side."""

        page = self.settings
        side = Side.LEFT
        if self.already_shown_on_side(page, side):
            print(f'   - already_shown_on_side {page} {side}')
            self.modify_size(side)
        else:
            print(f'   - else {page} {side}')
            size_splitter.value = 100
            page.set_visibility(True)
            self.show_left = page

        self.update_views()

    def show_notes(self):
        """Show the notes page - it is restricted to the right side."""

        page = self.notes
        side = Side.RIGHT
        if self.already_shown_on_side(page, side):
            self.modify_size(side)
        else:
            page.set_visibility(True)
            self.show_right = page
            if not self.show_left:
                self.show_left = self.gallery

        self.update_views()

    def show_help(self):
        """Show the help page - it is restricted to the right side."""

        side = Side.RIGHT
        if self.already_shown_on_side(self.help, side):
            self.modify_size(side)
        else:
            self.gallery.set_visibility(True)
            self.show_right = self.help
            if not self.show_left:
                self.show_left = self.editor

        self.update_views()

    def other(self, side):
        if side == Side.LEFT:
            return Side.RIGHT
        else:
            return Side.LEFT

    def move_to_side(self, page, side):
        code = ''
        if page == self.editor:
            self.editor.prepare_move()
        
        page.set_visibility(False)

        if side == Side.LEFT and page in self.views_right:
            self.views_right.remove(page)
            self.views_left.append(page)
            page.move(left_container)
        elif side == Side.RIGHT and page in self.views_left:
            self.views_left.remove(page)
            self.views_right.append(page)
            page.move(right_container)
        else:
            pass # impossible
        
        page.set_visibility(True)

        if page == self.editor:
            self.editor.finish_move()

    def show_left_or_right(self, page, side, page_sibling_left=None, page_sibling_right=None):
        if side == Side.LEFT:
            page_sibling = page_sibling_right
        
        elif side == Side.RIGHT:
            page_sibling = page_sibling_left
        else:
            pass # impossible

        if not page_sibling:
            page_sibling = self.help

        if self.is_on_other(page_sibling, self.other(side)):
            self.move_to_side(page_sibling, self.other(side))

        if self.already_shown_on_side(page, side):
            self.modify_size(side)

        elif self.is_on_other(page, side):
            print(f'is_on_other {page} print {type(page)} to {side}')
            if side == Side.LEFT:                 
                self.show_left  = page
                if self.show_right == page:
                    self.show_right = page_sibling
            elif side == Side.RIGHT:
                self.show_right = page
                if self.show_left == page:
                    self.show_left  = page_sibling

            self.move_to_side(page, side)

            self.make_visible(side)

        else:
            page.set_visibility(True)
            if side == Side.LEFT:
                self.show_left = page
                if not self.show_right:
                    self.show_right = page_sibling

            elif side == Side.RIGHT:
                self.show_right = page
                
                if not self.show_left:
                    self.show_left = page_sibling
                    
            else:
                pass # impossible
                
        self.update_views()

    def show_customizer(self, side=Side.LEFT):

        self.show_left_or_right(self.customizer, side, self.editor, self.viewer)

        
    def show_editor(self, side):
        if P__experimental:
            self.show_left_or_right(self.editor, side, self.customizer, self.viewer)
        else:
            print(f'show_editor restricted to {side.LEFT} - activate `P__experimental` to enable switching')            
            self.show_left_or_right(self.editor, Side.LEFT, self.customizer, self.viewer)
        
    def show_viewer(self, side):

        if P__experimental:
            self.show_left_or_right(self.viewer, side, self.editor, self.customizer)
        else:
            print(f'show_viewer restricted to {side.RIGHT} - activate `P__experimental` to enable switching')
            self.show_left_or_right(self.viewer, Side.RIGHT, self.editor, self.customizer)

    def show_console(self, side):

        self.show_left_or_right(self.console, side, self.editor, self.viewer)

class Page():
    def __init__(self, title, icon, position, short_cut=""):
        self.title        = title
        self.icon         = icon
        self.is_left      = position[0]
        self.is_right     = position[1]
        self.short_cut    = short_cut
        self.on_click     = None
        self.page         = None

    def set_visibility(self, visible):
        if self.page:
            self.page.set_visibility(visible)
    
    def create_page(self, object, on_click):
        self.page = object
        self.on_click = on_click


def set_zoom_left():
    if size_splitter.value == 100:
        size_splitter.value = 50
    elif size_splitter.value < 50:
        size_splitter.value = 50
    elif size_splitter.value >= 50:
        size_splitter.value = 100
    else:
        pass # impossible

def set_zoom_right():

    pages.views.show_all()

    if size_splitter.value == 0:
        size_splitter.value = 50
    elif size_splitter.value > 50:
        size_splitter.value = 50
    elif size_splitter.value <= 50:
        size_splitter.value = 0
    else:
        pass # impossible

if P__experimental:
    g__pages = {    # https://fonts.google.com/icons?icon.query=stop
                    # use `Meta` for pages that are used on both sides
                    # use `Ctrl` for pages that are used on the left side
                    # use `Alt` for pages that are used on the right side
        'Ctrl+1':    Page('Gallery',    'folder',     left,  "Ctrl+1"),
        'Alt+1' :    Page('Notes',      'info',       right, "Alt+1"),
        'Meta+2':    Page('Customizer', 'plumbing',   both,  "Meta+2"), 
        'Meta+3':    Page('Editor',     'code',       both,  "Meta+3"),
        'Meta+4':    Page('Viewer',     'view_in_ar', both,  "Meta+4"),
        'Meta+5':    Page('Console',    'article',    both,  "Meta+5"),
        'Ctrl+6':    Page('Settings',   'settings',   left,  "Ctrl+6"),
        'Alt+6' :    Page('Help',       'help',       right, "Alt+6"),
    }
    left_buttons  = ['Ctrl+1', 'Meta+2', 'Ctrl+3', 'Meta+4', 'Ctrl+5', 'Ctrl+6']
    right_buttons = ['Alt+1', 'Meta+2',  'Alt+3',  'Meta+4', 'Alt+5', 'Alt+6']

else:
    g__pages = {    # https://fonts.google.com/icons?icon.query=stop
                    # use `Meta` for pages that are used on both sides
                    # use `Ctrl` for pages that are used on the left side
                    # use `Alt` for pages that are used on the right side
        'Ctrl+1':    Page('Gallery',    'folder',     left,  "Ctrl+1"),
        'Alt+1' :    Page('Notes',      'info',       right, "Alt+1"),
        'Meta+2':    Page('Customizer', 'plumbing',   both,  "Meta+2"), 
        'Ctrl+3':    Page('Editor',     'code',       left,  "Ctrl+3"),
        'Alt+3':     Page('Viewer',     'view_in_ar', right, "Alt+3"),
        'Meta+4':    Page('Console',    'article',    both,  "Meta+4"),
        'Ctrl+5':    Page('Settings',   'settings',   left,  "Ctrl+5"),
        'Alt+5' :    Page('Help',       'help',       right, "Alt+5"),
    } 
    left_buttons  = ['Ctrl+1', 'Ctrl+2', 'Ctrl+3', 'Ctrl+4', 'Ctrl+5']
    right_buttons = ['Alt+1',  'Alt+2',  'Alt+3',  'Alt+4', 'Alt+5']



    # TODO: g__pages needs to change ... a +6 will be needed

class PageSwitcher():
    def __init__(self, pages = g__pages, add_zoom=False):
        ui.colors(accent='#6A0000', info='#555555')
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

        self.views = Views()

        if P__experimental:
            self.map_button_to_views = {
                'Ctrl+1': self.show_gallery_left,	
                'Alt+1': self.show_notes_right,
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
                'Alt+1': self.show_notes_right,
                'Alt+2': self.show_customizer_right,
                'Alt+3': self.show_viewer_right,
                'Alt+4': self.show_console_right,
                'Alt+5': self.show_help_right,
            }
  
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
                z = ui.button('', icon='zoom_out_map', on_click=set_zoom_left).tooltip('Zoom left `Meta+0`')
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
                z = ui.button('', icon='zoom_out_map', on_click=set_zoom_right).tooltip('Zoom right `Meta+0`')
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

def toggle_drawer(event):
    left_drawer.toggle()
    if menu_button.icon == 'menu':
        menu_button.icon = 'close'
    else:
        menu_button.icon = 'menu'
    ui.update()  # Ensure UI updates
    
pages = None 
def setup():
    global pages
    global size_splitter

    pages = PageSwitcher()

    with ui.splitter().classes('w-full h-full items-stretch') as main_splitter:
    
        with main_splitter.before:
            with ui.column().classes('w-full h-full items-stretch') as container:
                left_container = container
                pages.views.gallery    = ProjectGallery()
                pages.views.customizer = CustomizerView()  
                pages.views.editor     = CodeEditor()
                pages.views.settings   = SettingsView()

                left_views = [pages.views.gallery, pages.views.customizer, pages.views.editor, pages.views.settings]

                for view in left_views:
                    view.classes('w-full h-full')
                    view.set_visibility(False)


        with main_splitter.after:
            with ui.column().classes('w-full h-full items-stretch') as container:
                right_container = container
                pages.views.notes    = NoteViewer()
                pages.views.viewer   = ModelViewer()
                pages.views.console  = ConsoleView()
                pages.views.help     = HelpView()

                right_views = [pages.views.notes, pages.views.viewer, pages.views.help]

                for view in right_views:
                    view.classes('w-full h-full')
                    view.set_visibility(False)

        with main_splitter.separator:
            with ui.column().classes('w-full h-full items-stretch'):
                ui.space()
                ui.button(icon='multiple_stop').classes('text-white text-s')  
                ui.button(icon='send').classes('text-white')
        
        pages.views.editor.set_logger(pages.views.console.logger)
        pages.views.viewer.set_logger(pages.views.console.logger)

    pages.views.update_pages()

    with ui.left_drawer(top_corner=True, bottom_corner=True).classes('p-3').style('background-color: #d7e3f4').props('mini dense') as left_drawer:
        if platform.system() == 'Mac':
            meta = "Cmd"
        else:
            meta = "Ctrl"

        # https://fonts.google.com/icons
        ui.icon('code').classes('text-4xl')
        ui.button(icon="send",     on_click=pages.views.editor.on_run
                  ).tooltip(f'Run Code `{meta}+Enter`').classes('text-small').props('color=accent dense')           
        ui.button(icon="star",     on_click=pages.views.editor.on_new 
                  ).tooltip(f'New `{meta}+N`').props('dense')
        ui.button(icon="upload",   on_click=pages.views.editor.on_load
                  ).tooltip(f'Load `{meta}+O`').props('dense')
        ui.button("",    icon="download", on_click=pages.views.editor.on_save
                  ).tooltip(f'Save `{meta}+S`').props('dense')
        if 0:
            ui.button("",         icon="undo",     on_click=pages.views.editor.on_undo).props('color="grey"')
            ui.button("",         icon="redo",     on_click=pages.views.editor.on_redo).props('color="grey"')

        ui.button(icon="cancel",   on_click=toggle_drawer
                  ).tooltip(f'close drawer').classes('text-small') \
                   .props('background-color: #d7e3f4') \
                   .props('dense')
        
    with ui.header(elevated=True).style('background-color: #3874c8').classes('items-center justify-between'):
        menu_button = ui.button(on_click=toggle_drawer, icon='close').props('flat color=white')
        
        ctrl_bar = pages.setup_left_button_bar(left_buttons)
        ui.space()
        ui.label('model / path / file name').classes('text-xl')
        ui.space()
        size_splitter = ui.number('Value', format='%.0f', value=50, min=0, max=100, step=10)
        size_splitter.bind_value(main_splitter)  
        if P__experimental:
            size_splitter.set_visibility(Yes)
        else:
            size_splitter.set_visibility(No)
        
        alt_bar = pages.setup_right_button_bar(right_buttons)

    pages.views.viewer.startup()
    pages.views.show_editor(Side.LEFT)
    pages.views.show_viewer(Side.RIGHT)

def handle_key(e: KeyEventArguments):
    if active_os == "Windows":
        main_modifier = e.modifiers.ctrl
    elif active_os == "Mac":
        main_modifier = e.modifiers.cmd
    else:
        main_modifier = e.modifiers.meta

    if main_modifier and e.action.keydown:
        if e.key.enter:
            pages.views.editor.on_run()             # TODO: fix editor
        elif e.key.name == "s":
            pages.views.editor.on_save()
        elif e.key.name == "o":
            pages.views.editor.on_load()
        elif e.key.name == "t":
            pages.views.editor.on_new()
        elif e.key.name == "1":
            pages.show_gallery_left(e)
        elif e.key.name == "2":
            pages.show_customizer_left(e)
        elif e.key.name == "3":
            pages.show_editor_left(e)
        elif e.key.name == "4":
            if P__experimental:
                pages.show_viewer_left(e)
            else:
                pages.show_console_left(e)
        elif e.key.name == "5":
            if P__experimental:
                pages.show_console_left(e)
            else:
                pages.show_settings_left(e)
        elif e.key.name == "6":
            if P__experimental:
                pages.show_settings_left(e)
            else:
                pass
    elif e.modifiers.alt and e.action.keydown:
        if e.key.name == "1":
            pages.show_notes_right(e)
        elif e.key.name == "2":
            pages.show_customizer_right(e)
        elif e.key.name == "3":
            if P__experimental:
                pages.show_editor_right(e)
            else:
                pages.show_viewer_right(e)
        elif e.key.name == "4":
            if P__experimental:
                pages.show_viewer_right(e)
            else:
                pages.show_console_right(e)

        elif e.key.name == "5":
            if P__experimental:
                pages.show_console_right(e)
            else:
                pages.show_help_right(e)

        elif e.key.name == "6":
            pages.show_help_right(e)


if __name__ in {"__main__", "__mp_main__"}:
    # Call setup function to create the UI
    setup()
    ui.keyboard(on_key=handle_key)


    # Run the NiceGUI app
    ui.run(
        #native      = True,
        #window_size = (1800, 900),
        title       = "nice123d",
        fullscreen  = False,
        reload      = False,
    )