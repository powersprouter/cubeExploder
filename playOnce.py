import bpy

def play_once(scene):
    scene = bpy.data.scenes['Scene']
    frame_end = bpy.data.scenes['Scene'].frame_end    
   
    if scene.frame_current == frame_end:
        bpy.ops.screen.animation_cancel(restore_frame=False)
        remove_play_once(scene) 
        
def remove_play_once(scene):
    for h in bpy.app.handlers.frame_change_pre:
        if h.__name__ == 'play_once':
            bpy.app.handlers.frame_change_pre.remove(h)
        #else:
            #pass
            
            
class PLAYONCE_OT_play_once_operator(bpy.types.Operator):
    """creates play once technology"""
    bl_idname = "object.play_once_operator"
    bl_label = "Play"
    
    def execute(self, context):   
        if bpy.context.scene.play_once_prop:
            bpy.app.handlers.frame_change_pre.append(play_once)
            bpy.ops.screen.frame_jump(end=False)
            bpy.ops.screen.animation_play()
        
        else:
            bpy.ops.screen.animation_play()
        
        return {'FINISHED'}


class PLAYONCE_OT_remove_play_once_operator(bpy.types.Operator):
    """Removes Play Once in the handlers"""
    bl_idname = "object.remove_play_once_operator"
    bl_label = "Reset"
    
    def execute(self, context):
        scene = bpy.data.scenes['Scene']
        remove_play_once(scene)
        bpy.ops.screen.frame_jump(end=True)
        bpy.ops.screen.frame_jump(end=False)

        return {'FINISHED'}