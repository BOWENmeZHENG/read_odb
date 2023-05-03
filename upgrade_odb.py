import os

odb_file_old = 'customized_model_425_BachMesh_IMP2.odb'
odb_file = 'customized_model_425_BachMesh_IMP2_new_version.odb'
os.system(f"abaqus -upgrade -job {odb_file} -odb {odb_file_old}")