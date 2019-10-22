## Predicting OBOS Damallsvenskan 2019 results
## -------------------------------------------

## RFClassifier.py is used to predict the outcomes for OBOS Damallsvenskan
## matches using a RandomForestClassifier.

import statistics

import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier

def load_(filename):
    return pd.read_csv(filename)

def training_data(df):
    x = df.iloc[:150, 6:-2].to_numpy()
    y = df.iloc[:150, -2:].to_numpy()
    return x, y

def test_data(df):
    x = df.iloc[150:, 6:-2].to_numpy()
    y = df.iloc[150:, -2:].to_numpy()
    rest = df.iloc[150:, 1:6]
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

    print(min(result), max(result))
    return statistics.mean(result)
    
def score_prediction(pTest, yTest):
    pDiff = yTest[:,:]-pTest
    return sum(sum(np.abs(pDiff)))

def predict(clfs, xTest):
    result = []
    counts = [{} for _ in range(len(xTest))]
    for clf in clfs:
        pTest = clf.predict(xTest)
        for p, c in zip(pTest, counts):
            try:
                c[tuple(p)] += 1
            except KeyError:
                c[tuple(p)] = 1
        result.append(pTest)

    result = np.asarray(result)
    return result[:,:].mean(axis = 0).round(), counts

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description = 'Predict the results of Round 20-22 with a RandomForestClassifier.')
    parser.add_argument('train', nargs = 1, help = 'filename of .csv file with training data')
    parser.add_argument('--test', dest='test', action='store_const',
                        const = True, default = False,
                        help = 'Test the classifier(s) and print a score (instead of predicting).')
    args = parser.parse_args()

    xTrain, yTrain = training_data(load_(args.train[0]))
    xTest, yTest, rest = test_data(load_(args.train[0]))
    if args.test:
        clfs = make_classifiers(xTrain, yTrain, n = 100)   
        print(test_classifiers(clfs, xTest, yTest, n = 100))

    else:
        clfs = make_classifiers(xTrain, yTrain, n = 100)
        pTest, pCount = predict(clfs, xTest)
        rest['pHome'] = pTest[:,0].astype(int)
        rest['pAway'] = pTest[:,1].astype(int)
        _ = rest.pop('Score')
        count = [["%d%% %d-%d" % (c[k], k[0], k[1])
                    for k in sorted(c.keys(),
                                    key = lambda x : c[x],
                                    reverse = True) if c[k] > 10] \
            for c in pCount]
        rest['counts'] = np.asarray(count)

        print(rest)
        print("Score: %.2f" % (score_prediction(pTest, yTest)))
