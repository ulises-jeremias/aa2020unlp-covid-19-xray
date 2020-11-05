#!/usr/bin/env python

from tf_tools.datasets.splitsgen import generate_splits

from src.datasets.datagen.args import parse_args
from src.datasets.datagen.creator import create_dataset
from src.datasets.datagen.loader import load_chest_xray_splits, load_covid_chest_xray, load_covid19_radiography_database

if __name__ == '__main__':
    args = parse_args()

    """
    Labels:
    0 => normal
    1 => covid
    2 => pneumonia
    """

    x, y = load_covid_chest_xray("./data/covid-chest-xray/data")
    x2, y2 = load_covid19_radiography_database("./data/covid19-radiography-database/data")
    x.extend(x2)
    y.extend(y2)

    if args["generate_splits"]:
        generate_splits(x, y, **args)
        load_chest_xray_splits("./data/chest_xray/data", **args)

    if args["write_dataset"]:
        create_dataset(**args)
