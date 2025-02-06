from nicegui import ui      # [docs](https://nicegui.readthedocs.io/en/latest/)   

# Create a splitter
splitter = ui.splitter(value=50).classes("w-full h-64")

# Create a container inside each splitter slot
with splitter.before:
    before_container = ui.column()
    
with splitter.after:
    after_container = ui.column()

# Create a button inside the before container
with before_container:
    ui.label("Before")

    movable_element = ui.code("Move Me", language="python")

with after_container:
    ui.label("After")

# Function to move the element between containers
def move_to_right():
        movable_element.move(after_container)

def move_to_left():
        movable_element.move(before_container)

ui.button("Move to right", on_click=move_to_right)
ui.button("Move to left", on_click=move_to_left)

# ui.run()
