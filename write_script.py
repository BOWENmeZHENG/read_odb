def write_pymodel(inc, location='C:\\\\Users\\\\bowen\\\\Desktop\\\\abaqus_python\\\\realer\\\\read_odb',
                  odbname='\\\\customized_model_425_BachMesh_IMP2_new_version.odb'):
    filename = f'pyscript_element_inc{inc}.py'
    with open(filename, 'w') as f:
        f.write("from visualization import *\n")
        f.write("import utils\n")
        f.write(f"odb = openOdb(path='{location + odbname}', readOnly=True)\n")
        f.write("odb_assembly = odb.rootAssembly\n")
        f.write("odb_instance = odb_assembly.instances.keys()[0]\n")
        f.write("frames = odb.steps.values()[0].frames\n")
        f.write(f"frame = frames[{inc}]\n")
        f.write("element_info_all = odb_assembly.instances[odb_instance].elements\n")
        f.write("elemStress = frame.fieldOutputs['S']\n")
        f.write("elements = utils.element_output(elemStress, element_info_all)\n")
        f.write(f"with open('{location}' + '\\elements_inc' + str({inc}) + '.csv', 'w') as f:\n")
        f.write("    f.write('Element_ID,connectivity,mises,S11,S22,S33,S12\\n')\n")
        f.write("    for elementLabel, component in elements.items():\n")
        f.write("        f.write('%s,%s,%f,%f,%f,%f,%f\\n' % (elementLabel, component[0], component[1], component[2], component[3], component[4], component[5]))\n")
    return filename