
import csv



def read_data(path):
    data = []
    with open(path, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for line in reader:
            data.append(line)
        while [] in data:
            data.remove([])
    return data


def read_scheme(path):
    with open(path, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        attributes = next(reader)
        value_type = next(reader)
    return attributes, value_type



def str2numerical(data, value_type):
    size = len(data)
    columns = len(data[0])
    for i in range(size):
        for j in range(columns-1):
            if value_type[j] == 'numerical' and data[i][j] != '?':
                data[i][j] = float(data[i][j])
    return data



def read(data_path, scheme_path):
    data = read_data(data_path)
    attributes, value_type = read_scheme(scheme_path)
    data = str2numerical(data, value_type)
    return data, attributes, value_type


