"""Load COVID-19 Radiography Database dataset"""

import os
import glob
from src.datasets import covid_idx, normal_idx, pneumonia_idx


def create_data(dir_path):
    img_list = glob.glob(os.path.sep.join([dir_path, '/*']))
    return img_list, len(img_list)


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
    print(f"Loaded {size} images for NORMAL from COVID-19 Radiography Database dataset")
    x.extend(data)
    y.extend([normal_idx for _ in range(size)])

    # store covid paths
    covid_dir = os.path.sep.join([covid_dataset_path, "COVID-19"])
    data, size = create_data(covid_dir)
    print(f"Loaded {size} images for COVID-19 from COVID-19 Radiography Database dataset")
    x.extend(data)
    y.extend([covid_idx for _ in range(size)])

    # store viral pneumonia paths
    viral_pneumonia_dir = os.path.sep.join(
        [covid_dataset_path, "Viral Pneumonia"])
    data, size = create_data(viral_pneumonia_dir)
    print(f"Loaded {size} images for Viral Pneumonia from COVID-19 Radiography Database dataset")
    x.extend(data)
    y.extend([pneumonia_idx for _ in range(size)])

    return x, y
