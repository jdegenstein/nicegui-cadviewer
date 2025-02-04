
# Setup for usage

---
```shell
python3 -m venv .venv
source .venv/bin/activate
which python
which pip
```
---

Should show `...your path.../nicegui-cadviewer/.venv/bin/python`
and `...your path.../nicegui-cadviewer/.venv/bin/pip`

Now install the dependencies:
- ocp_vscode
- build123d
- nicegui
- pywebview

---
```
pip install ocp_vscode
pip install nicegui
pip install pywebview
pip list | grep ocp_vscode
pip list | grep build123d
pip list | grep nicegui
pip list | grep pywebview
```
---

Should show
---
```
ocp_vscode         2.6.1
build123d          0.9.0
nicegui            2.10.1
pywebview          5.3.2
```
---


# Setup for development 

follow the steps above but add the last build version for `build123d` with:

---
````
pip install git+https://github.com/gumyr/build123d.git
pip install pyyaml
pip install gitpython
pip install click
pip install rich




```
---



 
