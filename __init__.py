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
    "version": (0,8,1),
    "blender": (3, 6, 0),
    "location": "View3D > UI Sidebar",
    "description": "Ka-boom",
    "warning": "",
    "doc_url": "www.powersprouter.com",
    "category": "Mine",
}

import bpy

#local imports

from .cubeExploder import OBJECT_OT_cube_setup_operator
from .cubeExploder import OBJECT_OT_cube_exploder_operator

from .playOnce import PLAYONCE_OT_remove_play_once_operator
from .playOnce import PLAYONCE_OT_play_once_operator

from .loadSounds import SEQUENCE_EDITOR_OT_load_Sounds_operator
from .loadSounds import SEQUENCE_EDITOR_OT_unload_Sounds_operator




explosions = (
    ('0','Your Basic Daily Explosion',''),
    ('1','More Massive Destruction',''),
    ('2','Annihilate to Smithereens',''),
    )

bpy.types.Scene.obj_type = bpy.props.EnumProperty(items = explosions)



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
        
# If we want to display the playOnce utility ---which DOES work on the exploding cubes        
#        row.prop(scene, "play_once_prop", text = "1x ON/OFF",)
#        row = layout.row()
#        row.operator("screen.frame_jump", text="", icon='REW').end = False
#        row.operator("screen.keyframe_jump", text="", icon='PREV_KEYFRAME').next = False
#        if not screen.is_animation_playing:
#            row.operator("screen.animation_play", text="", icon='PLAY_REVERSE').reverse = True
#            row.operator("object.play_once_operator", text="", icon='PLAY')
#        else:
#            row.scale_x = 2
#            row.operator("screen.animation_play", text="", icon='PAUSE')
#            row.scale_x = 1
#        row.operator("screen.keyframe_jump", text="", icon='NEXT_KEYFRAME').next = True
#        row.operator("screen.frame_jump", text="", icon='FF').end = True


#register multiple classes

classes = [
OBJECT_OT_cube_setup_operator,
OBJECT_OT_cube_exploder_operator,

PLAYONCE_OT_remove_play_once_operator,
PLAYONCE_OT_play_once_operator,

VIEW3D_PT_cube_exploder_panel,
VIEW3D_PT_settings_panel,
VIEW3D_PT_extreme_panel,

SEQUENCE_EDITOR_OT_load_Sounds_operator,
SEQUENCE_EDITOR_OT_unload_Sounds_operator,
]

def register():
    
    for cls in classes:

        bpy.utils.register_class(cls)
##register new property for the checkbox bool    
    bpy.types.Scene.play_once_prop = bpy.props.BoolProperty(
    name="Play Once",
    description="Toggle on/off Play Once",
    default = True)
            

def unregister():
      
    for cls in classes:
        bpy.utils.unregister_class(cls)
        
##unregister new property for the checkbox bool    
    del bpy.types.Scene.play_once_prop
    

if __name__ == "__main__":

    register()
    
