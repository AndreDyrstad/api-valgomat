from sklearn.tree import DecisionTreeClassifier
from sklearn import datasets

def classify_document(data):
    iris = datasets.load_iris()

    X = iris["data"]
    y = iris["target"]

    cf = DecisionTreeClassifier()

    cf.fit(X,y)
    print(cf.predict([[1,2,1,2]])[0])
    return str(cf.predict([[1,2,1,2]])[0])