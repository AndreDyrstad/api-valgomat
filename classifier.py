from sklearn.tree import DecisionTreeClassifier
from sklearn import datasets
import pprint
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import Perceptron

def classify_document(data):
    iris = datasets.load_iris()

    X = iris["data"]
    y = iris["target"]

    cf = DecisionTreeClassifier()

    cf.fit(X,y)
    print(cf.predict([[1,2,1,2]])[0])
    return str(cf.predict([[1,2,1,2]])[0])


def make_classifier(data):
    print(data[0]["navn"])


def classifier(X,y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.4, random_state = 0)
    clf = Perceptron()
    clf.fit(X_train, y_train)

    scores = cross_val_score(clf, X_test, y_test, cv=5)

    print(scores)
