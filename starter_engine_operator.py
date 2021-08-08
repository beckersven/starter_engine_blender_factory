import bpy
import os
from bpy.props import *
from bpy_extras import object_utils
from bpy_extras.object_utils import AddObjectHelper
from . import component_generator_util
from inspect import getargspec
import json

class StarterEngineOperator(bpy.types.Operator,AddObjectHelper):
    
    bl_idname = "mesh.add_starter_engine"
    bl_label = "Starter Engine Properties"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}
    bl_description = "Add and configure new starter engine"    


    @classmethod
    def poll(cls, context):
        return context.scene is not None
    

    def get_propertydict_from_prototype(self, function, reduced):
        if getargspec(function).args is None:
            return dict()
        output_dict = {}
        if reduced and getargspec(function).defaults is not None:
            deductable = len(getargspec(function).defaults)
        else:
            deductable = 0
        try:
            for i in range(len(getargspec(function).args) - deductable):
                output_dict.update({getargspec(function).args[i]: getattr(self, getargspec(function).args[i])})
        except Exception as e:
            # May add some functionality later on
            raise(e)
        return output_dict



    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.prop(self, "part_type")
        for component in self.component_generators[self.part_type]:
            col.label(text=component.__name__.replace("_", " "))
            for prop in self.get_propertydict_from_prototype(component, True).keys():
                col.prop(self, prop)
            col.separator()

    def execute(self, context):
        objects = []
        for component in self.component_generators[self.part_type]:
            for sub_object in component(** self.get_propertydict_from_prototype(component, False)):
                objects.append(sub_object)
        bpy.ops.object.select_all(action='DESELECT')
        for obj in objects:
            obj.select_set(True)
        bpy.ops.object.join()
        bpy.context.object.name="starter_engine"
        return {"FINISHED"}
