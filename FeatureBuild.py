import os
import math

import pandas as pd
import numpy as np
import copy
from Ubility.ReadAndSave import LoadH5, LoadCSV



ENGINEERING_LIST = ['Cell Index','Cell X','Cell Y','Height','Azimuth','Electrical Downtilt',
                    'Mechanical Downtilt','Frequency Band','RS Power']

MAP_LIST = ['Cell Altitude','Cell Building Height','Cell Clutter Index','X','Y','Altitude','Building Height','Clutter Index']

LABEL = ['RSRP']


min_Cell_X = 384180.0
max_Cell_X = 434540.0
min_Cell_Y = 3376325.0
max_Cell_Y = 3417960.0

min_X = 382930
max_X = 434580
min_Y = 3375740
max_Y = 3418880


h5_columns_list = ENGINEERING_LIST + MAP_LIST + LABEL


def IterationSigleCase(case_folder):

    MAP_INDEX_LIST = ['Cell X', 'Cell Y', 'X', 'Y']
    map_dict = {}
    for map_index in MAP_INDEX_LIST:
        map_dict['min' + map_index] = []
        map_dict['max' + map_index] = []
    csv_num = 0
    for csv_index in os.listdir(case_folder):
        csv_num += 1
        print(csv_num)
        csv_path = os.path.join(case_folder, csv_index)
        pd = LoadCSV(csv_path)
        for map_index in MAP_INDEX_LIST:
            map_dict['min' + map_index].append(min(pd[map_index]))
            map_dict['max' + map_index].append(max(pd[map_index]))

    for map_index in MAP_INDEX_LIST:
        print('min ' + map_index + ': ', min(map_dict['min' + map_index]))
        print('max ' + map_index + ': ', max(map_dict['max' + map_index]))


def FeatureEngineering(feature_pd):

    h5_columns_list = feature_pd.columns.tolist()
    build_feature_list = ['Relative Distance', 'Relative Altitude']
    build_feature_dict = {}
    for index in build_feature_list:
        build_feature_dict[index] = []

    for index in feature_pd.index.tolist():

        ###Distance
        distance_l_feature = math.sqrt(math.pow(feature_pd.iloc[index, h5_columns_list.index('X')] -
                                                feature_pd.iloc[index, h5_columns_list.index('Cell X')], 2) + \
                                       math.pow(feature_pd.iloc[index, h5_columns_list.index('Y')] -
                                                feature_pd.iloc[index, h5_columns_list.index('Cell Y')], 2))

        build_feature_dict['Relative Distance'].append(math.sqrt(distance_l_feature))


        ####Hight
        hight_feature = feature_pd.iloc[index, h5_columns_list.index('Height')] + \
                        feature_pd.iloc[index, h5_columns_list.index('Cell Altitude')] \
                        -feature_pd.iloc[index, h5_columns_list.index('Altitude')]

        build_feature_dict['Relative Altitude'].append(hight_feature)





    return build_feature_dict





def PdGeneartion(h5_path):


    h5_array = LoadH5(h5_path)
    feature_pd = pd.DataFrame(data=h5_array, index=None, columns=h5_columns_list)
    print(FeatureEngineering(feature_pd))


    # plt.hist(target_list)
    # plt.show()


def main():
    h5_path = r'E:\建模2019'
    PdGeneartion(h5_path)


if __name__ == '__main__':
    main()




