"""Load COVID-19 Radiography Database dataset"""

import os
import glob

def create_data(dir_path):
    data = []
    img_list = glob.glob(os.path.sep.join([dir_path, '/*']))
    for img in img_list:
        data.append(img)
    return data, len(data)

def load_covid19_radiography_database(data_dir):
    """
    Load COVID-19 Radiography Database dataset.

    Returns (x, y): as dataset x and y containing paths.

    """

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    covid_dataset_path = os.path.sep.join([data_dir, ""])

    # variables to store output paths
    x, y = [], []


    # store normal paths
    normal_dir = os.path.sep.join([covid_dataset_path, "NORMAL"])
    data, size = create_data(normal_dir)
    x.extend(data)
    y.extend([0 for _ in range(size)])

    # store covid paths
    covid_dir = os.path.sep.join([covid_dataset_path, "COVID19"])
    data, size = create_data(normal_dir)
    x.extend(data)
    y.extend([1 for _ in range(size)])
    
    # store viral pneumonia paths
    viral_pneumonia_dir = os.path.sep.join([covid_dataset_path, "Viral Pneumonia"])
    data, size = create_data(normal_dir)
    x.extend(data)
    y.extend([2 for _ in range(size)])

    return x, y
