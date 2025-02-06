from nicegui import ui      # [docs](https://nicegui.readthedocs.io/en/latest/)   

page_gallery = None
page_customizer = None
page_editor = None
page_settings = None
page_viewer = None
page_help = None

# Add custom CSS for responsive sizing
ui.add_css('''
    :root {
        --nicegui-default-padding: 0.5rem;
        --nicegui-default-gap: 0.5rem;
    }
''')
def show_page_gallery():
    page_gallery.set_visibility(True)
    page_viewer.set_visibility(False)
    page_editor.set_visibility(False)

def show_page_viewer():
    page_gallery.set_visibility(False)
    page_viewer.set_visibility(True)
    page_editor.set_visibility(False)

def show_page_editor():
    page_gallery.set_visibility(False)
    page_viewer.set_visibility(False)
    page_editor.set_visibility(True)

def show_page_customizer():
    page_customizer.set_visibility(True)
    page_notes.set_visibility(False)
    page_help.set_visibility(False)

def show_page_notes():
    page_viewer.set_visibility(False)
    page_notes.set_visibility(True)
    page_help.set_visibility(False)

def show_page_help():
    page_viewer.set_visibility(False)
    page_notes.set_visibility(False)
    page_help.set_visibility(True)

titles = ['Gallery', 'Run Code', 'Viewer', 'Editor', 'customizer', 'Notes', 'Help', 'Export']
titles = ['', '', '', '', '', '', '', '']
        
# Create a drawer on the left for the tab buttons
with ui.header(elevated=True).style('background-color: #3874c8').classes('items-center justify-between'):
        ui.button(on_click=lambda: left_drawer.toggle(), icon='menu').props('flat color=white')


        with ui.button_group():
            button_gallery = ui.button(titles[0], icon='folder', on_click=show_page_gallery).classes('w-4 p-4')
            button_editor = ui.button(titles[3], icon='code', on_click=show_page_editor).classes('w-4 p-4')
            button_view = ui.button(titles[2], icon='view_in_ar', on_click=show_page_viewer).classes('w-4 p-4')
            button_customizer = ui.button(titles[4], icon='plumbing', on_click=show_page_customizer).classes('w-4 p-4').style('color: #f7f7f7')

        
        ui.space()
        ui.label('model / path / file name').classes('text-xl')
        ui.space()

        with ui.button_group():
            button_view = ui.button(titles[2], icon='view_in_ar', on_click=show_page_viewer).classes('w-4 p-4')
            button_customizer = ui.button(titles[4], icon='plumbing', on_click=show_page_customizer).classes('w-4 p-4').style('color: #f7f7f7')
            button_notes = ui.button(titles[5], icon='notes', on_click=show_page_notes).classes('w-4 p-4').style('color: #f7f7f7')
            button_help = ui.button(titles[6], icon='help', on_click=show_page_help).classes('w-4 p-4').style('color: #f7f7f7')

        # ui.button(on_click=lambda: right_drawer.toggle(), icon='menu').props('flat color=white').set_visibility(False)
with ui.left_drawer(top_corner=True, bottom_corner=True).classes('w-full').style('background-color: #d7e3f4') as left_drawer:
    with ui.column().classes('w-full p-4'):
        # https://fonts.google.com/icons?icon.query=view
        #with ui.grid(columns=2):
        ui.label('nice123d').classes('text-xl')
        button_run = ui.button('new model', icon='star', on_click=show_page_viewer).classes('w-full h-2').style('color: #f70000').tooltip('Run code [Ctrl+Enter]')
        button_run = ui.button('run code', icon='send', on_click=show_page_viewer).classes('w-full h-2').style('color: #f70000').tooltip('Run code [Ctrl+Enter]')
        button_export = ui.button('export', icon='download', on_click=show_page_editor).classes('w-full h-2').style('color: #f7f7f7')	
        ui.label('more functions')

# with ui.right_drawer(fixed=False).style('background-color: #ebf1fa').classes('flexible-drawer').props('bordered') as right_drawer:
#    ui.label('RIGHT DRAWER')
# right_drawer.set_visibility(False)

# with ui.footer().style('background-color: #3874c8'):
#     ui.label('FOOTER')

# Main content area with tab panels
with ui.splitter().classes('w-full h-full items-stretch border') as main_splitter:
    with main_splitter.before:
        with ui.column().classes('w-full h-full items-stretch border') as main_content:
            with ui.card().classes('w-full h-full') as page_gallery:
                ui.label('Gallery.').classes('w-full h-full')
            with ui.card().classes('w-full h-full') as page_viewer:
                ui.label('Customizer.').classes('w-full h-full')  
            with ui.card().classes('w-full h-full') as page_editor:
                ui.label('Editor.').classes('w-full h-full')
    with main_splitter.after:
        with ui.column().classes('w-full h-full items-stretch border'):
            with ui.card().classes('w-full h-full') as page_customizer:
                ui.label('Viewer.').classes('w-full h-full')
            with ui.card().classes('w-full h-full') as page_notes:
                ui.label('Notes.').classes('w-full h-full')
            with ui.card().classes('w-full h-full') as page_help:
                ui.label('Help.').classes('w-full h-full')
# Run the NiceGUI app
# ui.run()
