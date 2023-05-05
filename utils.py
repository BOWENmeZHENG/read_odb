def element_stresses(elemStress, stress_id):
    elementStesses = {}
    for value in elemStress.values:
        if value.elementLabel in elementStesses:
            elementStesses[value.elementLabel].append(value.data[stress_id])
        else:
            elementStesses.update({value.elementLabel: [value.data[stress_id]]})
    for key in elementStesses:
        elementStesses.update({key: sum(elementStesses[key]) / len(elementStesses[key])})
    return elementStesses


def element_mises(elemStress):
    elementMises = {}
    for value in elemStress.values:
        elementMises[value.elementLabel] = value.mises
    return elementMises


def connectivity(elementS, element_info_all):
    indices = elementS.keys()
    indices_whole_model = {}
    for element in element_info_all:
        indices_whole_model[element.label] = element.connectivity
    element_connectivity = {}
    for index in indices:
        element_connectivity[index] = indices_whole_model[index]
    return element_connectivity


def element_output(elemStress, element_info_all):
    elementS11 = element_stresses(elemStress, 0)
    elementS22 = element_stresses(elemStress, 1)
    elementS33 = element_stresses(elemStress, 2)
    elementS12 = element_stresses(elemStress, 3)
    elementMises = element_mises(elemStress)
    element_connectivity = connectivity(elementS11, element_info_all)
    element_all = [element_connectivity, elementMises, elementS11, elementS22, elementS33, elementS12]

    elements = elementS11.copy()
    for key in elements:
        elements[key] = []
    for element_set in element_all:
        for key, value in element_set.items():
            elements[key].append(value)
    return elements


def node_coor_init(node_info_all):
    # indices = elementS.keys()
    nodes_coordinates_init = {}
    for node in node_info_all:
        nodes_coordinates_init[node.label] = node.coordinates
    return nodes_coordinates_init


def nodal_disp(elemDisp):
    nodelDisp = {}
    for value in elemDisp.values:
        nodelDisp[value.nodeLabel] = value.data
    return nodelDisp


def node_coor_current(nodes_coordinates_init, nodelDisp):
    nodes_coordinates_current = {}
    for key in nodelDisp.keys():
        nodes_coordinates_current[key] = nodes_coordinates_init[key] + nodelDisp[key]
    return nodes_coordinates_current


def nodal_stresses(field, max_iter):
    info_all = field.values
    stresses = {}
    i = 0
    for info in info_all:
        i += 1
        if i > max_iter:
            break
        key = info.nodeLabel
        if key in stresses.keys():
            stresses[key].append((info.elementLabel, info.mises))
        else:
            stresses[key] = [(info.elementLabel, info.mises)]
    return stresses


def nodal_all(nodes_coordinates_current, stresses):
    nodes_all = {}
    for key, value in nodes_coordinates_current.items():
        nodes_all[key] = [value]
    for key, value in stresses.items():
        nodes_all[key].append(value)
        # print(nodes_all[key])
    return nodes_all