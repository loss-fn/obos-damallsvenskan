import statistics

import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier

def load_(filename):
    return pd.read_csv(filename)

def training_data(df):
    x = df.iloc[:108, 6:-2].to_numpy()
    y = df.iloc[:108, -2:].to_numpy()
    return x, y

def test_data(df):
    x = df.iloc[108:114, 6:-2].to_numpy()
    y = df.iloc[108:114, -2:].to_numpy()
    return x, y

def make_classifiers(xTrain, yTrain):
    from random import randint
    result = []
    for _ in range(100):
        clf = RandomForestClassifier(n_estimators = randint(8,32))
        clf.fit(xTrain, yTrain)
        result.append(clf)
    return result

def test_classifiers(clfs, xTest, yTest):
    result = []
    for _ in range(100):
        for clf in clfs:
            pTest = clf.predict(xTest)
            result.append(score_prediction(pTest, yTest))

    return statistics.mean(result)
    
def score_prediction(pTest, yTest):
    pDiff = yTest[:,:]-pTest
    return sum(sum(pDiff))

def predict(clfs, xTest):
    result =[] 
    for clf in clfs:
        pTest = clf.predict(xTest)
        result.append(pTest)

    result = np.asarray(result)
    return result[:,:].mean(axis = 0).round()

if __name__ == "__main__":
    xTrain, yTrain = training_data(load_('train.csv'))
    xTest, yTest = test_data(load_('train.csv'))
    clfs = make_classifiers(xTrain, yTrain)
    #print(test_classifiers(clfs, xTest, yTest))
    pTest = predict(clfs, xTest)
    print(yTest)
    print(pTest)
    print(score_prediction(pTest, yTest))
