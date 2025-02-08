# TODO: this concept is broken and needs to be fixed

# [Imports]                     #| Details and Links
import copier                   #| [Copier Docs](https://copier.readthedocs.io/en/stable/)
import yaml
from pathlib import Path
from nicegui import ui          #| [NiceGUI Docs](https://nicegui.io/)

# Define paths
P__template_path = "./template"
P__output_path = "./output"

def load_copier_questions():
    """Load the copier.yaml file and return the defined questions."""
    copier_yaml_path = Path(P__template_path) / "copier.yaml"
    print(f"Loading Copier questions from: {copier_yaml_path}")
    with copier_yaml_path.open("r", encoding="utf-8") as file:
        data =  yaml.safe_load(file)
        print(f"Questions: {data}")
        return data

class BasePage:
    """
    Base class for a page in the Copier GUI.
    """
    def __init__(self, gui, questions):
        self.gui = gui
        self.questions = questions

    def render(self):
        raise NotImplementedError("Subclasses should implement this method")

class DynamicPage(BasePage):
    def render(self):
        for key,data in self.questions.items():
            print(f"Question: {data}, type: {type(data)}")
            ui.label(key)
            self.gui.responses[key] = ui.input(label=data['help'])

class FinalPage(BasePage):
    def render(self):
        ui.label("Final Step: Review and Generate")
        for key, input_field in self.gui.responses.items():
            ui.label(f"{key.capitalize()}: {input_field.value}")
        ui.button("Generate", on_click=self.gui.submit)

class CopierGUI:
    def __init__(self, questions):
        self.questions = questions
        self.current_step = 0
        self.responses = {}
        self.pages = [DynamicPage(self, questions), FinalPage(self, questions)]
        self.progress = ui.linear_progress(size=len(self.pages), value=0)
        self.render_step()

    def render_step(self):
        self.progress.set_value(self.current_step + 1)
        self.pages[self.current_step].render()
        ui.button("Next", on_click=self.next_step)
        if self.current_step > 0:
            ui.button("Previous", on_click=self.previous_step)

    def next_step(self):
        """Go to the next step."""
        if self.current_step < len(self.pages) - 1:
            self.current_step += 1
            self.render_step()

    def previous_step(self):
        """Go to the previous step."""
        if self.current_step > 0:
            self.current_step -= 1
            self.render_step()

    def submit(self):
        """Run Copier with collected responses."""
        response_dict = {key: input_field.value for key, input_field in self.responses.items()}
        copier.run_update(P__template_path, P__output_path, data=response_dict)
        ui.notify("Project generated successfully!", type="positive")

# Load questions and start GUI
questions = load_copier_questions()
CopierGUI(questions)
ui.run()
