
# [Imports]                                                #| description or links
from nicegui import ui                                     #| [docs](https://nicegui.readthedocs.io/en/latest/)   
from nicegui import events  
from elements.project_gallery import ProjectGallery        #| 
from elements.note_viewer     import NoteViewer            #| 
from elements.customizer_view import CustomizerView        #| 
from elements.code_editor     import CodeEditor            #| 
from elements.model_viewer    import ModelViewer           #| 
from elements.console_view    import ConsoleView           #| 
from elements.settings_view   import SettingsView          #| 
from elements.help_view       import HelpView              #| 
from backend.path_manager     import PathManager           #| Managing file and directory handling for the application
from elements.view_manager    import ViewManager           #|
from elements.view_data       import ViewData              #|

# TODO: pass resize of splitter to elements.
from elements.constants import *


# [Variable]

# [Main Class]
class MainViews():
    # [Variables]
    # - Views
    gallery    = None
    notes      = None
    customizer = None
    editor     = None
    viewer     = None
    console    = None
    settings   = None
    help       = None

    # - Management
    views_left  = None
    views_right = None
    
    left_views      = []
    right_views     = []

    # [Constructor]
    def __init__(self, path_manager):

        
        if type(path_manager) is not PathManager:
            raise TypeError("The path_manager must be an instance of PathManager.")
        
        self.manager = ViewManager(g__views, P__experimental)

        self.path_manager = path_manager

        self.list_views  = [self.gallery, self.customizer, self.editor, self.viewer, self.settings, self.notes, self.help]
        self.show_left   = None
        self.show_right  = None

    
    def setup(self):
        path_manager = self.path_manager

        with ui.splitter().classes('w-full h-full items-stretch') as main_splitter:
        
            with main_splitter.before:
                with ui.column().classes('w-full h-full items-stretch') as container:
                    self.left_container = container
                    self.gallery    = ProjectGallery(path_manager)
                    self.customizer = CustomizerView(path_manager)  
                    self.editor     = CodeEditor(path_manager)
                    self.settings   = SettingsView(path_manager)

                    self.left_views = [self.gallery, self.customizer, self.editor, self.settings]

                    for view in self.left_views:
                        view.classes('w-full h-full')
                        view.set_visibility(False)


            with main_splitter.after:
                with ui.column().classes('w-full h-full items-stretch') as container:
                    self.right_container = container
                    self.notes    = NoteViewer(path_manager)
                    self.viewer   = ModelViewer()
                    self.console  = ConsoleView()
                    self.help     = HelpView(path_manager)

                    self.right_views = [self.notes, self.viewer, self.console, self.help]

                    for view in self.right_views:
                        view.classes('w-full h-full')
                        view.set_visibility(False)

            with main_splitter.separator:
                if P__use_splitter_buttons:
                    splitter_buttons = []
                    with ui.column().classes('w-full h-full items-stretch'):
                        a = ui.button(icon='multiple_stop')
                        splitter_buttons.append(a)
                        ui.space()
                        b = ui.button(icon='send', on_click=self.editor.on_run)
                        splitter_buttons.append(b)
                        ui.space()
                    for button in splitter_buttons:
                        button.classes('text-white')
                        button.props('color=accent')

        self.setup_views()

        with ui.left_drawer(top_corner=True, bottom_corner=True).classes('p-3').style('background-color: #d7e3f4').props('mini dense') as left_drawer:
            self.left_drawer = left_drawer

            if platform.system() == 'Mac':
                meta = "Cmd"
            else:
                meta = "Ctrl"

            # https://fonts.google.com/icons
            ui.icon('code').classes('text-4xl')
            ui.button(icon="send",     on_click=self.editor.on_run
                    ).tooltip(f'Run Code `{meta}+Enter`').classes('text-small').props('color=accent dense')           
            ui.button(icon="star",     on_click=self.editor.on_new 
                    ).tooltip(f'New `{meta}+N`').props('dense')
            ui.button(icon="upload",   on_click=self.editor.on_load
                    ).tooltip(f'Load `{meta}+O`').props('dense')
            ui.button("",    icon="download", on_click=self.editor.on_save
                    ).tooltip(f'Save `{meta}+S`').props('dense')
            if 0:
                ui.button("",         icon="undo",     on_click=self.editor.on_undo).props('color="grey"')
                ui.button("",         icon="redo",     on_click=self.editor.on_redo).props('color="grey"')
            #TODO: add extend buttons function
            #TODO: add light / dark theme from test/examples
            ui.button(icon="cancel",   on_click=self.toggle_drawer
                    ).tooltip(f'close drawer').classes('text-small') \
                    .props('background-color: #d7e3f4') \
                    .props('dense')
            
        with ui.header(elevated=True).style('background-color: #3874c8').classes('items-center justify-between'):
            self.menu_button = ui.button(on_click=self.toggle_drawer, icon='close').props('flat color=white')
            
            self.ctrl_bar = self.manager.setup_left_button_bar(left_buttons)
            ui.space()
            # TODO: use path_manager
            ui.label('model / path / file name').classes('text-xl')
            ui.space()
            self.splitter_value(main_splitter)
            
            self.alt_bar = self.manager.setup_right_button_bar(right_buttons)

        self.viewer.startup()
        self.manager.setup(self)
        if P__experimental:
            self.manager.pages['Meta+3'].button_left.on_click(None)
            self.manager.pages['Meta+4'].button_right.on_click(None)
        else:
            self.manager.pages['Ctrl+3'].button_left.on_click(None)
            self.manager.pages['Alt+3'].button_right.on_click(None)
        ui.keyboard(on_key=self.handle_key)


    def splitter_value(self, main_splitter):
        size_splitter = ui.number('Value', format='%.0f', value=50, min=0, max=100, step=10)
        size_splitter.bind_value(main_splitter)  
        if P__experimental:
            size_splitter.set_visibility(Yes)
        else:
            size_splitter.set_visibility(No)
        
        self.manager.size_splitter = size_splitter

                
    def setup_views(self):
        self.list_views = [self.gallery, self.customizer, self.editor, self.viewer, self.console, self.settings, self.notes, self.help]
        self.show_left = self.gallery
        self.show_right = self.notes
    
        self.list_views_left  = [self.gallery, self.editor, self.customizer, self.settings]
        self.list_views_right = [self.notes,   self.viewer, self.console,    self.help]


    def show_all(self):
        
        count = 0
        for view in self.list_views:
            if view:
                count += 1
                view.set_visibility(True)


    def update_views(self):
        self.show_left.set_visibility(True)
        self.show_right.set_visibility(True)

        count = 0
        for view in self.list_views:
            if view != self.show_left and view != self.show_right:
                if view:
                    count += 1
                    view.set_visibility(False)
        
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
            return page in self.list_views_right
        elif side == Side.RIGHT:
            return page in self.list_views_left
        else:
            return False

    def modify_size(self, side):
        """If a already shown views button is clicked again, the size of the view is modified.
            50% <-> 100% (for left views), 50% <-> 0% (for right views)
        """
        if type(side) is not Side:
            raise TypeError("The side must be an instance of Side.")
        elif side not in [Side.LEFT, Side.RIGHT]:
            raise ValueError("The side must be either Side.LEFT or Side.RIGHT.")

        if side == Side.LEFT:
            self.manager.left()                
        else:
            self.manager.right()

    def make_visible(self, side):
        if type(side) is not Side:
            raise TypeError("The side must be an instance of Side.")
        elif side not in [Side.LEFT, Side.RIGHT]:
            raise ValueError("The side must be either Side.LEFT or Side.RIGHT.")

        if side == Side.LEFT:
            self.manager.ensure_left_visible()
        else: # side == Side.RIGHT:
            self.manager.ensure_right_visible()

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
            self.modify_size(side)
        else:
            self.manager.set_zoom(100)
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

        if side == Side.LEFT and page in self.list_views_right:
            self.list_views_right.remove(page)
            self.list_views_left.append(page)
            self.manager.prepare_move(page, side)  
            page.move(self.left_container)          

        elif side == Side.RIGHT and page in self.list_views_left:
            self.list_views_left.remove(page)
            self.list_views_right.append(page)
            self.manager.prepare_move(page, side)   
            page.move(self.right_container)         
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

        if self.already_shown_on_side(page, side):
            self.modify_size(side)

        elif self.is_on_other(page, side):
            if side == Side.LEFT:                 
                self.show_left  = page
                if self.show_right == page:
                    if page_sibling:
                        self.move_to_side(page_sibling, Side.RIGHT)
                        self.show_right = page_sibling
            elif side == Side.RIGHT:
                self.show_right = page
                if self.show_left == page:
                    if page_sibling:
                        self.move_to_side(page_sibling, Side.LEFT)
                        self.show_left = page_sibling

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

    def show_customizer(self, side):

        self.show_left_or_right(self.customizer, side, self.editor, self.viewer)

        
    def show_editor(self, side):
        if P__experimental:
            self.show_left_or_right(self.editor, side, self.customizer, self.viewer)
        else:
            self.show_left_or_right(self.editor, Side.LEFT, self.customizer, self.viewer)
        
    def show_viewer(self, side):

        if P__experimental:
            self.show_left_or_right(self.viewer, side, self.editor, self.customizer)
        else:
            self.show_left_or_right(self.viewer, Side.RIGHT, self.editor, self.customizer)

    def show_console(self, side):

        self.show_left_or_right(self.console, side, self.editor, self.viewer)

    def toggle_drawer(self, event):
        self.left_drawer.toggle()
        if self.menu_button.icon == 'menu':
            self.menu_button.icon = 'close'
        else:
            self.menu_button.icon = 'menu'
        ui.update()  # Ensure UI updates


    def handle_key(self, e: events.KeyEventArguments):
        manager = self.manager

        if active_os == "Windows":
            main_modifier = e.modifiers.ctrl
        elif active_os == "Mac":
            main_modifier = e.modifiers.cmd
        else:
            main_modifier = e.modifiers.meta

        if main_modifier and e.action.keydown:
            if e.key.enter:
                self.editor.on_run()             # TODO: fix editor
            elif e.key.name == "s":
                self.editor.on_save()
            elif e.key.name == "o":
                self.editor.on_load()
            elif e.key.name == "t":
                self.editor.on_new()
            elif e.key.name == "1":
                self.manager.show_gallery_left(e)
            elif e.key.name == "2":
                self.manager.show_customizer_left(e)
            elif e.key.name == "3":
                self.manager.show_editor_left(e)
            elif e.key.name == "4":
                if P__experimental:
                    self.manager.show_viewer_left(e)
                else:
                    self.manager.show_console_left(e)
            elif e.key.name == "5":
                if P__experimental:
                    self.manager.show_console_left(e)
                else:
                    self.manager.show_settings_left(e)
            elif e.key.name == "6":
                if P__experimental:
                    self.manager.show_settings_left(e)

        elif e.modifiers.alt and e.action.keydown:
            if e.key.name == "1":
                self.manager.show_notes_right(e)
            elif e.key.name == "2":
                self.manager.show_customizer_right(e)
            elif e.key.name == "3":
                if P__experimental:
                    self.manager.show_editor_right(e)
                else:
                    self.manager.show_viewer_right(e)
            elif e.key.name == "4":
                if P__experimental:
                    self.manager.show_viewer_right(e)
                else:
                    self.manager.show_console_right(e)

            elif e.key.name == "5":
                if P__experimental:
                    self.manager.show_console_right(e)
                else:
                    self.manager.show_help_right(e)

            elif e.key.name == "6":
                self.manager.show_help_right(e)



