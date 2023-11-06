'''
Copyright (C) 2023 Powersprouter
https://powersprouter.com
andrew@powersprouter.com
Created by Powersprouter.

This file is the free utility software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation; either version 3
    of the License, or (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program; if not, see <https://www.gnu.org
/licenses>.
''' 




bl_info = {
    "name": "Cube Exploder",
    "author": "andrew <andrew@powersprouter.com>",
    "version": (0,8,7),
    "blender": (3, 6, 0),
    "location": "View3D > UI Sidebar",
    "description": "Ka-boom",
    "warning": "",
    "doc_url": "www.powersprouter.com",
    "category": "Mine",
}

import bpy
from bpy.app.handlers import persistent

#local imports
from .cubeExploder import OBJECT_OT_cube_remove_detritus_operator
from .cubeExploder import OBJECT_OT_cube_setup_operator
from .cubeExploder import OBJECT_OT_cube_exploder_operator

from .loadSounds import SEQUENCE_EDITOR_OT_load_Sounds_operator
from .loadSounds import SEQUENCE_EDITOR_OT_unload_Sounds_operator




explosions = (
    ('0','Your Basic Daily Explosion',''),
    ('1','More Massive Destruction',''),
    ('2','Annihilate to Smithereens',''),
    )

bpy.types.Scene.obj_type = bpy.props.EnumProperty(items = explosions)

@persistent
def cube_explode_play_once(scene):
    scene = bpy.data.scenes['Scene']
    frame_end = bpy.data.scenes['Scene'].frame_end    

    if scene.frame_current == frame_end:
        bpy.ops.screen.animation_cancel(restore_frame=False)
        print("where do we go from here")
        print("trying to remove detritus bc handler stopped")
        bpy.ops.object.cube_remove_detritus_operator()


    return {'FINISHED'}

class VIEW3D_PT_cube_exploder_panel (bpy.types.Panel):
    bl_label = "Cube Exploder"
    bl_idname = "CUBEEXPLODER_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Cube Exploder'
    bl_options = {'HIDE_HEADER'}

    def draw(self, context):
        scene = bpy.context.scene
        screen = bpy.context.screen
        layout = self.layout

        box = layout.box()
        box.scale_y = 4


        try:

            if bpy.data.objects["Cube"]:           

                if not screen.is_animation_playing:
                    box.scale_y = 4
                    box.operator("object.cube_exploder_operator", text="CUBE EXPLODER",)

                try:
                    if bpy.data.objects["DupeCube"]:
                        if screen.is_animation_playing:
                            box.scale_y = 4
                            box.operator("screen.animation_play", text="", icon='PAUSE')


                except:                            
                    if screen.is_animation_playing:
                        box.scale_y = 4
                        box.operator("object.cube_exploder_operator", text="CUBE EXPLODER",)

        except:

            box.label(text='       default cube exploded')



class VIEW3D_PT_settings_panel (bpy.types.Panel):
    bl_label = "Advanced Settings"
    bl_idname = "SETTINGS_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Cube Exploder'
    bl_options = {"DEFAULT_CLOSED"}


    def draw(self, context):
        scene = context.scene
        screen = context.screen
        layout = self.layout
        col1 = layout.column()
        col1.label(text="Select explosion type:")
        col1.prop(context.scene, 'obj_type', expand=True)

        layout.separator()
        row=layout.row()
        row.scale_y=8
        row.row()   
        row=layout.row()

        row.alignment = "RIGHT"
        
        try:
            if bpy.data.objects["Cube"]:
                row.enabled = False
                row=layout.row()
                
        except:
            row.operator("mesh.primitive_cube_add", text="Reset", icon='MESH_CUBE')

        
class VIEW3D_PT_extreme_panel (bpy.types.Panel):
    bl_label = "Cube Exploder Extreme"
    bl_idname = "EXTREME_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Cube Exploder'
    bl_options = {"DEFAULT_CLOSED"}


    def draw(self, context):
        scene = context.scene
        screen = context.screen
        layout = self.layout
        box = layout.box()
        box.scale_y = .5
        box.alignment = 'CENTER'
        row=box.row()
        box.label(text="            ~ * ~ * ~ * ~ ")
        box.label(text="    Why have an ordinary")
        box.label(text="    explosion when you can")
        box.label(text="    have an extreme one??")  
        layout.separator()
        row=box.row()        
        row=box.row()
        box.label(text="           GET EXTREME !")
        row=box.row()
        row=box.row()
        row=layout.row()
        row.scale_y = 1
        row.alignment = "RIGHT"
        row.operator('wm.url_open', text='Yes! I want this', icon='KEY_HLT').url='https://powersprouter.gumroad.com/l/rxftfw'        
        row=row.row()
        row=box.row()


#register multiple classes

classes = [
OBJECT_OT_cube_remove_detritus_operator,
OBJECT_OT_cube_setup_operator,
OBJECT_OT_cube_exploder_operator,

VIEW3D_PT_cube_exploder_panel,
VIEW3D_PT_settings_panel,
VIEW3D_PT_extreme_panel,

SEQUENCE_EDITOR_OT_load_Sounds_operator,
SEQUENCE_EDITOR_OT_unload_Sounds_operator,
]

def register():
    
    for cls in classes:

        bpy.utils.register_class(cls)
##register new property for a checkbox bool    
    bpy.types.Scene.cube_play_once_prop = bpy.props.BoolProperty(
    name="Cube Play Once",
    description="Toggle on/off Cube Play Once",
    default = True)
    bpy.app.handlers.frame_change_pre.append(cube_explode_play_once)
    print('ok now im here')


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)

##unregister new property for the checkbox bool    
    del bpy.types.Scene.cube_play_once_prop
    bpy.app.handlers.frame_change_pre.remove(cube_explode_play_once)    

if __name__ == "__main__":

    register()
    
