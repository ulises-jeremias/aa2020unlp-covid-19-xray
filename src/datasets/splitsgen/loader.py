import os
import numpy as np

def load_from_split(version, data_dir, split_file):
    x, y = [], []

    with open(split_file, 'r') as f:
        for i, line in enumerate(f.readlines()):
            target, *filepath = reversed(line.rstrip('\n').split(' '))
            filepath = ' '.join(reversed(filepath))
            x.append(filepath)
            y.append(int(target))

    return x, y
