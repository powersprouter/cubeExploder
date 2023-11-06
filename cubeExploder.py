import bpy
import pathlib
import random
import math
from math import radians

#scene = bpy.data.scenes['Scene']
#frame_end = bpy.data.scenes['Scene'].frame_end 

def selectOBJ(objectname):
    '''select object by name'''
    
    bpy.ops.object.select_all(action='DESELECT')
    
    try:        
        OBJ = bpy.data.objects[objectname]
        bpy.context.view_layer.objects.active = OBJ
        OBJ.select_set(True)
        
    except:
        pass

def delete_object(objectname):
    '''remove objects we no longer want'''
    
    try:
        print ("trying to remove", objectname)
        
        OBJ = bpy.data.objects[objectname]
        bpy.data.objects.remove(OBJ, do_unlink=True)
        print(objectname, "removed.")

        #now purge all datablocks   
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
        
    except:
        print ("there is no ", objectname)




def remove_detritus():

    bpy.ops.object.unload_sounds_operator()
    delete_object("Camera")
    delete_object("Light")
    delete_object("DupeCube")
    bpy.ops.screen.frame_jump(end=False)
    delete_object("Cube")

    if bpy.context.scene.obj_type == '2':
        for ob in bpy.context.scene.objects:
            if ob.name.startswith("Empty"):
                objectname = ob.name
                delete_object(objectname)
        bpy.context.space_data.overlay.show_relationship_lines = True

    # Manually add undo here
    bpy.ops.ed.undo_push()
    print("undo thing done")




            
            
            
##### Functions for rolling cube in annihilate_setup ####

def create_empty(location):
    bpy.ops.object.empty_add(radius=0)
    empty = bpy.context.active_object
    empty.location = location

    
    return empty

def parenting(childOBJ,parentOBJ, keep_transform):
    '''parents the child to the parent and keeps tranformation'''
    childOBJ.parent = parentOBJ
    if keep_transform:
        childOBJ.matrix_parent_inverse = parentOBJ.matrix_world.inverted()

def make_cube_roll():
    bpy.context.space_data.overlay.show_relationship_lines = False  ###Once the empties are removed, can reshow

    cube =  bpy.context.active_object
    #add_material(cube)

    #Starting Gulp animation
    cube.location.x = 1
    cube.location.y = 1
    cube.location.z = 1
    cube.keyframe_insert("location",frame = 1)
    cube.keyframe_insert("location",frame = 27)
    cube.location.z = 3
    cube.keyframe_insert("location",frame = 34)
    cube.rotation_euler.z = 0
    cube.keyframe_insert("rotation_euler",frame = 37)
    cube.rotation_euler.z = radians(-25)
    cube.keyframe_insert("rotation_euler",frame = 44)
    cube.keyframe_insert("rotation_euler",frame = 59)
    cube.rotation_euler.z = radians(25)
    cube.keyframe_insert("rotation_euler",frame = 70)
    cube.keyframe_insert("rotation_euler",frame = 81)
    cube.keyframe_insert("location",frame = 83)
    cube.location.z = 1
    cube.rotation_euler.z = 0
    cube.keyframe_insert("rotation_euler",frame = 85)
    cube.keyframe_insert("location",frame = 85)
    

    # list of locations for empties
    empty_locations = [        
            (-1,1,-1),
            (-1,1,1),
            (-1,-1, 1),
            (-1, -1, -1),
    ]

    previous_empty = None

    #variables for the animations
    rotation_animation_length = 5
    current_frame = 85   #delay start until this frame
    rotation_angle = -90
    total_revolutions = 7
    #end_delay = 0

    #bpy.context.scene.frame_end = total_revolutions * 4 * rotation_animation_length + end_delay

    for _ in range(total_revolutions):

        for loc in empty_locations:
            
            empty = create_empty(loc)

            if previous_empty:
                parenting(empty,previous_empty, keep_transform = True)

            else:
                empty_original = empty

            previous_empty = empty
            
            #animate the rotation
            #insert first keyframe
            empty.keyframe_insert("rotation_euler",frame=current_frame)
            
            current_frame += rotation_animation_length
            empty.rotation_euler.x = math.radians(rotation_angle)
            empty.keyframe_insert("rotation_euler",frame=current_frame)

            #reset the rotation_euler to zero so doesn't mess up parenting
            empty.rotation_euler.x = 0    

    cube.location.x = 1
    cube.location.y = 1
    cube.location.z = 1
    #parent cube to the last empty
    #cube.parent = empty
    parenting(cube,empty,keep_transform = True)
    




#### Functions for 3 different set-ups ####         

