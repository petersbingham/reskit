import os
import io
import shutil

new_requirements = []
utilities = []

with io.open("requirements.txt", 'r', newline='\n', encoding="utf-8") as f:
    for l in f:
        if "git" in l:
            utilities.append(l)
        else:
            new_requirements.append(l)

os.remove("requirements.txt")

with io.open("requirements.txt", 'w', newline='\n', encoding="utf-8") as f:
    for l in new_requirements:
        f.write(l)

os.remove("setup.py")
shutil.copyfile("alt_setup/setup.py", "setup.py")

os.mkdir("reskit/utilities")
with io.open("reskit/utilities/requirements.txt", 'w', newline='\n', encoding="utf-8") as f:
    for l in utilities:
        f.write(l)

shutil.copyfile("alt_setup/file_struct.txt", "file_struct.txt")
