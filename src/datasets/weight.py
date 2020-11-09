import numpy as np                                                                
from PIL import Image                                                            
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV

def compute_split_weights(X_paths, y, size=(600, 600)):
    X = np.array([np.array(Image.open(path).convert('L').resize(size)) for path in X_paths])
    return compute_weights(X, y)

def compute_weights(X, y):
    gsc = GridSearchCV(
        estimator=SVC(C=1),
        param_grid={
            'class_weight': [0.001, 0.01, 0.1]
        },
        scoring='f1_macro',
        cv=5
    )
    grid_result = gsc.fit(X, y)

    print("Best parameters : %s" % grid_result.best_params_)
    return grid_result.best_params_['class_weight']
