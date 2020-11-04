import os
import shutil
from src.datasets.splitsgen.loader import load_from_split

def create_dataset(**args):
    dataset_name = args["dataset"]
    version = args["version"]
    data_dir = args["data_dir"] if args["data_dir"] else os.path.sep.join(["./data", dataset_name, "data"])
    split_name = args["split"]
    splits_dir = args["splits_dir"]

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
