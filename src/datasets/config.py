"""
Labels:

    0 => normal
    1 => covid
    1 => pneumonia
"""

normal_idx = 0
covid_idx = 1
pneumonia_idx = 1

label_to_idx = {
    'normal': normal_idx,
    'covid': covid_idx,
    'pneumonia': pneumonia_idx,
}

# labels = ['normal', 'covid', 'pneumonia']
# labels_idxs = [normal_idx, covid_idx, pneumonia_idx]

labels = ['normal', 'pneumonia']
labels_idxs = [normal_idx, pneumonia_idx]
