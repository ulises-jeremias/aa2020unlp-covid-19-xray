"""Load covid chest xray"""

import os
import pandas as pd
from src.datasets.datagen import covid_idx

def row_filename(dataset_path, row):
    # build the path to the input image file
    imagePath = os.path.sep.join([dataset_path, "images", row["filename"]])

    # if the input image file does not exist (there are some errors in
    # the COVID-19 metadeta file), ignore the row
    if not os.path.exists(imagePath):
        return False

    # extract the filename from the image path
    return imagePath

def load_covid_chest_xray(data_dir):
    """
    Load covid chest xray

    Returns (x, y): as dataset x and y containing paths.

    """

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    covid_dataset_path = os.path.sep.join([data_dir, ""])

    # construct the path to the metadata CSV file and load it
    csvPath = os.path.sep.join([covid_dataset_path, "metadata.csv"])
    df = pd.read_csv(csvPath)

    # variables to store output paths
    x, y = [], []

    # loop over the rows of the COVID-19 data frame
    for (i, row) in df.iterrows():
        # if (1) the current case is not COVID-19 or (2) this is not
        # a 'PA' view, then ignore the row
        if row["finding"] == "COVID-19" and row["view"] == "PA":
            filename = row_filename(covid_dataset_path, row)
            if not filename:
                continue

            x.append(filename)
            y.append(covid_idx)

    return x, y
