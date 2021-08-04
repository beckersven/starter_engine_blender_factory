import bpy
import os
from bpy.props import *
from bpy_extras import object_utils
from bpy_extras.object_utils import AddObjectHelper
from . import component_generator_util
from inspect import getargspec, getmembers, isfunction
import json

def parse_options(module = component_generator_util):
        available_component_generators = getmembers(module, isfunction)
        parsed_component_generators = {}
        property_translator = {
            "float": FloatProperty,
            "int": IntProperty
        }
        for component_generator in available_component_generators:
            new_component = {"function": component_generator[1], "properties":{}}
            for argument in json.loads(component_generator[1].__doc__):
                new_component["properties"].update({argument["properties"]["attr"]: property_translator[argument["type"]](name="A")})
            parsed_component_generators[component_generator[0]] = new_component
        return parsed_component_generators


class StarterEngineOperator(bpy.types.Operator,AddObjectHelper):
    
    bl_idname = "mesh.add_starter_engine"
    bl_label = "Starter Engine Properties"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}
    bl_description = "Add and configure new starter engine"    
    
    @classmethod
    def poll(cls, context):
        return context.scene is not None
    

    def get_propertydict_from_prototype(self, function):
        output_dict = {}
        try:
            for argument in getargspec(function).args:
                output_dict.update({argument: getattr(self, argument)})
        except Exception as e:
            # May add some functionality later on
            raise(e)
        return output_dict



    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.label(text="General")
        for component in self.component_generators:
            for prop in self.get_propertydict_from_prototype(component).keys():
                print(prop)
                col.prop(self, prop)
        #return {"FINISHED"}

    def execute(self, context):

        objects = []
        for component in self.component_generators:
            for sub_object in component(** self.get_propertydict_from_prototype(component)):
                objects.append(sub_object)
        bpy.ops.object.select_all(action='DESELECT')
        for obj in objects:
            obj.select_set(True)
        bpy.ops.object.join()
        return {"FINISHED"}
    


   

    



