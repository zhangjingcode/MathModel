import os

import numpy as np
import pandas as pd
import h5py
import random


ENGINEERING_LIST = ['Cell Index', 'Cell X', 'Cell Y', 'Height', 'Azimuth', 'Electrical Downtilt',
                    'Mechanical Downtilt', 'Frequency Band', 'RS Power']

MAP_LIST = ['Cell Altitude', 'Cell Building Height', 'Cell Clutter Index',
            'X', 'Y', 'Altitude', 'Building Height', 'Clutter Index']

LABEL = ['RSRP']


def LoadCSV(csv_path):
    with open(csv_path, 'r') as f:
        csv_pd = pd.read_csv(f, index_col=0, header=0)
        # print(csv_pd)
        return csv_pd


def DataCombination(combinated_array, csv_path):
    with open(csv_path, 'r') as f:
        csv_pd = pd.read_csv(f, index_col=None, header=0)
        array = csv_pd.get_values()
        array = np.asarray(array, dtype=np.float32)

    if combinated_array == []:
        combinated_array = array

    else:
        combinated_array = np.concatenate([combinated_array, array], axis=0)

    return combinated_array


def SaveH5(saved_array, store_h5_folder):
    with h5py.File(os.path.join(store_h5_folder, 'CombinedData.h5'), 'w') as f:
        # f['list'] = ENGINEERING_LIST+MAP_LIST+LABEL
        f['array'] = saved_array


def Iteration(case_path_list, store_h5_folder):
    csv_num = 0
    combinated_array = []
    for csv_path in case_path_list:
        csv_num += 1
        print(csv_num)
        combinated_array = DataCombination(combinated_array, csv_path)

    SaveH5(combinated_array, store_h5_folder)

    # return combinated_array


def DataDivited(case_folder, store_folder, train_ratio=0.7, validation_ratio=0.1, test_ratio=0.2):
    csv_list = os.listdir(case_folder)
    case_num = len(csv_list)
    random.shuffle(csv_list)


    train_index_list = csv_list[:round(case_num * train_ratio)]
    print(round(case_num * train_ratio), round(case_num * validation_ratio))

    validation_index_list = csv_list[round(case_num * train_ratio):
                                       round(case_num * train_ratio) + round(case_num * validation_ratio)]

    test_index_list = csv_list[round(case_num * train_ratio) + round(case_num * validation_ratio):]

    data_set_dict = {'Train': train_index_list, 'Validation': validation_index_list, 'Test': test_index_list}
    for data_set_index in ['Train', 'Validation', 'Test']:
        sub_store_folder = os.path.join(store_folder, data_set_index)
        if not os.path.exists(sub_store_folder):
            os.mkdir(sub_store_folder)
        csv_path_list = [os.path.join(case_folder, index) for index in data_set_dict[data_set_index]]

        Iteration(csv_path_list, sub_store_folder)






def LoadH5(h5_path):
    with h5py.File(os.path.join(h5_path, 'CombinedData.h5'), 'r') as f:
        # f['list'] = ENGINEERING_LIST+MAP_LIST+LABEL
        combinated_array = np.array(f['array'])
        return combinated_array

# def SaveImageh5(csv_path):

def main():
    # Iteration(r'C:\Users\zj\Desktop\word_and_ppt\建模2019\A题\train_set',
    #           r'C:\Users\zj\Desktop\word_and_ppt\建模2019\A题\ProcessedData')

    # CheckH5(r'C:\Users\zj\Desktop\word_and_ppt\建模2019\A题\ProcessedData')
    DataDivited(r'E:\建模2019\train_set', r'E:\建模2019\Divited_set')
if __name__ == '__main__':
    main()
