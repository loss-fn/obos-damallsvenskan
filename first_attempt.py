import pandas

from sklearn.ensemble import RandomForestClassifier

def load_(filename):
    return pandas.read_csv(filename)

def training_data(df):
    x = df.iloc[:108, 6:-2].to_numpy()
    y = df.iloc[:108, -2:].to_numpy()
    return x, y

def test_data(df):
    x = df.iloc[108:114, 6:-2].to_numpy()
    y = df.iloc[108:114, -2:].to_numpy()
    return x, y

def make_classifier(xTrain, yTrain):
    clf = RandomForestClassifier()
    clf.fit(xTrain, yTrain)
    return clf

def validate(clf, xTest, yTest):
    pTest = clf.predict(xTest)
    print(pTest)
    print(yTest)

if __name__ == "__main__":
    xTrain, yTrain = training_data(load_('train.csv'))
    xTest, yTest = test_data(load_('train.csv'))
    clf = make_classifier(xTrain, yTrain)
    validate(clf, xTest, yTest)
