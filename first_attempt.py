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
    rest = df.iloc[108:114, 1:6]
    return x, y, rest

def make_classifiers(xTrain, yTrain, n = 100):
    from random import randint
    result = []
    for _ in range(n):
        clf = RandomForestClassifier(n_estimators = randint(8,32))
        clf.fit(xTrain, yTrain)
        result.append(clf)
    return result

def test_classifiers(clfs, xTest, yTest, n = 100):
    result = []
    for _ in range(n):
        for clf in clfs:
            pTest = clf.predict(xTest)
            result.append(score_prediction(pTest, yTest))

    return statistics.mean(result)
    
def score_prediction(pTest, yTest):
    pDiff = yTest[:,:]-pTest
    return sum(sum(np.abs(pDiff)))

def predict(clfs, xTest):
    result =[] 
    for clf in clfs:
        pTest = clf.predict(xTest)
        result.append(pTest)

    result = np.asarray(result)
    return result[:,:].mean(axis = 0).round()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description = 'Predict the results of Round 19 with a RandomForestClassifier.')
    parser.add_argument('--test', dest='test', action='store_const',
                        const = True, default = False,
                        help = 'Test the classifier(s) and print a score (instead of predicting).')
    args = parser.parse_args()

    xTrain, yTrain = training_data(load_('train.csv'))
    xTest, yTest, rest = test_data(load_('train.csv'))
    if args.test:
        clfs = make_classifiers(xTrain, yTrain, n = 100)   
        print(test_classifiers(clfs, xTest, yTest, n = 100))

    else:
        clfs = make_classifiers(xTrain, yTrain, n = 100)
        pTest = predict(clfs, xTest)
        rest['pHo'] = pTest[:,0].astype(int)
        rest['pAw'] = pTest[:,1].astype(int)
        print(rest)
        print("Score: %.2f" % (score_prediction(pTest, yTest)))
