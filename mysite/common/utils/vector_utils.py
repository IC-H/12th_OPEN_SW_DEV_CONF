import numpy as np

def convert_vector_set_to_row_vector_set(vector_set):
    row_vector_set = []
    dimension = len(vector_set[0])
    for row_index in range(dimension):
        row_vector_set.append([])
    for vector in vector_set:
        for row_index in range(dimension):
            row_vector_set[row_index].append(vector[row_index])
    return np.array(row_vector_set)

def generate_group_set_by_dim_and_deg(dim, deg):
    if dim == 1:
        return np.array([[deg]])
    elif dim > 1:
        group_set = []
        for n_deg in range(0, deg + 1):
            header = np.array([n_deg])
            for group in generate_group_set_by_dim_and_deg(dim - 1, deg - n_deg):
                tmp = np.append(header, group)
                group_set.append(tmp)
        return np.array(group_set)

def n_spatial_moments(vector_set, degree, with_label=False):
    spatial_moments = {}
    prefix = 'm'
    prefix_c = 'mu'
    prefix_n = 'nu'
    row_vector_set = convert_vector_set_to_row_vector_set(vector_set)
    dimension = len(row_vector_set)
    mass = None
    deg_1_set = []
    for nth_deg in range(0, degree + 1):
        group_set = generate_group_set_by_dim_and_deg(dimension, nth_deg)
        for group in group_set:
            label = ''
            moment = None
            moment_c = None
            for index in range(dimension):
                label += str(group[index])
                tmp = row_vector_set[index]**group[index]
                moment = moment*tmp if moment is not None else tmp
                if mass is not None and len(deg_1_set) == dimension:
                    tmp_c = (row_vector_set[index] - np.array([deg_1_set[index]/mass]*len(vector_set)))**group[index]
                    moment_c = moment_c*tmp_c if moment_c is not None else tmp_c
            spatial_moments[prefix + label] = np.sum(moment)
            if nth_deg == 0:
                mass = spatial_moments[prefix + label]
            elif nth_deg == 1:
                deg_1_set.append(spatial_moments[prefix + label]/mass)
            elif nth_deg > 1:
                spatial_moments[prefix_c + label] = np.sum(moment_c)
                spatial_moments[prefix_n + label] = spatial_moments[prefix_c + label]/(mass**(nth_deg/dimension + 1))
    
    if with_label:
        return spatial_moments
    else:
        return list(spatial_moments.values())

__all__ = [
    'convert_vector_set_to_row_vector_set', 'generate_group_set_by_dim_and_deg', 'n_spatial_moments'
]