import os
import csv
import shutil
from PIL import Image
from src.datasets import labels, compute_split_weights
from src.datasets.datagen.loader import load_from_split

def copy_img_to_ds(src, dst, size=(600, 600)):
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

def generate_split(split, data_dir, sets=[]):
    dataset_paths = {}

    for (x_split, y_split), split_name in sets:
        split_dir = create_split_dir(split, split_name, labels, data_dir)
            
        # labels counter to determine file name based on split and label
        labels_counter = {'normal': 0, 'covid': 0, 'pneumonia': 0}

        X, y = [], []        

        for img, label in zip(x_split, y_split):
            y.append(label)

            # str representation of the label
            label = labels[label]
            
            i = labels_counter[label]
            ext = img.split(".")[-1]
            dest = os.path.sep.join([split_dir, label, "{0:04d}.jpg".format(i)])
            copy_img_to_ds(img, dest)
            X.append(dest)
            labels_counter[label] += 1

        dataset_paths[split_name] = (X, y)

    return dataset_paths
        

def create_dataset(dataset, version, data_dir, split, splits_dir, **kwargs):
    data_dir = data_dir if data_dir else os.path.sep.join(["./data", dataset, "data"])

    # Load splits and save those into a new dataset called {dataset}
    train_split_path = os.path.sep.join([splits_dir, split, "train.txt"])
    test_split_path = os.path.sep.join([splits_dir, split, "test.txt"])
    val_split_path = os.path.sep.join([splits_dir, split, "val.txt"])
    train_split = (load_from_split(version, data_dir, train_split_path), 'train')
    val_split = (load_from_split(version, data_dir, val_split_path), 'val')
    test_split = (load_from_split(version, data_dir, test_split_path), 'test')

    # splits to iterate
    train_val_test = [train_split, val_split, test_split]
    train_val = [train_split, val_split]
    test = [test_split]

    # generate labeled train and val sets
    generate_split(split, data_dir, sets=train_val)

    # generate all datasets in one
    sets = ([], [])
    for (X, y), _ in train_val_test:
        sets = (X + sets[0], y + sets[1])
    paths = generate_split(split, data_dir, sets=[(sets, 'dataset')])
    (X, y) = paths['dataset']

    # generate test with unknown label
    (x_split, y_split), split_name = test_split
    split_dir = create_split_dir(split, split_name, labels, data_dir)
        
    # labels counter to determine file name based on split and label
    i = 0
    filenames, y_test = [], []

    for img, label in zip(x_split, y_split):
        ext = img.split(".")[-1]
        dest = os.path.sep.join([split_dir, 'unknown', "{0:04d}.jpg".format(i)])
        copy_img_to_ds(img, dest)
        filenames.append("{0:04d}.jpg".format(i))
        y_test.append(label)
        i += 1

    weights = compute_split_weights(X, y)

    # save test labels for kaggle
    with open(os.path.sep.join([data_dir, split, 'derived.csv']), mode='w') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Id', 'Expected', 'Weight'])
        for f, y in zip(filenames, y_test):
            weight = weights[y]
            writer.writerow([f, str(y), str(weight)])
