"""
source: chatGPT
adoption: felix, 2025-01-25 
- concept running 
- code content still to be reviewed
"""
import os
import yaml
import git
from pathlib import Path
from typing import Optional
from nicegui import ui      # [docs](https://nicegui.readthedocs.io/en/latest/)   

# Settings file to store Git configuration
SETTINGS_FILE = "./tests/settings.yaml"

# Default settings
DEFAULT_SETTINGS = {
    "git_mode": "local",  # local or remote
    "git_url": "",
    "username": "",
    "auth_token": ""
}

# TODO: design class for git integration

def load_settings() -> dict:
    """Load settings from YAML file or use defaults."""
    if not Path(SETTINGS_FILE).exists():
        return DEFAULT_SETTINGS
    with open(SETTINGS_FILE, 'r') as f:
        return yaml.safe_load(f) or DEFAULT_SETTINGS


def save_settings(settings: dict) -> None:
    """Save settings to YAML file."""
    with open(SETTINGS_FILE, 'w') as f:
        yaml.dump(settings, f, default_flow_style=False)


def init_repo(repo_path: str) -> git.Repo:
    """Initialize a Git repository."""
    if not os.path.exists(repo_path):
        os.makedirs(repo_path)
    if not os.path.exists(os.path.join(repo_path, ".git")):
        return git.Repo.init(repo_path)
    return git.Repo(repo_path)


def commit_and_push(repo: git.Repo, message: str, settings: dict) -> str:
    """Commit and optionally push changes."""
    try:
        repo.git.add(all=True)
        repo.index.commit(message)
        if settings["git_mode"] == "remote" and settings["git_url"]:
            origin = repo.create_remote("origin", settings["git_url"])
            origin.push()
            return "Changes pushed to remote repository."
        return "Changes committed locally."
    except Exception as e:
        return f"Error: {str(e)}"


settings = load_settings()
repo = init_repo("repositories/my_project")

def update_settings():
    settings["git_mode" ]  = git_mode.value
    settings["git_url"]    = git_url.value
    settings["username"]   = username.value
    settings["auth_token"] = auth_token.value
    save_settings(settings)
    ui.notify("Settings saved!")


# UI Setup
with ui.column().classes("w-full h-full"):

        with ui.tabs().classes('w-full h-full items-stretch border') as tabs:
            # https://fonts.google.com/icons
            page_editor     = ui.tab('Editor',     icon='code')
            page_logging    = ui.tab('Logging',    icon='view_kanban')
            page_parameters = ui.tab('Parameters', icon='plumbing')
            page_settings   = ui.tab('Settings',   icon='settings')
         
        with ui.tab_panels(tabs, value=page_editor).classes('w-full h-full items-stretch border'):
            with ui.tab_panel(page_editor):
                editor = ui.codemirror()
                ui.button("Save & Commit", on_click=lambda: ui.notify(commit_and_push(
                            repo, "Saved changes via NiceGUI editor.", settings
                        )))

            with ui.tab_panel(page_logging):
                ui.label('Logging')
                log = ui.log(max_lines=60)

            with ui.tab_panel(page_parameters):
                ui.label('Parameters')

            with ui.tab_panel(page_settings):
                ui.label("Settings").classes("text-lg")
                with ui.grid(columns="200px 600px"):
                    ui.label("Git Mode")
                    git_mode = ui.select(["local", "remote"], value=settings["git_mode"])
                    ui.label("Git URL")
                    git_url = ui.input(value=settings["git_url"], placeholder="Git Server URL")
                    ui.label("Username")
                    username = ui.input(value=settings["username"], placeholder="Username")
                    ui.label("Auth Token")
                    auth_token = ui.input(value=settings["auth_token"], placeholder="Auth Token")
                    ui.button("Save Settings", on_click=update_settings)

            


# Run the app
# ui.run()
