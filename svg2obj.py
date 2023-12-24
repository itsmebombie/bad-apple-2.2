# memory leaking or sth, slow af

import bpy
import os
import sys

directory = './svg_bad'
output_directory = './obj_bad'

# (from_frame, to_frame, trigs_per_frame)
ranges = [
    (0, 150, 60), (350, 440, 60), (440, 465, 80),
    (465, 655, 105), (655, 755, 115), (755, 790, 100),
    (800, 817, 50), (817, 823, 80), (823, 850, 55),
    (850, 1080, 75), (1080, 1227, 100), (1227, 1262, 45),
    (1262, 1300, 70), (1300, 1330, 35), (1330, 1350, 55),
    (1350, 1478, 90), (1478, 1505, 25), (1505, 1590, 170),
    (1590, 1725, 250), (1725, 1883, 140), (1883, 1911, 450),
    (1911, 2330, 80), (2330, 2354, 25), (2354, 2470, 100),
    (2470, 2508, 120), (2508, 2535, 35), (2535, 2625, 75),
    (2625, 2737, 130), (2737, 2780, 40), (2780, 2825, 110),
    (2825, 2925, 150), (2925, 2950, 60), (2950, 2965, 50),
    (2965, 3135, 85), (3135, 3155, 50), (3155, 3220, 85),
    (3220, 3290, 65), (3290, 3295, 50), (3295, 3320, 75),
    (3320, 3353, 15), (3353, 3476, 165), (3476, 3575, 110),
    (3575, 3700, 85), (3700, 3775, 75), (3775, 3820, 90),
    (3820, 3840, 80), (3840, 3910, 75), (3910, 3980, 90),
    (3980, 4000, 80), (4000, 4020, 70), (4020, 4187, 85),
    (4187, 4208, 25), (4208, 4250, 55), (4250, 4310, 75),
    (4310, 4405, 95), (4405, 4415, 50), (4415, 4500, 80),
]
default_trigs = 80

bpy.data.objects["Camera"].select_set(True)
bpy.ops.object.delete()
bpy.data.objects["Light"].select_set(True)
bpy.ops.object.delete()

proc = False
for filename in os.listdir(directory):
    if not filename.endswith(".svg"):
        continue

    if proc == False:
        if filename == "610.svg":
            proc = True
        else: continue
    # if len(filename) == len("123.svg"): continue

    num = int(filename.split(".")[0])
    target_trigs = default_trigs
    for i in ranges:
        if num >= i[0] and num < i[1]:
            target_trigs = i[2]
            break
    
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
        bpy.context.object.modifiers["Decimate"].ratio = target_trigs / len(bpy.context.object.data.polygons)

        bpy.ops.export_scene.obj(filepath=os.path.join(output_directory, filename.split(".")[0] + ".obj"), 
                                    use_materials=False, use_normals=False, use_uvs=False)

    for i in bpy.data.objects:
        bpy.data.objects.remove(i, do_unlink=True)
    for obj in bpy.data.objects:
        bpy.data.objects.remove(obj, do_unlink=True)
    for mesh in bpy.data.meshes:
        bpy.data.meshes.remove(mesh, do_unlink=True)
        
