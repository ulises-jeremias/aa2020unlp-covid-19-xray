#!/usr/bin/env python

import os
import argparse
import shutil
from tf_tools.datasets.splitsgen import generate_splits

from src.datasets.splitsgen.loader import load_from_split
from src.datasets.splitsgen.covid_chest_xray import load_covid_chest_xray
from src.datasets.splitsgen.covid19_radiography_database import load_covid19_radiography_database

parser = argparse.ArgumentParser(description="Generate splits for datasets")

parser.add_argument("--seed", type=int, default=42)
parser.add_argument("--split", type=str)
parser.add_argument("--dataset", type=str, default="", help="Dataset name")
parser.add_argument("--version", type=str, default="", help="Dataset version")
parser.add_argument("--data_dir", type=str, default="",
                     help="Directory to load and store data")
parser.add_argument("--splits_dir", type=str,
                     default="/tmp/splits", help="Output dir to save the splits")
parser.add_argument("--train_size", type=float, default=0)
parser.add_argument("--test_size", type=float, default=0.2)
parser.add_argument("--n_train_per_class", type=int, default=0)
parser.add_argument("--n_test_per_class", type=int, default=0)
parser.add_argument("--balanced", type=bool, default=False)

args = vars(parser.parse_args())

dataset_name = args["dataset"]
version = args["version"]
data_dir = args["data_dir"] if args["data_dir"] else os.path.sep.join(["./data", dataset_name, "data"])
split_name = args["split"]
splits_dir = args["splits_dir"]

# 0 => normal
# 1 => covid
# 2 => pneumonia

x, y = load_covid_chest_xray("./data/covid-chest-xray/data")
x2, y2 = load_covid19_radiography_database("./data/covid19-radiography-database/data")

x.extend(x2)
y.extend(y2)

generate_splits(x, y, **args)

# Load splits and save those into a new dataset called {dataset}

train_split = os.path.sep.join([splits_dir, split_name, "train.txt"])
test_split = os.path.sep.join([splits_dir, split_name, "test.txt"])
val_split = os.path.sep.join([splits_dir, split_name, "val.txt"])

splits = [
    (load_from_split(version, data_dir, train_split), 'train'),
    (load_from_split(version, data_dir, test_split), 'test'),
    (load_from_split(version, data_dir, val_split), 'val')
]

labels = ['normal', 'covid', 'pneumonia']

for (x_split, y_split), split in splits:
    split_dir = os.path.sep.join([data_dir, split_name, split])
    if not os.path.exists(split_dir):
        os.makedirs(split_dir)

    i = 0
    for img, label in zip(x_split, y_split):
        ext = img.split(".")[-1]
        dest = os.path.sep.join([split_dir, f"{i}.{ext}"])
        shutil.copy2(img, dest)
        i += 1
