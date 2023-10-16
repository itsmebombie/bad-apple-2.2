import json
import os

# Create a directory path for your OBJ files
obj_directory = 'obj_bad'

# Get a list of all OBJ files in the directory
obj_files = [f for f in os.listdir(obj_directory) if f.endswith('.obj')]
mv = 0
mf = 0
output = []
for obj_file in obj_files:
    vertices = []
    faces = []
    
    with open(os.path.join(obj_directory, obj_file), 'r') as file:
        lines = file.read().splitlines()

    for line in lines:
        if line.startswith('v '):
            vertex_data = line.split()[1:]
            x, _, z = [float(x) for x in vertex_data]
            vertices.append([x, z])
        elif line.startswith('f '):
            face_data = line.split()[1:]
            face = [int(vertex.split('/')[0]) for vertex in face_data]
            faces.append(face)

    mv = max(mv, len(vertices))
    mf = max(mf, len(faces))

    filename = os.path.splitext(obj_file)[0]
    int_filename = int(filename)
    output_filename = filename + '.json'

    if int_filename % 6 == 0:
        print("adding", filename)

    if int_filename >= len(output):
        output += [0] * (int_filename - len(output) + 1)
    
    output[int(filename)] = {"vertices": vertices, "faces": faces}

print(mf, mv)

print("dumping json")
with open("out.json", 'w') as f:
    f.write(str(output).replace(" ", "").replace("'", '"'))

