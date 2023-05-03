import glob
import os
import shutil

import write_script

os.makedirs('results', exist_ok=True)
for i in range(1, 29):
    filename = write_script.write_pymodel(inc=i)
    os.system(f"abaqus cae noGUI={filename}")
for f in glob.glob("abaqus.rp*"):
    os.remove(f)
for f in glob.glob("pyscript*"):
    os.remove(f)
files = os.listdir('./')
for file in files:
    if file.endswith('.csv'):
        shutil.move(file, f'results/{file}')