import os

import numpy as np
import matplotlib.pyplot as plt
import cv2

from Ubility.ReadAndSave import LoadCSV, LoadH5

min_Cell_X = 384180.0
max_Cell_X = 434540.0
min_Cell_Y = 3376325.0
max_Cell_Y = 3417960.0

min_X = 382930
max_X = 434580
min_Y = 3375740
max_Y = 3418880

ENGINEERING_LIST = ['Cell Index', 'Cell X', 'Cell Y', 'Height', 'Azimuth', 'Electrical Downtilt',
                    'Mechanical Downtilt', 'Frequency Band', 'RS Power']

MAP_LIST = ['Cell Altitude', 'Cell Building Height', 'Cell Clutter Index',
            'X', 'Y', 'Altitude', 'Building Height', 'Clutter Index']

LABEL = ['RSRP']

h5_index_list = ENGINEERING_LIST+MAP_LIST+LABEL

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

def ShowMap(h5_path, target_index, store_path):


    h5_array = LoadH5(h5_path)

    map_index = ['X', 'Y', target_index]
    map_array_index = [h5_index_list.index(index) for index in map_index]
    sub_h5_array = h5_array[:20000,  map_array_index]
    #
    target_list = list(set(sub_h5_array[:, 2].flatten()))
    mean_target = np.mean(target_list)
    std_target = np.std(target_list)
    min_target = np.min(target_list)
    #
    # plt.hist(target_list)
    # plt.show()


    x_list = []
    y_list = []

    for col in range(sub_h5_array.shape[0]):
        x_list.append(sub_h5_array[col][0])
        y_list.append(sub_h5_array[col][1])

    x_list = list(set(x_list))
    y_list = list(set(y_list))


    map_array = np.zeros((len(x_list), len(y_list)))

    for col in range(sub_h5_array.shape[0]):
        x_coordinate = x_list.index(sub_h5_array[col][0])
        y_coordinate = y_list.index(sub_h5_array[col][1])

        target_value = sub_h5_array[col][2]
        original_target_value = map_array[x_coordinate, y_coordinate]
        if original_target_value != 0 and original_target_value != target_value:
            print('Multi - value', map_array[x_coordinate, y_coordinate], target_value)
        else:
            map_array[x_coordinate, y_coordinate] = target_value

    sub_store_path = os.path.join(store_path, target_index)

    if not os.path.exists(sub_store_path):
        os.mkdir(sub_store_path)

    store_array_path = os.path.join(sub_store_path, target_index+'_all_map.npy')
    np.save(store_array_path, map_array)
    # cv2.imshow('img', map_array)
    # cv2.imwrite(os.path.join(sub_store_path, target_index+'_all_map_cv2.jpg'), map_array, [int(cv2.IMWRITE_JPEG_QUALITY),95])
    # cv2.waitKey(0)

    plt.axis('off')
    plt.title(target_index)
    plt.imshow(map_array, vmin=np.min(target_list)-std_target, vmax=np.max(target_list)+std_target, cmap='tab20c')
    plt.colorbar()

    plt.savefig(os.path.join(sub_store_path, target_index+'_all_map.png'))


    plt.show()


def ShowMapFromH5(h5_path):
    h5_array = LoadH5(h5_path)
    x_index = h5_index_list.index('X')
    y_index = h5_index_list.index('Y')


    print('X arrange from {} to {}'.format(np.min(h5_array[:, x_index]), np.max(h5_array[:, x_index])))
    print('y arrange from {} to {}'.format(np.min(h5_array[:, y_index]), np.max(h5_array[:, y_index])))


def ShowMapFromCsv(csv_path, target_name, store_path):
    csv_pd = LoadCSV(csv_path)

    min_x = min(csv_pd['X'])
    max_x = max(csv_pd['X'])
    min_y = min(csv_pd['Y'])
    max_y = max(csv_pd['Y'])

    Cell_X = min(csv_pd['Cell X'])
    Cell_Y = min(csv_pd['Cell Y'])

    x_list = []
    y_list = []

    for index in range(len(csv_pd.index.tolist())):
        x_coordinate = csv_pd.iloc[index, h5_index_list.index('X') - 1]
        y_coordinate = csv_pd.iloc[index, h5_index_list.index('Y') - 1]
        # target_value = csv_pd.iloc[index, h5_index_list.index(target_name) - 1]
        x_list.append(x_coordinate)
        y_list.append(y_coordinate)

    x_list = list(set(x_list))
    y_list = list(set(y_list))

    map_array = np.zeros((len(x_list), len(y_list)))
    for index in range(len(csv_pd.index.tolist())):
        x_coordinate = x_list.index(csv_pd.iloc[index, h5_index_list.index('X') - 1])
        y_coordinate = y_list.index(csv_pd.iloc[index, h5_index_list.index('Y') - 1])

        map_array[x_coordinate, y_coordinate] = csv_pd.iloc[index, h5_index_list.index(target_name) - 1]


    sub_store_path = os.path.join(store_path, target_name)

    if not os.path.exists(sub_store_path):
        os.mkdir(sub_store_path)

    store_array_path = os.path.join(sub_store_path, target_name+str(min_x)+' to ' + str(max_x) +'_'+
                             str(min_y)+' to ' + str(max_y)+'_single_map.npy')
    np.save(store_array_path, map_array)
    # plt.style.use('ggplot')
    # plt.hist(x_list, normed=0, edgecolor='black', label='X', color='r')
    # plt.hist(y_list, normed=0, edgecolor='black', label='Y', color='b')
    # plt.legend()
    plt.figure(figsize=(6, 8))
    plt.title(target_name+'\n'+str(min_x)+' to ' + str(max_x) + '\n' + str(min_y)+' to ' + str(max_y))
    try:
        plt.scatter(x_list.index(Cell_X), y_list.index(Cell_Y),  color='w', marker='*')

    except:
        pass
    plt.imshow(map_array, vmin=400, vmax=600, cmap='jet')



    plt.colorbar()
    plt.savefig(os.path.join(sub_store_path, target_name+str(min_x)+' to ' + str(max_x) +'_'+
                             str(min_y)+' to ' + str(max_y)+'_single_map.png'))
    # plt.show()
    # return 0




def main():
    # IterationSigleCase(r'C:\Users\zj\Desktop\word_and_ppt\建模2019\A题\train_set')
    # h5_path = r'E:\建模2019'
    # ShowMap(h5_path, 'Clutter Index', r'E:\建模2019\Image\All_map')
    # ShowMapFromH5(h5_path)
    folder_path = r'E:\建模2019\train_set'
    for index in os.listdir(folder_path):
        csv_path = os.path.join(folder_path, index)
    # csv_path = r'E:\建模2019\train_set\train_108401.csv'
        for parameters in ['Altitude']:
            ShowMapFromCsv(csv_path, parameters, r'E:\建模2019\Image\Single_map')
if __name__ == '__main__':
    main()