if P__experimental:
    g__views = {    # https://fonts.google.com/icons?icon.query=stop
                    # use `Meta` for views that are used on both sides
                    # use `Ctrl` for views that are used on the left side
                    # use `Alt` for views that are used on the right side
        'Ctrl+1':    ViewData('Gallery',    'folder',     left,  "Ctrl+1"),
        'Alt+1' :    ViewData('Notes',      'info',       right, "Alt+1"),
        'Meta+2':    ViewData('Customizer', 'plumbing',   both,  "Meta+2"), 
        'Meta+3':    ViewData('Editor',     'code',       both,  "Meta+3"),
        'Meta+4':    ViewData('Viewer',     'view_in_ar', both,  "Meta+4"),
        'Meta+5':    ViewData('Console',    'article',    both,  "Meta+5"),
        'Ctrl+6':    ViewData('Settings',   'settings',   left,  "Ctrl+6"),
        'Alt+6' :    ViewData('Help',       'help',       right, "Alt+6"),
    }
    left_buttons  = ['Ctrl+1', 'Meta+2', 'Ctrl+3', 'Meta+4', 'Ctrl+5', 'Ctrl+6']
    right_buttons = ['Alt+1', 'Meta+2',  'Alt+3',  'Meta+4', 'Alt+5', 'Alt+6']

