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
    "name" : "TEST",
    "author" : "Sven Becker, working student of Jan-Philipp Kaiser at wbk",
    "description" : "TEST",
    "blender" : (2, 90, 1),
    "version" : (0, 0, 1),
    "location" : "?",
    "warning" : "Early development stage - Errors might occur!",
    "category" : "Object"
}

import bpy
from bpy.props import *
import json

from inspect import getargspec, getmembers, isfunction

from . starter_engine_operator import StarterEngineOperator
from . import component_generator_util

def enum_wrapper(**kwargs):
    """JSON in docstring can not contain tuples, so lists must be converted to work with blender-python's EnumProperty"""
    items_as_tuples = []
    for item in kwargs["items"]:
        items_as_tuples.append(tuple(item))
    kwargs["items"] = items_as_tuples
    return EnumProperty(**kwargs)


def parse_and_process_generators(module = component_generator_util, target_class = StarterEngineOperator):
    available_component_generators = getmembers(module, isfunction)
    parsed_component_generators = []
    property_translator = {
        "float": FloatProperty,
        "int": IntProperty,
        "enum": enum_wrapper,
        "bool": BoolProperty
    }
    for component_generator in available_component_generators:
        for argument in json.loads(component_generator[1].__doc__):
            setattr(target_class, argument["properties"]["attr"], property_translator[argument["type"]](**argument["properties"]))
        parsed_component_generators.append(component_generator[1])
    
    
    setattr(target_class, "component_generators", parsed_component_generators)



def register():
    parse_and_process_generators()
    # bpy.ops.preferences.addon_enable(module="add_mesh_extra_objects")
    bpy.utils.register_class(StarterEngineOperator)


def unregister():
    bpy.utils.unregister_class(StarterEngineOperator)