def basic_daily_setup():
        #make scene 100 frames
        bpy.context.scene.frame_end = 100

        #make default cube active object
        selectOBJ("Cube")

        #duplicate cube to use for displacement and explosion starting on frame 24
        bpy.ops.object.duplicate()
        bpy.context.active_object.name = "DupeCube"

        #modify dupCube subdiv, displace & apply
        bpy.ops.object.modifier_add(type='SUBSURF')
        bpy.context.object.modifiers["Subdivision"].levels = 3
        bpy.context.object.modifiers["Subdivision"].subdivision_type = 'SIMPLE'

        bpy.data.textures.new("babySplodeTexture",'DISTORTED_NOISE')
        bpy.data.textures["babySplodeTexture"].distortion = 5
        bpy.data.textures["babySplodeTexture"].noise_scale = 0.79

        bpy.ops.object.modifier_add(type='DISPLACE')
        bpy.context.object.modifiers["Displace"].texture = bpy.data.textures["babySplodeTexture"]
        bpy.context.object.modifiers["Displace"].strength = 0.4

        bpy.context.object.modifiers["Displace"].mid_level = 1.0

        #DupeCube modifiers quick explode, adjust particle settings
        bpy.ops.object.quick_explode()
        bpy.context.object.modifiers["Explode"].use_edge_cut = False

        bpy.data.particles["ParticleSettings"].name = "babySplodeParticles"
        bpy.data.particles["babySplodeParticles"].frame_start = 24
        bpy.data.particles["babySplodeParticles"].frame_end = 24
        bpy.data.particles["babySplodeParticles"].normal_factor = 100
        bpy.data.particles["babySplodeParticles"].use_rotations = True
        bpy.data.particles["babySplodeParticles"].use_dynamic_rotation = True
        bpy.data.particles["babySplodeParticles"].effector_weights.gravity = 0

        # keyframe 24 so that default cube to disappear dupCube appears
        OBJ=bpy.data.objects["Cube"]
        bpy.context.view_layer.objects.active = OBJ
        OBJ.select_set(True)
        OBJ.hide_viewport = False
        OBJ.keyframe_insert("hide_viewport", frame=23)
        OBJ.hide_viewport = True
        OBJ.keyframe_insert("hide_viewport", frame=24)

        OBJ2=bpy.data.objects["DupeCube"]
        bpy.context.view_layer.objects.active = OBJ2
        OBJ2.select_set(True)
        OBJ2.hide_viewport = True
        OBJ2.keyframe_insert("hide_viewport", frame=23)
        OBJ2.hide_viewport = False
        OBJ2.keyframe_insert("hide_viewport", frame=24)

        bpy.ops.screen.frame_jump(end=False)

def more_massive_setup():
        #make scene 100 frames
        bpy.context.scene.frame_end = 150

        #make default cube active object
        selectOBJ("Cube")

        #duplicate cube to use for displacement and explosion starting on frame 24
        bpy.ops.object.duplicate()
        bpy.context.active_object.name = "DupeCube"

        #modify dupCube subdiv, displace & apply
        bpy.ops.object.modifier_add(type='SUBSURF')
        bpy.context.object.modifiers["Subdivision"].levels = 2
        bpy.context.object.modifiers["Subdivision"].subdivision_type = 'SIMPLE'

        bpy.data.textures.new("babySplodeTexture",'DISTORTED_NOISE')
        bpy.data.textures["babySplodeTexture"].distortion = 5
        bpy.data.textures["babySplodeTexture"].noise_scale = 0.79

        bpy.ops.object.modifier_add(type='DISPLACE')
        bpy.context.object.modifiers["Displace"].texture = bpy.data.textures["babySplodeTexture"]
        bpy.context.object.modifiers["Displace"].strength = 0.6

        bpy.context.object.modifiers["Displace"].mid_level = .8

        #DupeCube modifiers quick explode, adjust particle settings
        bpy.ops.object.quick_explode()
        bpy.context.object.modifiers["Explode"].use_edge_cut = False

        bpy.data.particles["ParticleSettings"].name = "babySplodeParticles"
        bpy.data.particles["babySplodeParticles"].frame_start = 64
        bpy.data.particles["babySplodeParticles"].frame_end = 64
        bpy.data.particles["babySplodeParticles"].normal_factor = 100
        bpy.data.particles["babySplodeParticles"].use_rotations = True
        bpy.data.particles["babySplodeParticles"].use_dynamic_rotation = True
        bpy.data.particles["babySplodeParticles"].effector_weights.gravity = 0


        #make the cube tremble
        OBJ=bpy.data.objects["Cube"]
        bpy.context.view_layer.objects.active = OBJ
        OBJ.select_set(True)
        OBJ.keyframe_insert("location", frame=1)
        
        action = OBJ.animation_data.action
        for fcu in action.fcurves:
            if fcu.data_path == "location":
                mod = fcu.modifiers.new("NOISE")
                mod.use_restricted_range = True
                mod.frame_start = 24
                mod.frame_end = 58
                mod.scale = .2
                mod.strength = .2
                mod.depth = 100
                rand_num = random.choice(range(1,10))
                mod.phase = rand_num
        
        
        # keyframe 64 so that default cube to disappear dupCube appears        
        OBJ.hide_viewport = False
        OBJ.keyframe_insert("hide_viewport", frame=63)
        OBJ.hide_viewport = True
        OBJ.keyframe_insert("hide_viewport", frame=64)

        OBJ2=bpy.data.objects["DupeCube"]
        bpy.context.view_layer.objects.active = OBJ2
        OBJ2.select_set(True)
        OBJ2.hide_viewport = True
        OBJ2.keyframe_insert("hide_viewport", frame=63)
        OBJ2.hide_viewport = False
        OBJ2.keyframe_insert("hide_viewport", frame=64)

        bpy.ops.screen.frame_jump(end=False)

