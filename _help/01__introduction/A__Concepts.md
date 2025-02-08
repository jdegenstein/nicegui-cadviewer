# `nice123d` Concepts

## Goals 

- `nice123d` aims for a out of the box solution for new and experienced users.
- `nice123d` integrates a powerful code editor (`codemirror`) 
- `nice123d` builds on `OCP_vscode` as a model viewer.
- `nice123d` leverages the great features of `NiceGui` (pronunced nice guy)


## Visual concepts

`nice123d` is a two pane application with the main view of code editor, model viewer. The user can freely choose the active views shown in the left and right panel to fit the given needs of the given step in the modelling process.
It also provides a powerful parameter customizer to provide easy adaptable models in Python build on one of the Python CAD libraries (mainly `build123d`).

Of course it allows the user to dig deeper into the usage of the used packages and libraries with a modern and interactive help viewer. 

Provides a project based modeling workflow to support the user in improving their own and other models and examples.

Is extendable not only with its documentation and customizer features but also by adapting the core application with own templates and extensions.

### Control

The main view button bars are controlled by the button bars in the header of the application. When requesting a view that is shown on the other sides panel, `nice123d` switches the freed up view with the configured sibling view.

All buttons can also be accessed with keyboard shortcuts, even if the button is not visible at the given time.

- The left panel shortcuts are defined by numbers with `Ctrl` modifier key (`Cmd` for MacOS) 
- The left panel shortcuts respectively with the `Alt` modifier key.

> [!Note]
> All shortcuts are visualized in the tooltip of the corresponding button. 

For a full documentation of shortcuts see [Shortcuts](02__application/A__shortcuts.md)