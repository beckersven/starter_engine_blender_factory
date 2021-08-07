import bpy
import os
from bpy.props import *
from bpy_extras import object_utils
from bpy_extras.object_utils import AddObjectHelper
import numpy as np
import mathutils
from . import util
from random import random

def main_housing(main_housing_radius, main_housing_height):
    """
    [   
        {"type": "float", "properties": {"attr":"main_housing_height", "name": "Height (main housing)", "subtype": "DISTANCE", "unit": "LENGTH", "default": 3.0, "min": 0.1, "max": 10}},
        {"type": "float", "properties": {"attr":"main_housing_radius", "name": "Radius (main housing)", "subtype": "DISTANCE", "unit": "LENGTH", "default": 1.0, "min": 0.1, "max": 10}}
    ]
    """
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=main_housing_radius, depth=main_housing_height, location=(0,0,0))
    bpy.context.object.location.z = main_housing_height / 2.0
    mat = bpy.data.materials.new(name="Material") 
    bpy.context.object.data.materials.append(mat) 
    bpy.context.object.active_material.diffuse_color = (0.05, 0.05, 0.05, 1) 
    yield bpy.context.object


def subside(shaft_radius, shaft_length, bit_type, screw_amount, screw_radius, screw_placement_radial, screw_placement_tangential,
    main_housing_radius=0):
    """
    [     
        {"type": "float", "properties": {"attr":"shaft_radius", "name": "Radius (shaft)", "subtype": "DISTANCE", "unit": "LENGTH", "default": 0.2, "min": 0.0, "max": 10}},
        {"type": "float", "properties": {"attr":"shaft_length", "name": "Length (shaft)", "subtype": "DISTANCE", "unit": "LENGTH", "default": 0.3, "min": 0.0, "max": 10}},
        {"type": "enum", "properties": {"attr":"bit_type", "name": "Bit type (screws)", "items": [["Allen", "ALLEN", "Hexagon-shaped"], ["Torx", "TORX", "Star-shaped"], ["Phillips", "PHILLIPS", "Cross-shaped"], ["None", "NONE", "No shape"]],"default": "Phillips"}},
        {"type": "int", "properties": {"attr":"screw_amount", "name": "Amount (screws)", "default": 0, "min": 0, "max": 10}},
        {"type": "float", "properties": {"attr":"screw_radius", "name": "Size (screws)", "subtype": "DISTANCE", "unit": "LENGTH", "default": 0.2, "min": 0.1, "max": 10}},
        {"type": "float", "properties": {"attr":"screw_placement_radial", "name": "Radial Placement (screws)", "subtype": "DISTANCE", "unit": "LENGTH", "default": 0.7, "min": 0.1, "max": 10}},
        {"type": "float", "properties": {"attr":"screw_placement_tangential", "name": "Tangential Placement (screws)", "subtype": "DISTANCE", "unit": "LENGTH", "default": 1.0, "min": 0.1, "max": 10}}
    ]
    """
    angles = [np.deg2rad(i * 360 / screw_amount) + screw_placement_tangential for i in range(screw_amount)]
    for angle in angles:
        yield util._create_screw_head(bit_type, screw_radius * 0.6, screw_radius, screw_radius * 0.5, 
            mathutils.Matrix.Rotation(angle, 4, "Z") @ mathutils.Matrix.Translation(mathutils.Vector((screw_placement_radial, 0, 0))) @ mathutils.Matrix.Rotation(random(), 4, "Z") @ mathutils.Matrix.Rotation(np.deg2rad(180), 4, "X"))
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=shaft_radius, depth=shaft_length, location=(0,0,-shaft_length / 2))
    mat = bpy.data.materials.new(name="Material") 
    bpy.context.object.data.materials.append(mat) 
    bpy.context.object.active_material.diffuse_color = (0.05, 0.05, 0.05, 1) 
    yield bpy.context.object

