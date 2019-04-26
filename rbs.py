import requests

from sql_queries import get_all_center_scores, get_all_connections

def recommend_center_based_on_patient_answers(patient):
    """
    Used to calculate the scores when a patient is submitting answers.
    This is used when the data i submitted with the slider form.
    :param patient: Patient answers
    :return: a JSON response with the results
    """

    #get scores from database
    center_scores = get_all_center_scores()
    connections = get_all_connections()

    list_of_all_center_scores = []

    list_of_centers = split_each_center_to_its_own_list(center_scores)
    patient_question_and_score_tuple = remove_scores_bellow_threshold(patient)

    for center in list_of_centers.keys():
        score_for_current_center = 0 #Reset variable on new center
        questions_that_gives_a_match = [] #Reset variable on new center

        for center_score_for_current_question in list_of_centers[center]:

            #Iterate answers and add scores 0 to 10 to the current score
            for question_id, question_score in patient_question_and_score_tuple:
                if int(question_id) == center_score_for_current_question.Question.id:
                    score_for_current_center += question_score * (center_score_for_current_question.Score.score/100)
                    questions_that_gives_a_match.append(center_score_for_current_question.Question.label)

                #Check if the question is connected to any other question
                for connection in connections:
                    if there_is_a_connection(connection, question_id, center_score_for_current_question):
                        questions_that_gives_a_match.append(center_score_for_current_question.Question.label)
                        score_for_current_center += question_score * (center_score_for_current_question.Score.score/100)

        center_name = "Behandlingssted " + str(list_of_centers[center][0].Entity.id)  # Change after testing to current_center.Entity.name
        list_of_all_center_scores.append((center_name, score_for_current_center, questions_that_gives_a_match))

    return generate_json_from_results(list_of_all_center_scores, len(patient_question_and_score_tuple))


def split_each_center_to_its_own_list(center_scores):
    current_center = center_scores[0].Entity.name
    list_of_centers = {current_center:[]}
    for score in center_scores:
        if score.Entity.name != current_center:
            current_center = score.Entity.name
            list_of_centers[current_center] = []
        list_of_centers[current_center].append(score)

    return list_of_centers


def remove_scores_bellow_threshold(patient):
    """
    Iterates trough the patient answers and removes all questions that has a score bellow the threshold
    :param patient: Patient answers
    :return: sorted list of all scores
    """

    patient_question_and_score_tuple = []
    threshold = 0

    for question, score in patient.items():
        if score > threshold and not isinstance(score, str):
            patient_question_and_score_tuple.append((question,score))
        elif isinstance(question, str) and score > threshold: #if questions is not a number, it has to be the post code
            print("Postnummer:", score)

    return sorted(patient_question_and_score_tuple, key=lambda x: x[1], reverse=True)

def there_is_a_connection(connection, question_id, center_score_for_current_question):
    """
    Check if there is a connection between two questions
    :param connection: list of all connections
    :param question_id: current questions we want to check
    :param center_score_for_current_question: Score object of current question
    :return: True if there is a connection, else false
    """

    if connection.question_id == center_score_for_current_question.Question.id or connection.connected_to_id == center_score_for_current_question.Question.id:
        if connection.question_id == int(question_id) or connection.connected_to_id == int(question_id):
            return True
        return False

def generate_json_from_results(list_of_all_center_scores, questions_answered):
    """
    Generates a JSON file from the RBS results
    :param list_of_all_center_scores: Results from RBS
    :param questions_answered: Number of questions that has a score above the threshold
    :return: a JSON response
    """
    #Sort list by score, descending
    list_of_all_center_scores = sorted(list_of_all_center_scores, key=lambda x: x[1], reverse=True)
    print(list_of_all_center_scores)
    response = {'centers': []}

    #Generate JSON from top three results
    for score in list_of_all_center_scores[0:3]:
        probability = "Behandlingsstedet tilbyr " + str(len(score[2])) + " av " + str(questions_answered) +" behandlinger som er viktig for deg"
        response['centers'].append({'name':score[0],'probability':probability,'match':score[2],'link':'#','about':'Her skal det stå informasjon om senteret'})

    return response

def get_distance_to_centers(postcode):
    """
    Method for finding treatment centers close to the patient
    :param postcode: Patient postcode
    :return: Distances
    """
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
