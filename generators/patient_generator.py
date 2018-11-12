import json
import random
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import Perceptron
from sklearn import preprocessing
import itertools


def read_json():

    with open('../storage/patients.json') as f:
        data = json.load(f)

    keys = data["questions"].keys()
    question_number = 0
    labels = []

    for key in keys:
        labels.append([])

        #Add all labels to the list
        labels[question_number] = list(map(lambda x: x["value"],data["questions"][key]))

        question_number += 1

    return labels, keys

def generate_center_data(labels, keys):
    string = "id,name,a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z\n"


    for i in range(50):
        element_number = 0
        string += str(i) + ",Senter " + str(i) + ","
        for key in keys:
            if element_number < 3:
                labels[element_number].sort()
                if element_number == 2:
                    amount = random.sample(range(3,7),1)[0]
                    random_numbers = random.sample(range(len(labels[element_number])), amount)
                else:
                    amount = random.sample(range(2,4),1)[0]
                    random_numbers = random.sample(range(len(labels[element_number])), amount)
                for number in random_numbers:
                    string += labels[element_number][number] + ","
                element_number += 1
        string = string[:-1]
        string += "\n"
    return string


def generate_patient_data(labels, keys):
    patients = []
    target = []

    for i in range(0, 10):
        data = []
        element_number = 0

        for key in keys:

            random_numbers = random.sample(range(len(labels[element_number])), 3)

            for number in range(len(labels[element_number])):
                data.append("none") if number not in random_numbers else data.append(labels[element_number][number])

            element_number += 1
        target.append(initial_rules(data))
        patients.append(data)

    return patients, target


def initial_rules(data):

    switcher = {
        "basseng" in data: 0,
        "blære" in data: 1,
        "tarm" in data: 1,
        "arbeidsrettet" in data: 2,
        "nyFysiskAktivitet" in data: 2,
        "gange/balanse" in data: 3,
        "spastisitet" in data: 3,
        "smerte" in data: 4,
        "kognitiv" in data: 5,
        "stressmestring" in data: 5,
    }

    return switcher.get(True, 6)


def classifier(X, y, labels):

    #Make list of lists to a single list
    labels = list(itertools.chain.from_iterable(labels))

    labels.append("none")
    le = preprocessing.LabelEncoder()
    le.fit(labels)

    #Encode every patient to floats (it will not work with sklearn otherwise)
    X = list(map(lambda x: le.transform(x), X))

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.4, random_state = 10)
    clf = Perceptron()
    print("training")
    clf.fit(X_train, y_train)

    print("validating")
    scores = cross_val_score(clf, X_test, y_test, cv=10)

    print(scores)


labels, keys = read_json()
#patients, target = generate_patient_data(labels, keys)
print(generate_center_data(labels, keys))
#print(patients)
#print(target[0])

#classifier(patients, target, labels)
