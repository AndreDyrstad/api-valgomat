import pandas as pd
import numpy as np
import itertools
from database_folder.sql_queries import get_all_center_scores, get_all_connections
import requests


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
    #Remove all answers with the score of 0, since they add up to 0 at the end anyway
    #Reduces runtime
    for key, value in patient.items():
        if value != 0 and not isinstance(value, str):
            patient_information.append((key,value))
        elif isinstance(key, str) and value != 0:
            print("Postnummer:", value)

    patient_information = sorted(patient_information, key=lambda x: x[1], reverse=True)

    #metadata = pd.read_csv("centers3.csv", low_memory=False)
    #metadata = np.array(metadata)

    #get scores from database
    center_scores = get_all_center_scores()
    connections = get_all_connections()

    all_center_scores = []

    #Calculate score for each center
    current_center = center_scores[0]
    score_for_current_center = 0
    good_match_question = []

    #Number of iterations (testing only)
    i = 0

    for center_score in center_scores:
        print(center_score.Score.score)

        #Add to the same score as long as the center name is the same
        if center_score.Entity.name != current_center.Entity.name:
            score_for_current_center = int((score_for_current_center/len(patient_information))*10)
            all_center_scores.append((current_center.Entity.name,score_for_current_center,good_match_question))
            score_for_current_center = 0
            good_match_question = []
        current_center = center_score

        #Iterate answers and add scores -5 to 5 to the current score
        for question_name, answer_score in patient_information:
            i += 1
            if int(question_name) == center_score.Question.id:
                score_for_current_center += answer_score #* (center_score.Score.score/100)

                if answer_score > 0:
                    good_match_question.append(center_score.Question.label)

            #Check if the question is connected to any other question
            for connection in connections:
                if (connection.question_id == center_score.Question.id or connection.connected_to_id == center_score.Question.id)\
                        and (connection.question_id == int(question_name) or connection.connected_to_id == int(question_name)):
                    score_for_current_center += answer_score #* (center_score.Score.score/100)
                    good_match_question.append(center_score.Question.label)


    all_center_scores.append((current_center.Entity.name, score_for_current_center, good_match_question))

    all_center_scores = sorted(all_center_scores, key=lambda x: x[1], reverse=True)

    print("Number of iterations: ", i)

    response = {'centers': []}

    #Generate return string
    for score in all_center_scores[0:3]:
        response['centers'].append({'name':score[0],'probability':score[1],'match':score[2],'link':'#','about':'Her skal det stå informasjon om senteret'})

    return response

def get_distance_to_centers(postcode):
    URL = 'https://api.bring.com/shippingguide/api/postalCode.json?clientUrl=insertYourClientUrlHere&country=NO&'
    PARAMS = {'pnr': postcode}
    r = requests.get(url=URL, params=PARAMS)
    data = r.json()

    print(data["result"])

    list_of_postcodes = ['Oslo','Drammen', 'Bergen', "Os"]
    param_string = ""

    for codes in list_of_postcodes:
        param_string += data['result'] +'|'+ codes + '|'

    URL = 'https://no.avstand.org/route.json'
    PARAMS = {"stops":param_string}

    r = requests.get(url=URL, params=PARAMS)
    data = r.json()

    print(data["distances"])