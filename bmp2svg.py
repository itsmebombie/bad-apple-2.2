import os
import subprocess
import cv2

bmp_directory = './bad'
svg_directory = './svg_bad'

if not os.path.exists(svg_directory):
    os.makedirs(svg_directory)

for filename in os.listdir(bmp_directory):
    if filename.endswith(".bmp"):
        bmp_file = os.path.join(bmp_directory, filename)
        image = cv2.imread(bmp_file)
        inverted_image = 255 - image
        cv2.imwrite(bmp_file, inverted_image)
        svg_file = os.path.join(svg_directory, os.path.splitext(filename)[0].replace("$filename", "") + ".svg")

        command = ["C:/Users/d/Downloads/potrace/potrace.exe", bmp_file, "-o", svg_file, "-b", "svg"]
        subprocess.run(command)

print("Conversion complete.")
