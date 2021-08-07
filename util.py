import bpy
import mathutils
def _create_screw_head(bit_type, inner_radius, outer_radius, height, transform=mathutils.Matrix.Identity(4)):
    """Creates parametrized srew head and applies spatial transform
    (without the transform argument, the bottom plane of the head is equal to the xy-plane)"""
    argument_dictionary = {
        "change": False,
        "bf_Head_Type": "bf_Head_Cap",
        "bf_Cap_Head_Height": height,
        "bf_Cap_Head_Dia": 2 * outer_radius,
        "bf_Shank_Dia": outer_radius,
    }
    if bit_type == "None":
        argument_dictionary.update({
            "bf_Bit_Type": "bf_Bit_None"
            })
    elif bit_type == "Phillips":
        argument_dictionary.update({
            # Here is a typo (in the official addon-codebase) - One instead of two "l"s
            "bf_Bit_Type": "bf_Bit_Philips",
            "bf_Phillips_Bit_Depth": height * 0.75,
            "bf_Philips_Bit_Dia": 2 * inner_radius
            })
    elif bit_type == "Allen":
        argument_dictionary.update({
            # Here is a typo (in the official addon-codebase) - One instead of two "l"s
            "bf_Bit_Type": "bf_Bit_Allen",
            "bf_Allen_Bit_Depth": height * 0.75,
            "bf_Allen_Bit_Flat_Distance": 2 * inner_radius
            })
    elif bit_type == "Torx":
        argument_dictionary.update({
            "bf_Bit_Type": "bf_Bit_Torx",
            "bf_Torx_Bit_Depth": height * 0.75,
            "bf_Torx_Size_Type": "bf_Torx_T20"
            })
        
    bpy.ops.mesh.bolt_add(**argument_dictionary)
    screw = bpy.context.object
    screw.data.transform(mathutils.Matrix.Translation(mathutils.Vector((0,0,-0.01 * outer_radius - 5.25))))
    screw.data.update()
    #bpy.context.scene.objects.active = screw
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.bisect(plane_co=[0,0,0], plane_no=[0,0,1], clear_inner=True)
    bpy.ops.object.mode_set(mode="OBJECT")
    screw.data.transform(transform)
    screw.data.update()
    return screw