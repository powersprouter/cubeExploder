import bpy

import pathlib
    
def get_sound_directory():
    # check if we are running from the Text Editor
    if bpy.context.space_data != None and bpy.context.space_data.type == "TEXT_EDITOR":
        # get the path to the SAVED TO DISK script when running from blender
        script_path = bpy.context.space_data.text.filepath
    else:
        # __file__ is built-in Python variable that represents the path to the script
        script_path = __file__

    sound_directory = pathlib.Path(script_path).resolve().parent
    
    return sound_directory

def get_sound_file_name():

    if bpy.context.scene.obj_type == '0': #basic_daily_sound
        sound_file_name = 'kaboom.mp3'
        
    if bpy.context.scene.obj_type == '1': #more_massive_sound
        sound_file_name = 'gulp_more_massive.mp3'
        
    if bpy.context.scene.obj_type == '2': #annihilate_sound
        sound_file_name = 'annihilate_sound.mp3'
        
    return sound_file_name
    
    
    

def load_Sound(file_name, sound_directory):
    # get a path to a file that is next to the script
    sound_file_path = str(sound_directory / file_name)

    return sound_file_path

def basic_daily_sound():
    sound_file_name = "kaboom.mp3"
    sound_directory = get_sound_directory()
    sound_file_path = load_Sound(sound_file_name,sound_directory)
    bpy.data.scenes['Scene'].sequence_editor.sequences.new_sound(sound_file_name, sound_file_path, channel=7, frame_start = 23)
 
 
def more_massive_sound():
    sound_file_name = "gulp_more_massive.mp3"
    sound_directory = get_sound_directory()
    sound_file_path = load_Sound(sound_file_name,sound_directory)
    sound = bpy.data.scenes['Scene'].sequence_editor.sequences.new_sound(sound_file_name, sound_file_path, channel=7, frame_start = 14)
    sound.volume = .2

def annihilate_sound():
    sound_file_name = "annihilate_sound.mp3"
    sound_directory = get_sound_directory()
    sound_file_path = load_Sound(sound_file_name,sound_directory)
    bpy.data.scenes['Scene'].sequence_editor.sequences.new_sound(sound_file_name, sound_file_path, channel=7, frame_start = 14)
 
    

class SEQUENCE_EDITOR_OT_load_Sounds_operator(bpy.types.Operator):
    """creates load sounds technology"""
    bl_idname = "object.load_sounds_operator"
    bl_label = "sound to vse"
    
    def execute(self, context):   
        
        context = bpy.context.scene    
        print(f'bpy.context.scene.obj_type = {bpy.context.scene.obj_type}')

        if bpy.context.scene.obj_type == '0':
            basic_daily_sound()
            print(f'explosion type is Basic => {bpy.context.scene.obj_type}')
        
        if bpy.context.scene.obj_type == '1':
            more_massive_sound()
            print(f'explosion type is More Massive Destruction => {bpy.context.scene.obj_type}')

        if bpy.context.scene.obj_type == '2':
            annihilate_sound()
            print(f'explosion type is Annihilate to Smitherines => {bpy.context.scene.obj_type}')

        return {'FINISHED'}    
    
    
class SEQUENCE_EDITOR_OT_unload_Sounds_operator(bpy.types.Operator):
    """removes the loaded sound"""
    bl_idname = "object.unload_sounds_operator"
    bl_label = "unload sound from vse"
    
    def execute(self, context):   

        context = bpy.context.scene
        sound_file_name = get_sound_file_name()
        bpy.data.sounds.remove(bpy.data.sounds[sound_file_name])
        bpy.data.scenes['Scene'].sequence_editor_clear()
        bpy.data.scenes['Scene'].sequence_editor_create()
        
        return {'FINISHED'}