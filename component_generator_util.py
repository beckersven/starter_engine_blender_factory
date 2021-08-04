import bpy
import os
from bpy.props import *
from bpy_extras import object_utils
from bpy_extras.object_utils import AddObjectHelper

# def create_gearbox():
#     pass

def main_housing(main_housing_radius, main_housing_height):
    """
    [     
        {"type": "float", "properties": {"attr":"main_housing_height", "name": "Height (main housing)", "subtype": "DISTANCE", "unit": "LENGTH", "default": 1.0, "min": 0.1, "max": 10}},
        {"type": "float", "properties": {"attr":"main_housing_radius", "name": "Radius (main)", "subtype": "DISTANCE", "unit": "LENGTH", "default": 1.0, "min": 0.1, "max": 10}}
    ]
    """
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=main_housing_radius, depth=main_housing_height, location=(0,0,0))
    yield bpy.context.object

# def create_sub_parts(shaft_radius, shaft_length, z_offset=0):
#     bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=shaft_radius, depth=shaft_length, location=(0,0,z_offset))
#     obj = bpy.context.object
#     obj.name = "sub_shaft"
#     yield obj
    