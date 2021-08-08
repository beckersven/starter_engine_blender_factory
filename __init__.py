
bl_info = {
    "name" : "Starter Engine Factory",
    "author" : "Sven Becker, working student of Jan-Philipp Kaiser at wbk",
    "description" : "Create a customized starter engine model in Blender",
    "blender" : (2, 90, 1),
    "version" : (0, 0, 1),
    "location" : "Lausanne, CH",
    "warning" : "Early development stage - Errors might occur!",
    "category" : "Object"
}

import bpy
from bpy.props import *
import json
from inspect import getargspec, getmembers, isfunction

from . starter_engine_operator import StarterEngineOperator
from . import component_generator_util




def parse_and_process_parameters(parameter_file = "parameters", target_class = StarterEngineOperator):

    with open(parameter_file, "r") as ifile:
        parameters = json.loads(ifile.read())
    
    def _enum_wrapper(**kwargs):
        """JSON in docstring can not contain tuples, so lists must be converted to work with blender-python's EnumProperty"""
        items_as_tuples = []
        for item in kwargs["items"]:
            items_as_tuples.append(tuple(item))
        kwargs["items"] = items_as_tuples
        return EnumProperty(**kwargs)
    property_translator = {
        "float": FloatProperty,
        "int": IntProperty,
        "enum": _enum_wrapper,
        "bool": BoolProperty
    }
    for parameter_name, parameter_properties in parameters.items():
            parameter_properties["properties"].update({"attr": parameter_name})
            setattr(target_class, parameter_name, property_translator[parameter_properties["type"]](**parameter_properties["properties"]))
    return parameters.keys()

def parse_and_process_components(source_module = component_generator_util, target_class = StarterEngineOperator):
    available_component_generators = getmembers(source_module, isfunction)
    type_dict = {}
    for component_generator in available_component_generators:
        for component_generator_type in json.loads(component_generator[1].__doc__):
            
            if component_generator_type not in type_dict.keys():
                type_dict.update({component_generator_type: [component_generator[1]]})
            else:
                type_dict[component_generator_type].append(component_generator[1])
    setattr(target_class, "part_type", EnumProperty(
        attr="part_type",
        name="Type",
        description="Select part type. Different shapes or input parameters might come available.", 
        items=[(key, key, "Part type {}".format(key)) for key in type_dict.keys()],

        ))
    setattr(target_class, "component_generators", type_dict)
    return type_dict

def check_configuration(parameters, type_dict):
    used_parameters = set()
    for component_generator_type, component_generators in type_dict.items():
        user_input_parameters = set()
        for component_generator in component_generators:
            if getargspec(component_generator).args is None:
                continue
            for i, argument in enumerate(getargspec(component_generator).args):
                if argument not in parameters:
                    raise(Exception("Component with function '{}' requires argument '{}' which is not part of 'parameters'-file!".format(component_generator.__name__, argument)))
                if getargspec(component_generator).defaults is None:
                    default_length = 0
                else:
                    default_length = len(getargspec(component_generator).defaults)
                if i < len(getargspec(component_generator).args) - default_length:
                    if argument in user_input_parameters:
                        print("[WARNING!] Property '{}' will have redundant user-input in function '{}' (it is already non-default kwarg in another function)".format(argument, component_generator.__name__))
                        bpy.context.window_manager.popup_menu(lambda self, context: self.layout.label(text="Redundant user input parameters - Check console"), title="Sloppy Configuration", icon='ERROR')
                    else:
                        user_input_parameters.add(argument)
        used_parameters = used_parameters.union(user_input_parameters)
    
    unused_parameters = set(parameters) - used_parameters
    if len(unused_parameters) > 0:
        print("[WARNING!] Properties {} are unused and causing overhead".format(unused_parameters))
        bpy.context.window_manager.popup_menu(lambda self, context: self.layout.label(text="Unused properties found - Check console"), title="Sloppy Configuration", icon='ERROR')


def register():
    
    
    check_configuration(parse_and_process_parameters(), parse_and_process_components())
    bpy.utils.register_class(StarterEngineOperator)
    bpy.types.VIEW3D_MT_mesh_add.append(lambda self, context: self.layout.operator(StarterEngineOperator.bl_idname, text="Starter Engine", icon="CONSTRAINT"))
def unregister():
    bpy.utils.unregister_class(StarterEngineOperator)

