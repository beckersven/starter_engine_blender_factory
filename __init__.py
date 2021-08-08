# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

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




def parse_and_process_parameters(parameter_file = "parameters.yaml", target_class = StarterEngineOperator):
    with open("parameters", "r") as ifile:
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

def check_configuration():
    pass

def register():
    parse_and_process_parameters()
    parse_and_process_components()
    # bpy.ops.preferences.addon_enable(module="add_mesh_extra_objects")
    bpy.utils.register_class(StarterEngineOperator)


def unregister():
    bpy.utils.unregister_class(StarterEngineOperator)

