import requests

from sql_queries import get_all_center_scores, get_all_connections

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


    #get scores from database
    center_scores = get_all_center_scores()
    connections = get_all_connections()

    all_center_scores = []

    #Calculate score for each center
    current_center = center_scores[0]
    score_for_current_center = 0
    good_match_question = []


    for center_score in center_scores:
        print(center_score.Score.score)

        #Add to the same score as long as the center name is the same
        if center_score.Entity.name != current_center.Entity.name:
            score_for_current_center = int((score_for_current_center/len(patient_information))*10)

            center_name = "Behandlingssted " + str(current_center.Entity.id) # Change after testing to current_center.Entity.name

            all_center_scores.append((center_name,score_for_current_center,good_match_question))
            score_for_current_center = 0
            good_match_question = []
        current_center = center_score

        #Iterate answers and add scores -5 to 5 to the current score
        for question_name, answer_score in patient_information:
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

    center_name = "Behandlingssted " + str(current_center.Entity.id)  # Change after testing to current_center.Entity.name

    all_center_scores.append((center_name, score_for_current_center, good_match_question))

    all_center_scores = sorted(all_center_scores, key=lambda x: x[1], reverse=True)

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