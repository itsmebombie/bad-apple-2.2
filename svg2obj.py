# memory leaking or sth, slow af

import bpy
import os
import sys

directory = './svg_bad'
output_directory = './obj_bad'

bpy.data.objects["Camera"].select_set(True)
bpy.ops.object.delete()
bpy.data.objects["Light"].select_set(True)
bpy.ops.object.delete()

# Define a dummy file path
dummy_file = os.devnull  # On most systems, this points to the null device

# Redirect stdout and stderr to the dummy file
original_stdout = sys.stdout
original_stderr = sys.stderr
sys.stdout = open(dummy_file, 'w')
sys.stderr = open(dummy_file, 'w')

proc = False
for filename in os.listdir(directory):
    if not filename.endswith(".svg"):
        continue

    if proc == False:
        if filename == "6170.svg":
            proc = True
        else: continue
    
    
    bpy.ops.import_curve.svg(filepath=os.path.join(directory, filename))

    if len(bpy.context.scene.objects) > 1:
        for obj in bpy.data.objects: # select them
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
        bpy.ops.object.join()
    
    # print(len(bpy.context.scene.objects))

    if len(bpy.context.scene.objects) == 1:
        bpy.data.objects[0].select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects[-1]

        bpy.ops.object.convert(target='MESH')
        bpy.ops.object.modifier_add(type='DECIMATE')
        bpy.context.object.modifiers["Decimate"].ratio = 150 / len(bpy.context.object.data.polygons)

        bpy.ops.export_scene.obj(filepath=os.path.join(output_directory, filename.split(".")[0] + ".obj"), 
                                    use_materials=False, use_normals=False, use_uvs=False)

    for i in bpy.data.objects:
        bpy.data.objects.remove(i)
    for obj in bpy.data.objects:
        bpy.data.objects.remove(obj, do_unlink=True)
    for mesh in bpy.data.meshes:
        bpy.data.meshes.remove(mesh, do_unlink=True)
        
