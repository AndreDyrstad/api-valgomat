import pandas as pd
import numpy as np
import itertools
import math

def jaccard_similarity(x, y):
    """
    Formula to check the similarity of two sets.
    :param x: set 1
    :param y: set 2
    :return: A score based on jaccard index
    """
    intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))
    return intersection_cardinality / float(union_cardinality)


def remove_items_from_center(metadata, patient):
    """
    Clean the data to make it possible to use Jaccard. Remove name and id
    :param metadata: data from centers
    :param patient: patient data we want to use
    :return: new list of metadata
    """
    new_metadata = []

    for center in metadata:
        new_center = []
        for i in range(2,len(center)):
            if center[i] in patient:
                new_center.append(center[i])
        new_metadata.append(new_center)

    return new_metadata


def calculate_and_print_scores(metadata, show_top_x, patient, new_metadata):
    """
    Calculates the score for each center and selects the best tree
    :param metadata: Data from centers
    :param show_top_x: how many centers to show
    :param patient: patient data
    :param new_metadata: list of clean data from centers
    :return: json with results
    """

    scores = []

    for i in range(len(new_metadata)):
        scores.append((i+1,jaccard_similarity(patient,new_metadata[i])))

    scores = sorted(scores, key=lambda x: x[1], reverse=True)


    #for score in scores[0:show_top_x]:
        #print(metadata[score[0]][1] + ":","%.2f" % score[1],new_metadata[score[0]-1])
		
    return generate_json(metadata,scores,new_metadata)

	
def generate_json(metadata,scores, new_metadata):
    """
    Generate json based on results
    :param metadata: data from centers
    :param scores: scores form Jaccard
    :param new_metadata: clean data
    :return: json response with results
    """
    response = {}
    response['centers'] = []
	
    for score in scores[0:3]:
	
        response['centers'].append({'name':metadata[score[0]][1],'probability':score[1],'link':'#','about':'informasjon'})
								
    return response


def predict_center(patient):
    """
    Main method to predict a center
    :param patient: patient we want to predict
    :return: json of scores
    """
    new_patient = []

    for key in patient.keys():
        new_patient.append(patient[key])

    patient = list(itertools.chain.from_iterable(new_patient))

    metadata = pd.read_csv("centers3.csv", low_memory=False)
    metadata = np.array(metadata)

    patient_number = 44
    show_top_x = 3


    new_metadata = remove_items_from_center(metadata,patient)
    #patient = new_metadata[patient_number]
    #new_metadata.__delitem__(patient_number)

    return calculate_and_print_scores(metadata, show_top_x, patient, new_metadata)


def use_scores(patient):
    """
    Used to calculate the scores when a patient is submitting answers.
    This is used when the data i submitted with the slider form.
    :param patient:
    :return:
    """

    patient_information = []

    #Make tuple
    for key, value in patient.items():
        patient_information.append((key,value))

    patient_information = sorted(patient_information, key=lambda x: x[1], reverse=True)

    metadata = pd.read_csv("centers3.csv", low_memory=False)
    metadata = np.array(metadata)

    scores = []

    #Calculate score for each center
    for element in metadata:
        current_score = 0
        good_match = []
        for name, score in patient_information:
            if name in element:
                current_score += score - 5
                if score > 5:
                    good_match.append(name)

        scores.append((element[1],current_score,good_match))

    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    response = {'centers': []}

    #Generate return string
    for score in scores[0:3]:
        response['centers'].append({'name':score[0],'probability':score[1],'match':score[2],'link':'#','about':'informasjon'})

    for r in response['centers']:
        print(r)
        print()
    print(patient_information)
    print()
    print()
    print()

    return response


"""use_scores({'aktiviteter': 75,
            'arbeidsrettet': 50,
            'arm/hånd': 50,
            'barnPårørende': 10,
            'basseng': 50,
            'behovHjelpemidler': 100,
            'bevegelseshemmedeUte': 50,
            'bevegelseshemmendeInne': 50,
            'blære': 50,
            'dagopphold': 50,
            'depresjon/angst': 50,
            'døgnopphold': 50,
            'fatigue': 50,
            'gange/balanse': 40,
            'gruppe': 50,
            'individuell': 50,
            'informasjon': 50,
            'kognitiv': 50,
            'kost': 50,
            'lunge': 50,
            'nyFysiskAktivitet': 50,
            'nærhet': 50,
            'poliklinikk': 50,
            'rehabilitering': 35,
            'rehabiliteringGradvis': 50,
            'rehabiliteringRaskt': 100,
            'røykeslutt': 50,
            'sammeDiagnose': 50,
            'seksual': 50,
            'selvhjulpen': 50,
            'smerte': 50,
            'spastisitet': 50,
            'stressmestring': 75,
            'søvn': 50,
            'tale/språk/svelg': 50,
            'tarm': 50,
            'voksnePårørende': 100,
            'vurdering': 50,
            })"""
#predict_center(patient)
