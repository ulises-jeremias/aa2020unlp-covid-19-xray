#!/usr/bin/env python

from tf_tools.datasets.splitsgen import generate_splits

from src.datasets.splitsgen.args import parse_args
from src.datasets.splitsgen.creator import create_dataset
from src.datasets.splitsgen.covid_chest_xray import load_covid_chest_xray
from src.datasets.splitsgen.covid19_radiography_database import load_covid19_radiography_database

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

    generate_splits(x, y, **args)
    create_dataset(**args)
