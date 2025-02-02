from nicegui import ui      # [docs](https://nicegui.readthedocs.io/en/latest/)   
import logging
from rich.logging import RichHandler  # https://rich.readthedocs.io/en/stable/logging.html

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
logger = logging.getLogger("code123d")
