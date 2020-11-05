import os
import csv
import shutil
from PIL import Image
from src.datasets.datagen.loader import load_from_split

def copy_img_to_ds(src, dst, size = (600, 600)):
    img = Image.open(src).convert('L')
    img = img.resize(size)
    img.save(dst)

def create_split_dir(split, split_name, labels, data_dir):
    split_dir = os.path.sep.join([data_dir, split, split_name])

    labels = ['unknown'] if split_name == 'test' else labels

    # create dirs for labels into {split_dir}
    for label in labels:
        label_dir = os.path.sep.join([split_dir, label])
        if not os.path.exists(label_dir):
            os.makedirs(label_dir)

    return split_dir

def create_dataset(dataset, version, data_dir, split, splits_dir, **kwargs):
    data_dir = data_dir if data_dir else os.path.sep.join(["./data", dataset, "data"])

    # Load splits and save those into a new dataset called {dataset}
    train_split = os.path.sep.join([splits_dir, split, "train.txt"])
    test_split = os.path.sep.join([splits_dir, split, "test.txt"])
    val_split = os.path.sep.join([splits_dir, split, "val.txt"])
    train_val = [
        (load_from_split(version, data_dir, train_split), 'train'),
        (load_from_split(version, data_dir, val_split), 'val')
    ]
    test = (load_from_split(version, data_dir, test_split), 'test')

    labels = ['normal', 'covid', 'pneumonia']

    # generate labeled train and val sets
    for (x_split, y_split), split_name in train_val:
        split_dir = create_split_dir(split, split_name, labels, data_dir)
            
        # labels counter to determine file name based on split and label
        labels_counter = {'normal': 0, 'covid': 0, 'pneumonia': 0}

        for img, label in zip(x_split, y_split):
            # str representation of the label
            label = labels[label]
            
            i = labels_counter[label]
            ext = img.split(".")[-1]
            dest = os.path.sep.join([split_dir, label, f"{i}.jpg"])
            copy_img_to_ds(img, dest)
            labels_counter[label] += 1

    # generate test with unknown label
    (x_split, y_split), split_name = test
    split_dir = create_split_dir(split, split_name, labels, data_dir)
        
    # labels counter to determine file name based on split and label
    i = 0
    filenames, y_test = [], []

    for img, label in zip(x_split, y_split):
        ext = img.split(".")[-1]
        dest = os.path.sep.join([split_dir, 'unknown', f"{i}.jpg"])
        copy_img_to_ds(img, dest)
        filenames.append(f"{i}.jpg")
        y_test.append(label)
        i += 1

    # save test labels for kaggle
    with open(os.path.sep.join([data_dir, split 'derived.csv']), mode='w') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        writer.writerow(['Id', 'Expected'])
        for f, y in zip(filenames, y_test):
            writer.writerow([f, str(y)])
