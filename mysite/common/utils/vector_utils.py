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
    row_vector_set = convert_vector_set_to_row_vector_set(vector_set)
    dimension = len(row_vector_set)
    mass = None
    deg_1_set = []
    for nth_deg in range(0, degree + 1):
        group_set = generate_group_set_by_dim_and_deg(dimension, nth_deg)
        for group in group_set:
            label = prefix
            moment = None
            for index in range(dimension):
                label += str(group[index])
                tmp = row_vector_set[index]**group[index]
                moment = moment*tmp if moment is not None else tmp
            spatial_moments[label] = np.sum(moment)
            if nth_deg == 0:
                mass = np.sum(moment)
            elif nth_deg == 1:
                deg_1_set.append(np.sum(moment)/mass)
    prefix = 'mu'
    prefix_n = 'nu'
    for nth_deg in range(2, degree + 1):
        group_set = generate_group_set_by_dim_and_deg(dimension, nth_deg)
        for group in group_set:
            label = prefix
            label_n = prefix_n
            moment = None
            moment_n = None
            for index in range(dimension):
                label += str(group[index])
                label_n += str(group[index])
                tmp = (row_vector_set[index] - np.array([deg_1_set[index]/mass]*len(vector_set)))**group[index]
                tmp_n = (row_vector_set[index] - np.array([deg_1_set[index]/(mass**(nth_deg/dimension + 1))]*len(vector_set)))**group[index]
                moment = moment*tmp if moment is not None else tmp
                moment_n = moment_n*tmp_n if moment_n is not None else tmp_n
            spatial_moments[label] = np.sum(moment)
            spatial_moments[label_n] = np.sum(moment_n)
    
    if with_label:
        return spatial_moments
    else:
        return list(spatial_moments.values())

__all__ = [
    'convert_vector_set_to_row_vector_set', 'generate_group_set_by_dim_and_deg', 'n_spatial_moments'
]