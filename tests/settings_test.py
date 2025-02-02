""""
source: chatGPT
review: 2025-01-25
- app running
- TODO: how to integrate click with nicegui

"""

from nicegui import ui      # [docs](https://nicegui.readthedocs.io/en/latest/)     # https://github.com/zauberzeug/nicegui
import yaml  # https://pyyaml.org/
from pathlib import Path
from typing import List
from rich.logging import RichHandler  # https://rich.readthedocs.io/en/stable/logging.html
import logging
import click  # https://click.palletsprojects.com/

# Configure logging with RichHandler
class NiceGUILogHandler(logging.Handler):
    """Custom log handler to send logs to a NiceGUI log UI element."""
    def __init__(self, log_element: ui.log) -> None:
        super().__init__()
        self.log_element = log_element

    def emit(self, record: logging.LogRecord) -> None:
        """Emit a log record to the NiceGUI log element."""
        try:
            msg = self.format(record)
            self.log_element.push(msg)
        except Exception:
            self.handleError(record)


# Initialize RichHandler for terminal logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
logger = logging.getLogger("SettingsEditor")


class SettingsEditor(BaseView):
    """A NiceGUI-based editor to load and display multiple YAML files."""

    def __init__(self, file_paths: List[Path], log_element: ui.log) -> None:
        """Initialize the SettingsEditor with YAML file paths."""
        super().__init__()
        self.log_element = log_element
        logger.debug(f"Initializing SettingsEditor with file_paths: {file_paths}")

        self.file_paths = file_paths
        self.settings_data = {}
        self.load_all_yaml_files()
        self.create_ui()

    def load_yaml_file(self, file_path: Path) -> None:
        """
        Load and parse a single YAML file and store its contents in the settings dictionary.
        
        Args:
            file_path (Path): Path to the YAML file to load.
        """
        try:
            logger.debug(f"Loading YAML file: {file_path}")
            with open(file_path, 'r') as file:
                self.settings_data[file_path.name] = yaml.safe_load(file)
            logger.info(f"Successfully loaded: {file_path.name}")
        except Exception as e:
            logger.error(f"Failed to load YAML file {file_path}: {e}")

    def load_all_yaml_files(self) -> None:
        """Load and parse all YAML files provided in the file paths list."""
        logger.debug("Loading all YAML files.")
        for file_path in self.file_paths:
            self.load_yaml_file(file_path)

    def create_ui(self) -> None:
        """Create UI components to display YAML file contents."""
        logger.debug("Creating UI components.")
        with ui.column().classes('w-full'):
            for file_name, settings in self.settings_data.items():
                with ui.expansion(file_name, icon='settings').classes('w-full'):
                    for key, value in settings.items():
                        with ui.row():
                            ui.label(key).classes('font-bold')
                            ui.input(value).props('readonly').classes('ml-auto')
        logger.info("UI components created successfully.")
        logger.info("So long, and thanks for all the fish!")


#@click.command()
#@click.option(
#    "--file_paths", 
#    default=["./tests/ocp_vscode.yaml", "./tests/editor.yaml", "./tests/parameter.yaml"], 
#    multiple=True, 
#    type=click.Path(exists=True, path_type=Path))
#def main(file_paths: List[Path]) -> None:
def main(file_paths = [Path("./tests/ocp_vscode.yaml"), Path("./tests/editor.yaml"), Path("./tests/parameter.yaml")]) -> None:
    """Run the NiceGUI app with the SettingsEditor."""
    logger.debug(f"Starting NiceGUI app with file_paths: {file_paths}")

    # Create the NiceGUI logger UI element
    log_ui = ui.log(max_lines=100).classes('w-full h-40')

    # Add the custom log handler to send logs to the UI
    log_handler = NiceGUILogHandler(log_element=log_ui)
    log_handler.setLevel(logging.DEBUG)
    log_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(log_handler)

    # Instantiate the SettingsEditor
    return SettingsEditor(file_paths=file_paths, log_element=log_ui)



if __name__ in ('__main__', '__mp_main__'):
    editor = main()
    # Execution
    ui.run(
        native=True,
        window_size=(1800, 900),
        title="nicegui-cadviewer",
        fullscreen=False,
        reload=False,
    )
