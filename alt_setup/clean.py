import os
import shutil

os.remove("reskit.vpp")
os.remove(".gitattributes")
os.remove("reskit/utilities/requirements.txt")

del_folders = []
del_files = []

for dirpath, dirnames, filenames in os.walk("."):
    del_files.extend([dirpath+os.sep+filename for filename in filenames if ".pyc" in filename])
    del_folders.extend([dirpath+os.sep+dirname for dirname in dirnames if ("tests" in dirname or "-info" in dirname)])

for filename in del_files:
    os.remove(filename)

for dirname in del_folders:
    shutil.rmtree(dirname)

shutil.rmtree("reskit/doc")
try:
    shutil.rmtree(".git")
except:
    pass
try:
    shutil.rmtree("alt_setup")
except:
    pass
