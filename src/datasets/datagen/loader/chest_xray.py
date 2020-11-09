"""Load COVID-19 Radiography Database dataset"""

import os
import glob
import pandas as pd
from src.datasets import labels, normal_idx, pneumonia_idx


def store_split(x, y, path, data_dir, mode='w'):
    f = open(path, mode)
    for img, label in zip(x, y):
        img = os.path.relpath(img, data_dir)
        f.write(f"{img} {label}\n")
    f.close()


def store_label_to_split(label, split_dir, split_name, chest_xray_data_dir, **kwargs):
    output_dir = os.path.join(kwargs["splits_dir"], kwargs["split"])
    img_list = glob.glob(os.path.sep.join([split_dir, labels[label], "/*"]))
    y = [label for _ in img_list]
    store_split(img_list, y, os.path.join(
        output_dir, f"{split_name}.txt"), kwargs["data_dir"], "a+")


def load_chest_xray_splits(chest_xray_data_dir, **kwargs):
    """
    Load and append to existing splits
    """

    dataset_path = os.path.sep.join([chest_xray_data_dir, ""])

    # store train paths
    train_dir = os.path.sep.join([dataset_path, "train"])
    store_label_to_split(normal_idx, train_dir, "train",
                         chest_xray_data_dir, **kwargs)
    store_label_to_split(pneumonia_idx, train_dir, "train",
                         chest_xray_data_dir, **kwargs)

    # store val paths
    val_dir = os.path.sep.join([dataset_path, "val"])
    store_label_to_split(normal_idx, val_dir, "val",
                         chest_xray_data_dir, **kwargs)
    store_label_to_split(pneumonia_idx, val_dir, "val",
                         chest_xray_data_dir, **kwargs)

    # store test paths
    test_dir = os.path.sep.join([dataset_path, "test"])

    # construct the path to the metadata CSV file and load it
    csvPath = os.path.sep.join([dataset_path, "derived.csv"])
    df = pd.read_csv(csvPath)

    # variables to store output paths
    x, y = [], []

    # loop over the rows of the COVID-19 data frame
    for (i, row) in df.iterrows():
        x.append(os.path.sep.join([test_dir, "unknown", row["Id"]]))
        y.append(row["Expected"])

    output_dir = os.path.join(kwargs["splits_dir"], kwargs["split"])
    store_split(x, y, os.path.join(output_dir, "test.txt"),
                kwargs["data_dir"], "a+")