def cap(cap_height, cap_narrowing, cap_shape, main_housing_height=0, main_housing_radius=0, connector_height=0, flange_height=0):
    """
    [     
        {"type": "float", "properties": {"attr":"cap_height", "name": "Height (cap)", "subtype": "DISTANCE", "unit": "LENGTH", "default": 0.2, "min": 0.0, "max": 5}},
        {"type": "float", "properties": {"attr":"cap_narrowing", "name": "Narrowing (cap)", "subtype": "DISTANCE", "unit": "LENGTH",  "default": 0.2, "min": 0.0, "max": 5}},
        {"type": "float", "properties": {"attr":"cap_shape", "name": "Shape modifier (cap)", "default": 6.0, "min": 1.0, "max": 10.0}}
    ]
    """
    b = cap_height / ((main_housing_radius)**(2 * cap_shape)-(main_housing_radius-cap_narrowing)**(2 * cap_shape))
    a = b * main_housing_radius ** (2 * cap_shape)
    
    bpy.ops.mesh.primitive_z_function_surface(size_x = main_housing_radius * 2, size_y= 2 * main_housing_radius, div_x=64, div_y=64, equation="{}-{}*((x**2+y**2) ** {})".format(a, b, cap_shape))
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.bisect(plane_co=[0,0,0], plane_no=[0,0,1], clear_inner=True, clear_outer= False, use_fill=True)
    bpy.ops.mesh.select_linked()
    bpy.ops.mesh.bisect(plane_co=[0,0,cap_height], plane_no=[0,0,1], clear_inner=False, clear_outer= True, use_fill=True)
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.context.object.data.transform(mathutils.Matrix.Translation(mathutils.Vector((0, 0, main_housing_height + connector_height + flange_height))))
    bpy.context.object.data.update()
    mat = bpy.data.materials.new(name="Material") 
    bpy.context.object.data.materials.append(mat) 
    bpy.context.object.active_material.diffuse_color = (0.95, 0.95, 0.95, 1) 
    yield bpy.context.object

