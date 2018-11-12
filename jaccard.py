import pandas as pd
import numpy as np
import itertools

def jaccard_similarity(x, y):
    intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))
    return intersection_cardinality / float(union_cardinality)


def remove_items_from_center(metadata, patient_number):
    new_metadata = []

    for center in metadata:
        new_center = []
        for i in range(2,len(center)):
            if center[i] in metadata[patient_number]:
                new_center.append(center[i])
        new_metadata.append(new_center)

    return new_metadata


def calculate_and_print_scores(metadata, show_top_x, patient, new_metadata):

    scores = []

    for i in range(len(new_metadata)):
        scores.append((i+1,jaccard_similarity(patient,new_metadata[i])))

    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    print(patient)

    for score in scores[0:show_top_x]:
        print(metadata[score[0]][1] + ":","%.2f" % score[1],new_metadata[score[0]-1])


def predict_center(patient):

    new_patient = []

    for key in patient.keys():
        new_patient.append(patient[key])

    patient = list(itertools.chain.from_iterable(new_patient))

    print(patient)

    metadata = pd.read_csv("centers3.csv", low_memory=False)
    metadata = np.array(metadata)

    patient_number = 44
    show_top_x = 3

    new_metadata = remove_items_from_center(metadata,patient_number)
    #patient = new_metadata[patient_number]
    new_metadata.__delitem__(patient_number)

    calculate_and_print_scores(metadata, show_top_x, patient, new_metadata)

#predict_center(patient)
