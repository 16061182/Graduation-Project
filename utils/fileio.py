import csv
import numpy as np
from sklearn.utils import shuffle
from math import ceil

def prepare_data(Ldata, Rdata, max_width = 319):
    LX_bias = 0 - Ldata[0][0][0]
    LY_bias = 0 - Ldata[0][0][1]
    RX_bias = 0 - (max_width - Rdata[0][0][0])
    RY_bias = 0 - Rdata[0][0][1]

    # print(LX_bias, LY_bias, RX_bias, RY_bias)

    Lresult, Rresult = [], []
    for i in range(21):
        Lresult.append([Ldata[0][i][0] + LX_bias, Ldata[0][i][1] + LY_bias])
        Rresult.append([max_width - Rdata[0][i][0] + RX_bias, Rdata[0][i][1] + RY_bias])
    return Lresult, Rresult

def generate_csv(data, path):
    with open(path, 'a', newline='') as fid:
        print('start writing csv ' + path)
        for hand in data:
            list_entry = [entry for keypoint in hand for entry in keypoint]

            csv_writer = csv.writer(fid)
            csv_writer.writerow(list_entry)

def read_data_files(data_files, limit_data_count):
    # Ensure that file paths are present in a list.
    # Will be labeled as per entry in list
    # limit_data_count: Upper limit of how many entries are allowed for each type.
    X_data, y_data = None, None
    for label_index, data_file in enumerate(data_files):
        data = np.genfromtxt(data_file, delimiter = ',')
        data = data[:limit_data_count, :]
        labels = [label_index] * data.shape[0]
        if X_data is None:
            X_data = data
            y_data = labels
        else:
            X_data = np.append(X_data, data, axis = 0)
            y_data.extend(labels)

    return X_data, y_data

def split_data(X_data, y_data, split_ratio):
    X_data, y_data = shuffle(X_data, y_data)
    split_at = int(ceil(len(y_data) * split_ratio))
    X_train, y_train = X_data[:split_at, :], y_data[:split_at]
    X_test, y_test = X_data[split_at:, :], y_data[split_at:]
    return (X_train, y_train), (X_test, y_test)