def gearbox(gear_height, gear_radius, gear_cone_angle, gear_number_of_teeth, gear_housing, gear_housing_shape, gear_housing_opening_angle, gear_housing_opening_offset,gear_housing_thickness,
    main_housing_radius=0, main_housing_height=0, cap_narrowing=0, cap_height=0, connector_height=0, flange_height=0):
    """
    [     
        {"type": "float", "properties": {"attr":"gear_height", "name": "Height (gear)", "subtype": "DISTANCE", "unit": "LENGTH", "default": 0.5, "min": 0.0, "max": 10}},
        {"type": "float", "properties": {"attr":"gear_radius", "name": "Radius (gear)", "subtype": "DISTANCE", "unit": "LENGTH", "default": 0.5, "min": 0.0, "max": 10}},
        {"type": "float", "properties": {"attr":"gear_cone_angle", "name": "Cone angle (gear)", "subtype": "ANGLE", "unit": "ROTATION", "default": 0.0, "min": 0.0, "max": 1.57}},
        {"type": "int", "properties": {"attr":"gear_number_of_teeth", "name": "Number of teeth (gear)", "subtype": "UNSIGNED", "default": 30, "min": 2, "max": 100}},
        {"type": "bool", "properties": {"attr":"gear_housing", "name": "Gear Housing", "default": true}},
        {"type": "float", "properties": {"attr":"gear_housing_shape", "name": "Shape modifier (gear housing)", "default": 2.0, "min": 1.0, "max": 10.0}},
        {"type": "float", "properties": {"attr":"gear_housing_opening_angle", "name": "Opening angle (gear housing)", "subtype": "ANGLE", "unit": "ROTATION", "default": 0.0, "min": 0.0, "max": 6.2831}},
        {"type": "float", "properties": {"attr":"gear_housing_opening_offset", "name": "Opening offset (gear housing)", "subtype": "ANGLE", "unit": "ROTATION", "default": 0.0, "min": 0.0, "max": 6.2831}},
        {"type": "float", "properties": {"attr":"gear_housing_thickness", "name": "Thickness (gear housing)", "subtype": "DISTANCE", "unit": "LENGTH", "default": 0.05, "min": 0.001, "max": 10}}
    ]
    """
    if gear_radius > main_housing_radius - 0.1 - cap_narrowing:
        gear_radius = main_housing_radius - 0.1 - cap_narrowing
    if gear_radius - 0.1 - cap_narrowing < np.tan(gear_cone_angle) * 2.0 * gear_height:
        gear_height = (gear_radius - 0.1 - cap_narrowing) / np.tan(gear_cone_angle) / 2.0

    bpy.ops.mesh.primitive_gear(change=False, number_of_teeth=gear_number_of_teeth, conangle=gear_cone_angle, width=gear_height, radius=gear_radius, base=gear_radius - 0.1)
    bpy.context.object.location.z = main_housing_height + gear_height + cap_height + connector_height + flange_height
    yield bpy.context.object
    if gear_housing:

        main_housing_radius = main_housing_radius - gear_housing_thickness - cap_narrowing
        a = 2 * gear_height * main_housing_radius ** (2 * gear_housing_shape) / (main_housing_radius ** (2 * gear_housing_shape) - (gear_radius + 0.1) ** (2 * gear_housing_shape))
        b = 2 * gear_height / (main_housing_radius ** (2 * gear_housing_shape) - (gear_radius + 0.1) ** (2 * gear_housing_shape))
        
        bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=gear_radius * 0.2, depth=a - 2 * gear_height, location=(0,0,(a - 2 * gear_height) / 2 + 2 * gear_height + cap_height + main_housing_height + connector_height + flange_height))
        yield bpy.context.object
        
        
        def _create_cap(gear_housing_opening_angle):

            bpy.ops.mesh.primitive_z_function_surface(size_x = 2 * main_housing_radius, size_y= 2* main_housing_radius, div_x=64, div_y=64, equation="{}-{}*((x**2+y**2) ** {})".format(a, b, gear_housing_shape))
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.bisect(plane_co=[0,0,0], plane_no=[0,0,1], clear_inner=True, use_fill=False)
            bpy.ops.mesh.select_linked()
            bpy.ops.mesh.bisect(plane_co=[0,0,0], plane_no=[0,1,0], clear_inner=True, use_fill=False)
            bpy.ops.mesh.select_linked()
            bpy.ops.mesh.bisect(plane_co=[0,0,0], plane_no=[-np.sin(gear_housing_opening_angle),np.cos(gear_housing_opening_angle),0], clear_inner=False, clear_outer=True)
            bpy.ops.object.mode_set(mode="OBJECT")
            modifier = bpy.context.object.modifiers.new(name="Thickness", type="SOLIDIFY")
            modifier.thickness = -1 * gear_housing_thickness
            modifier.offset = -1.0
            bpy.ops.object.modifier_apply(modifier="Thickness")

            bpy.context.object.data.transform(mathutils.Matrix.Translation(mathutils.Vector((0, 0, main_housing_height + cap_height + connector_height + flange_height))))
            bpy.context.object.data.update()
            bpy.context.object.data.transform(mathutils.Matrix.Rotation(gear_housing_opening_offset, 4, "Z"))
            bpy.context.object.data.update()
            return bpy.context.object

        if gear_housing_opening_angle > np.deg2rad(180):
            yield _create_cap(np.deg2rad(180))
            b = _create_cap(gear_housing_opening_angle - np.deg2rad(180))
            b.data.transform(mathutils.Matrix.Rotation(np.deg2rad(180), 4, "Z"))
            b.data.update()
            yield b
        else:
            yield _create_cap(gear_housing_opening_angle)
    else:
        bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=gear_radius * 0.2, depth=gear_height, location=(0,0,gear_height / 2 + cap_height + main_housing_height + connector_height + flange_height))
        yield bpy.context.object
def connector(connector_height, connector_width, connector_length, solenoid_housing_radius=0, main_housing_radius=0, main_housing_height=0):
    """
    [     
        {"type": "float", "properties": {"attr":"connector_height", "name": "Height", "subtype": "DISTANCE", "unit": "LENGTH", "default": 0.5, "min": 0.0, "max": 10}},
        {"type": "float", "properties": {"attr":"connector_width", "name": "Width (crosspiece)", "subtype": "DISTANCE", "unit": "LENGTH", "default": 0.8, "min": 0.0, "max": 10}},
        {"type": "float", "properties": {"attr":"connector_length", "name": "Length (crosspiece)", "subtype": "DISTANCE", "unit": "LENGTH", "default": 0.5, "min": 0.0, "max": 10}}
    ]
    """
    connector_width = min([2*main_housing_radius, 2*solenoid_housing_radius, connector_width])
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=main_housing_radius, depth=connector_height, location=(0,0,main_housing_height + connector_height / 2.0))
    yield bpy.context.object
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=solenoid_housing_radius, depth=connector_height, location=(connector_length + main_housing_radius + solenoid_housing_radius,0,main_housing_height + connector_height / 2.0))
    yield bpy.context.object
    bpy.ops.mesh.primitive_cube_add(location=((main_housing_radius + connector_length + solenoid_housing_radius) / 2.0, 0, main_housing_height + connector_height / 2.0))
    bpy.context.object.scale[0] = (solenoid_housing_radius + main_housing_radius + connector_length) / 2.0
    bpy.context.object.scale[1] = connector_width / 2.0
    bpy.context.object.scale[2] = connector_height / 2.0
    yield bpy.context.object