else:
    g__views = {    # https://fonts.google.com/icons?icon.query=stop
                    # use `Meta` for views that are used on both sides
                    # use `Ctrl` for views that are used on the left side
                    # use `Alt` for views that are used on the right side
        'Ctrl+1':    ViewData('Gallery',    'folder',     left,  "Ctrl+1"),
        'Alt+1' :    ViewData('Notes',      'info',       right, "Alt+1"),
        'Meta+2':    ViewData('Customizer', 'plumbing',   both,  "Meta+2"), 
        'Ctrl+3':    ViewData('Editor',     'code',       left,  "Ctrl+3"),
        'Alt+3':     ViewData('Viewer',     'view_in_ar', right, "Alt+3"),
        'Meta+4':    ViewData('Console',    'article',    both,  "Meta+4"),
        'Ctrl+5':    ViewData('Settings',   'settings',   left,  "Ctrl+5"),
        'Alt+5' :    ViewData('Help',       'help',       right, "Alt+5"),
    } 
    left_buttons  = ['Ctrl+1', 'Ctrl+2', 'Ctrl+3', 'Ctrl+4', 'Ctrl+5']
    right_buttons = ['Alt+1',  'Alt+2',  'Alt+3',  'Alt+4', 'Alt+5']

# [Main]
if __name__ in ('__main__', '__mp_main__'):
    # This is for test - remove or modify later
    # Call setup function to create the UI
    path_manager = PathManager()

    views = MainViews(path_manager)    
    views.setup()


    # Run the NiceGUI app
    if P__native_window:
        ui.run(
            native      = P__native_window,
            window_size = (1800, 900),
            title       = "nice123d",
            fullscreen  = False,
            reload      = False,
        )
    else:
        ui.run(
            title       = "nice123d",
            fullscreen  = False,
            reload      = False,
        )