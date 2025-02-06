from build123d import *
from ocp_vscode import *

with BuildPart() as main:
    Sphere(9)

main.part.color = "#4422FFEE"
main.part.name = "second"


show(main.part)