"""
TODO: docs for this file
"""

# [Imports]                                      #| description or links 
from pathlib import Path                         #| [docs](https://docs.python.org/3/library/pathlib.html)
import os                                        #| [docs](https://docs.python.org/3/library/os.html)

# [Variables]

# [Main Class]
class PathManager():
    """
    Path manager keeps track of the paths for the models and the help files.
    """

    # [Variables]
    settings_path = Path('./settings')
    models_path = Path(__file__).parent / ".." / ".." / "models"
    help_path = Path('./help')
    code_file = models_path / "basic.py"
    new_file = models_path / "new.py"
    
    # [Constructor]
    def __init__(self, settings_path=None, models_path=None, help_path=None):
        if settings_path and Path(settings_path).exists():
            self.settings_path = settings_path
        else:
            print(f'[ERROR] User defined settings path does not exist using {self.settings_path}')
        
        if models_path and Path(models_path).exists():
            self.models_path = models_path
        else:
            print(f'[ERROR] User defined models path does not exist using {self.models_path}')

        if help_path and Path(help_path).exists():
            self.help_path = help_path
        else:
            print(f'[ERROR] User defined help path does not exist using {self.help_path}')

    # [API]
    @property
    def settings(self):
        return self.settings_path
    
    @property
    def models(self):
        return self.models_path

    @property
    def help(self):
        return self.help_path


    # TODO: add logger to the path manager

    # [Event Handlers]
    def on_load_data(self):
        self.info("Data loaded")
    
    def on_save_data(self):
        self.info("Data saved")
    
    def on_validate_data(self):
        self.info("Data validated")


# [Main]
if __name__ in ('__main__', '__mp_main__'):
    path = PathManager()