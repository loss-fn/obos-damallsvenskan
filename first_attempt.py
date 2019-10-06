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

def make_classifier(xTrain, yTrain):
    clf = RandomForestClassifier(n_estimators = 10)
    clf.fit(xTrain, yTrain)
    return clf

def test_classifier(clf, xTest, yTest):
    pTest = clf.predict(xTest)
    return pTest, score_prediction(pTest, yTest)
    
def score_prediction(pTest, yTest):
    pDiff = yTest[:,:]-pTest
    return sum(sum(pDiff))

if __name__ == "__main__":
    xTrain, yTrain = training_data(load_('train.csv'))
    xTest, yTest = test_data(load_('train.csv'))
    clf = make_classifier(xTrain, yTrain)
    print(test_classifier(clf, xTest, yTest))
