"""
  ViewerSettings -> @dataclass 

file                : _settings/viewer.yaml
file-id             : 0c9c1891-1c1b-4a83-bd0d-323fb3c78011
project             : nice123d
project-id          : e2bbd03f-0ac6-41ec-89ae-2ad52fa0652a
using               : jinja2
description         : This file contains OCP_vscode parameters. | The file contains all setting of the `nice123d` model viewer.
author              : felix@42sol.eu
"""

from dataclasses import dataclass

@dataclass
class ViewerSettings:
    default_port: int
    ambient_intensity: float
    angular_tolerance: float
    axes: bool
    axes0: bool
    black_edges: bool
    center_grid: bool
    collapse: str
    control: str
    debug: bool
    default_color: str
    default_edgecolor: str
    default_facecolor: str
    default_opacity: float
    default_thickedgecolor: str
    default_vertexcolor: str
    deviation: float
    direct_intensity: float
    explode: bool
    grid_xy: bool
    grid_xz: bool
    grid_yz: bool
    metalness: float
    new_tree_behavior: bool
    no_glass: bool
    no_tools: bool
    pan_speed: float
    perspective: bool
    rotate_speed: float
    roughness: float
    theme: str
    ticks: int
    transparent: bool
    tree_width: int
    up: str
    zoom_speed: float
    modifier_keys__ctrl: str
    modifier_keys__meta: str
    modifier_keys__shift: str
