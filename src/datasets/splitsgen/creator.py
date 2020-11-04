import os
import shutil
from src.datasets.splitsgen.loader import load_from_split

def create_dataset(dataset, version, data_dir, split, splits_dir, **kargs):
    data_dir = data_dir if data_dir else os.path.sep.join(["./data", dataset, "data"])

    # Load splits and save those into a new dataset called {dataset}
    train_split = os.path.sep.join([splits_dir, split, "train.txt"])
    test_split = os.path.sep.join([splits_dir, split, "test.txt"])
    val_split = os.path.sep.join([splits_dir, split, "val.txt"])
    splits = [
        (load_from_split(version, data_dir, train_split), 'train'),
        (load_from_split(version, data_dir, test_split), 'test'),
        (load_from_split(version, data_dir, val_split), 'val')
    ]

    labels = ['normal', 'covid', 'pneumonia']

    for (x_split, y_split), split_name in splits:
        split_dir = os.path.sep.join([data_dir, split, split_name])
        if not os.path.exists(split_dir):
            os.makedirs(split_dir)

        i = 0
        for img, label in zip(x_split, y_split):
            ext = img.split(".")[-1]
            dest = os.path.sep.join([split_dir, f"{i}.{ext}"])
            shutil.copy2(img, dest)
            i += 1
