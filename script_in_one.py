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
# element_info_all = odb_assembly.instances[odb_instance].elements
# elemStress = frame.fieldOutputs['S']
# elements = utils.element_output(elemStress, element_info_all)
#
# # Output files
# with open(location + '\elements_inc' + str(frame_id) + '.csv', 'w') as f:
#     f.write('Element_ID,connectivity,mises,S11,S22,S33,S12\n')
#     for elementLabel, component in elements.items():
#         f.write('%s,%s,%f,%f,%f,%f,%f\n' % (elementLabel, component[0], component[1], component[2], component[3], component[4], component[5]))

# Node-based
node_info_all = odb_assembly.instances[odb_instance].nodes
nodes_coordinates_init = utils.node_coor_init(node_info_all)
# print('\n\n')
# print(nodes_coordinates_init[80001424])

elemDisp = frame.fieldOutputs['U']
nodelDisp = utils.nodal_disp(elemDisp)
# print('\n\n')
# print(nodelDisp[80001424])


nodes_coordinates_current = utils.node_coor_current(nodes_coordinates_init, nodelDisp)
# print('\n\n')
# print(nodes_coordinates_current[80000481])

elemStress = frame.fieldOutputs['S']
# odb_set_whole = odb_assembly.elementSets[' ALL ELEMENTS']
# field = elemStress.getSubset(region=odb_set_whole, position=ELEMENT_NODAL)
field = elemStress.getSubset(position=ELEMENT_NODAL)
stresses = utils.nodal_stresses(field, 1000000)
print('\n\n')
print(80000512, stresses[80000512])

# Output files
with open(location + '\\nodes_coor_inc' + str(frame_id) + '.csv', 'w') as f:
    f.write('Node_ID,Node_Coordinates)\n')
    for nodeLabel, component in nodes_coordinates_current.items():
        f.write('%s,%s\n' % (nodeLabel, component))

with open(location + '\\nodes_stress_inc' + str(frame_id) + '.csv', 'w') as f:
    f.write('Node_ID,Contour(Corner/S-Stress_components)\n')
    for nodeLabel, component in stresses.items():
        f.write('%s,%s\n' % (nodeLabel, component))

# Combine
nodes_all = utils.nodal_all(nodes_coordinates_current, stresses)
with open(location + '\\nodes_inc' + str(frame_id) + '.csv', 'w') as f:
    f.write('Element_ID,Node_Coordinates,Contour(Corner/S-Stress_components)\n')
    for nodeLabel, component in nodes_all.items():
        if len(component) > 1:
            f.write('%s,%s,%s\n' % (nodeLabel, component[0], component[1]))
