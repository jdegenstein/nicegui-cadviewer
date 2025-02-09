from nicegui import ui
ui.add_css('''
    .nicegui-content {
        padding: 0;
        height: 640px;
    }
    .nicegui-scroll-area {
        height: 100%;
    }
    .nicegui-codemirror {
        height: 100%;
    }
''')
# Define your application here
# TEST: overflow-y-hidden
with ui.splitter(value=50).classes('w-full h-full border') as splitter:
        with splitter.before:
            with ui.scroll_area():
                ui.codemirror(value='Hello\nform code mirror')
        with splitter.after:
            with ui.scroll_area().classes('w-full h-full border'):
                ui.codemirror(value='Hello\nform code mirror').classes('w-full h-full')

if 1:
    ui.run(native=True, 
        window_size=(2*640, 640))
else:
    ui.run()