def solenoid(solenoid_housing_radius, solenoid_housing_height, main_housing_radius=0, main_housing_height=0, connector_length=0):
    """
    [     
        {"type": "float", "properties": {"attr":"solenoid_housing_radius", "name": "Radius (solenoid housing)", "subtype": "DISTANCE", "unit": "LENGTH", "default": 0.5, "min": 0.0, "max": 10}},
        {"type": "float", "properties": {"attr":"solenoid_housing_height", "name": "Height (solenoid housing)", "subtype": "DISTANCE", "unit": "LENGTH", "default": 1.0, "min": 0.0, "max": 10}}
    ]
    """
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=solenoid_housing_radius, depth=solenoid_housing_height, location=(connector_length + main_housing_radius + solenoid_housing_radius,0,main_housing_height - solenoid_housing_height / 2.0))
    yield bpy.context.object

def flange(flange_amount_prongs, flange_height, flange_length_prongs, flange_angle_offset, main_housing_radius=0, main_housing_height=0, connector_height=0):
    """
    [     
        {"type": "int", "properties": {"attr":"flange_amount_prongs", "name": "Amount of prongs (flange)", "default": 2, "min": 1, "max": 6}},
        {"type": "float", "properties": {"attr":"flange_height", "name": "Height (flange)", "subtype": "DISTANCE", "unit": "LENGTH", "default": 0.2, "min": 0.0, "max": 3}},
        {"type": "float", "properties": {"attr":"flange_length_prongs", "name": "Length (flange prongs)", "subtype": "DISTANCE", "unit": "LENGTH", "default": 0.2, "min": 0.0, "max": 3}},
        {"type": "float", "properties": {"attr":"flange_angle_offset", "name": "Angle offset (flange)", "subtype": "ANGLE", "unit": "ROTATION", "default": 0.0, "min": 0.0, "max": 6.2831}}
    ]
    """
    angles = [np.deg2rad(i * 360 / float(flange_amount_prongs)) + flange_angle_offset for i in range(flange_amount_prongs)]
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=main_housing_radius, depth=flange_height, location=(0,0,main_housing_height + connector_height + flange_height / 2.0))
    yield bpy.context.object
    for angle in angles:
        bpy.ops.mesh.make_triangle(triangleType="EQUILATERAL")
        bpy.context.object.scale[0] = 1.95 * main_housing_radius
        bpy.context.object.scale[1] = flange_length_prongs + main_housing_radius
        modifier = bpy.context.object.modifiers.new(name="Thickness", type="SOLIDIFY")
        modifier.thickness = flange_height
        modifier.offset = -1.0
        bpy.ops.object.modifier_apply(modifier="Thickness")
        triangle = bpy.context.object
        bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=0.1 * (flange_length_prongs + main_housing_radius), depth=flange_height*1.1, location=(0, (flange_length_prongs + main_housing_radius)*0.8,flange_height/2))
        drill_hole_outer = bpy.context.object
        bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=0.06 * (flange_length_prongs + main_housing_radius), depth=flange_height*1.2, location=(0, (flange_length_prongs + main_housing_radius)*0.8,flange_height/2))
        drill_hole_inner = bpy.context.object

        bool_op = triangle.modifiers.new(name="Boolean", type="BOOLEAN")
        bool_op.object = drill_hole_outer
        bool_op.operation = "UNION"
        bpy.ops.object.modifier_apply({"object": triangle},modifier="Boolean")

        bool_op = triangle.modifiers.new(name="Boolean", type="BOOLEAN")
        bool_op.object = drill_hole_inner
        bool_op.operation = "DIFFERENCE"
        bpy.ops.object.modifier_apply({"object": triangle},modifier="Boolean")

        bpy.ops.object.select_all(action='DESELECT')
        drill_hole_inner.select_set(True)
        drill_hole_outer.select_set(True)
        bpy.ops.object.delete(confirm=False)

        triangle.rotation_euler[2] = angle
        triangle.location[2] = connector_height + main_housing_height
        yield triangle
           