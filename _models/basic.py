from build123d import * 
from ocp_vscode import show_all


with BuildPart() as mounting_ring:
    with BuildSketch() as sk1:
        with PolarLocations(radius=120, count=6, start_angle=0, angular_range=360):
            Rectangle(14 * 2, 20)
    extrude(amount=10, both=True)
    with BuildSketch() as sk2:
        Circle(150)
        Circle(128, mode=Mode.SUBTRACT)
    extrude(amount=10, mode=Mode.SUBTRACT, both=True)
    with BuildSketch(Plane.XZ) as sk3:
        Rectangle(123, 10, align=(Align.MIN, Align.CENTER))
        chamfer(sk3.vertices(), 1)
    revolve(mode=Mode.SUBTRACT)

show_all()