def annihilate_setup():
        #make scene 100 frames
        bpy.context.scene.frame_end = 300

        #make default cube active object
        selectOBJ("Cube")
        
#        #wait until frame 10
#        bpy.context.object.keyframe_insert("location", frame=1)
#        bpy.context.object.keyframe_insert("location", frame=10)
#        bpy.context.scene.frame_current = 10

        #make it start running
        make_cube_roll()

        #make default cube active object
        selectOBJ("Cube")

        #duplicate cube to use for displacement and explosion starting on frame 236
        bpy.ops.object.duplicate()
        bpy.context.active_object.name = "DupeCube"

        #modify dupCube subdiv, displace & apply
        bpy.ops.object.modifier_add(type='SUBSURF')
        bpy.context.object.modifiers["Subdivision"].levels = 3
        bpy.context.object.modifiers["Subdivision"].subdivision_type = 'SIMPLE'

        bpy.data.textures.new("babySplodeTexture",'DISTORTED_NOISE')
        bpy.data.textures["babySplodeTexture"].distortion = 5
        bpy.data.textures["babySplodeTexture"].noise_scale = 0.79

        bpy.ops.object.modifier_add(type='DISPLACE')
        bpy.context.object.modifiers["Displace"].texture = bpy.data.textures["babySplodeTexture"]
        bpy.context.object.modifiers["Displace"].strength = 0.4

        bpy.context.object.modifiers["Displace"].mid_level = 1.0

        #DupeCube modifiers quick explode, adjust particle settings
        bpy.ops.object.quick_explode()
        bpy.context.object.modifiers["Explode"].use_edge_cut = False

        bpy.data.particles["ParticleSettings"].name = "babySplodeParticles"
        bpy.data.particles["babySplodeParticles"].frame_start = 236
        bpy.data.particles["babySplodeParticles"].frame_end = 236
        bpy.data.particles["babySplodeParticles"].normal_factor = 100
        bpy.data.particles["babySplodeParticles"].use_rotations = True
        bpy.data.particles["babySplodeParticles"].use_dynamic_rotation = True
        bpy.data.particles["babySplodeParticles"].effector_weights.gravity = 0

        # keyframe 219 so that default cube to disappear dupCube appears
        OBJ=bpy.data.objects["Cube"]
        bpy.context.view_layer.objects.active = OBJ
        OBJ.select_set(True)
        OBJ.hide_viewport = False
        OBJ.keyframe_insert("hide_viewport", frame=235)
        OBJ.hide_viewport = True
        OBJ.keyframe_insert("hide_viewport", frame=236)

        OBJ2=bpy.data.objects["DupeCube"]
        bpy.context.view_layer.objects.active = OBJ2
        OBJ2.select_set(True)
        OBJ2.hide_viewport = True
        OBJ2.keyframe_insert("hide_viewport", frame=235)
        OBJ2.hide_viewport = False
        OBJ2.keyframe_insert("hide_viewport", frame=236)

        bpy.ops.screen.frame_jump(end=False)


class OBJECT_OT_cube_remove_detritus_operator(bpy.types.Operator):
    """cleans up after explosion"""
    bl_idname = "object.cube_remove_detritus_operator"
    bl_label = "cleans up after explosion"
    #bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):

        remove_detritus()

        return {'FINISHED'}
    

class OBJECT_OT_cube_setup_operator(bpy.types.Operator):
    """sets up the default cube to be explodable"""
    bl_idname = "object.cube_setup_operator"
    bl_label = "Setup object for explosion"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):

        if bpy.context.scene.obj_type == '0':
            basic_daily_setup()
    
        if bpy.context.scene.obj_type == '1':
            more_massive_setup()

        if bpy.context.scene.obj_type == '2':
            annihilate_setup()

        return {'FINISHED'}
    

class OBJECT_OT_cube_exploder_operator(bpy.types.Operator):
    "click to explode this bad boy"
    bl_idname = "object.cube_exploder_operator"
    bl_label = "Ka-boom"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        
        bpy.ops.object.cube_setup_operator()
        bpy.ops.object.load_sounds_operator()
        bpy.ops.screen.frame_jump(end=False)
        bpy.ops.screen.animation_play()

        return {'FINISHED'}
