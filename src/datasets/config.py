"""
Labels:

    0 => normal
    1 => covid
    2 => pneumonia
"""

normal_idx = 0
covid_idx = 1
pneumonia_idx = 2

label_to_idx = {
    'normal': normal_idx,
    'covid': covid_idx,
    'pneumonia': pneumonia_idx,
}

labels = ['normal', 'covid', 'pneumonia']
weights = [1, 1, 1]
