from visualization import *
import utils

# Variables
frame_id = 4

# Initialization
location = 'C:\Users\\bowen\Desktop\\abaqus_python\\realer\\read_odb'
odb_name = location + '\customized_model_425_BachMesh_IMP2_new_version.odb'
odb = openOdb(path=odb_name, readOnly=True)
odb_assembly = odb.rootAssembly
odb_instance = odb_assembly.instances.keys()[0]
frames = odb.steps.values()[0].frames  # len == number of increments
frame = frames[frame_id]

# Element-based
element_info_all = odb_assembly.instances[odb_instance].elements
elemStress = frame.fieldOutputs['S']
elements = utils.element_output(elemStress, element_info_all)

# Output files
with open(location + '\elements_inc' + str(frame_id) + '.csv', 'w') as f:
    f.write('Element_ID,connectivity,mises,S11,S22,S33,S12\n')
    for elementLabel, component in elements.items():
        f.write('%s,%s,%f,%f,%f,%f,%f\n' % (elementLabel, component[0], component[1], component[2], component[3], component[4], component[5]))
