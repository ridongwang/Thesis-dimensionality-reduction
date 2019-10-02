#  import libraries for loading data
import pandas as pd
import numpy as np
import math 
from sklearn.preprocessing import label_binarize

#  import libraries for dimensionality reduction
from sklearn.feature_selection import SelectFromModel
from sklearn.manifold import Isomap

#  import libraries for classifier
from sklearn import datasets, preprocessing
from sklearn.model_selection import train_test_split  
from sklearn.ensemble import RandomForestClassifier
from sklearn.multiclass import OneVsRestClassifier

#  import libraries for evaluation
import time
from eval_metrics import model_evaluation

data_columns = {'Data': ["execution time", "AUC label 0", "AUC label 1", "AUC label 2", "Overall Accuracy", "Precision-Recall label 0", "Precision-Recall label 1", "Precision-Recall label 2", "Average Precision"]}
save_data = pd.DataFrame(data=data_columns)

x = pd.read_pickle(r"x_1000.pkl").values
y = pd.read_pickle(r"y_1000.pkl").values

#  binarize labels for multilabel auc calculations
y = label_binarize(y, classes=[0, 1, 2])
n_classes = y.shape[1]

#-------------------------------------------
# RUN CLASSIFIER WITH ISOMAP IMPLEMENTATION
#-------------------------------------------
classifier_condition = "Random Forest, ISOMAP"

x_train, x_test, y_train, y_test = train_test_split(x, y, stratify=y, test_size = 0.20, random_state=5)

start = time.time()

embedding = Isomap(n_components=6)
x_train = embedding.fit_transform(x_train)
x_test = embedding.fit_transform(x_test)

rfclassifier = RandomForestClassifier(n_estimators=500, random_state=5, criterion = 'gini')
classifier = OneVsRestClassifier(rfclassifier, n_jobs=-1)
classifier.fit(x_train, y_train)

prediction = classifier.predict(x_test)

end = time.time()

save_data[f"{classifier_condition}_n = 6"] = (model_evaluation("RF", "6", x_test, y_test, prediction, classifier, end-start, n_classes))

save_data.to_csv("Random_Forest_ISO_1000_6.csv")
