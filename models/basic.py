from build123d import *
from ocp_vscode import *

with BuildPart() as p:
    with BuildSketch(Plane.XY.offset(0.5)) as s:
        with Locations(Rotation(Z=-90)):
            Circle(0.8)
    with BuildSketch() as s:
        with Locations(Rotation(Z=-90)):
            Circle(0.5)
    loft()
    with BuildLine() as l:
        m1 = FilletPolyline([(0, 0, 0), (0, 0, -2), (-6, 0, -2)], radius=1.25)
    sweep(s.sketch, path=l.line)

with BuildPart() as p2:
    add(p.part)
    with Locations((-3, 0, 0)):
        add(p.part)
    sect = section(p2.part,section_by=Plane.YZ.offset(-3))
    # extrude(sect,amount=-3)
    with BuildSketch(Plane.YZ.offset(-3)) as s:
        with Locations(Rotation(Z=-90)):
            add(sect)
        with Locations((0,-1)):
            SlotCenterToCenter(2,1,rotation=90)
    extrude(amount=3)

show(p.part,p2.part)
