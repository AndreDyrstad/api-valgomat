import random
import json

def question_to_dict(q, display_as):
    """
    Converts a question object to a dict
    :param display_as: which type the question should be rendered as
    :param q: current question
    :return: dict with question information
    """

    return {'id':q.id, 'label': q.label, 'value': q.value, 'info': q.info, 'displayAs': display_as}

def questions_to_json(questions):
    """
    Converts a list of questions to json
    :param questions: questions to convert
    :return: json of dicts with questions
    """
    elements = []
    for q in questions:
        elements.append(question_to_dict(q,"None"))
    response = {'questions': elements}

    return response

def centers_to_json(centers):
    """
    Converts a list of centers to json
    :param centers: centers to convert
    :return: json of dicts with centers
    """
    elements = []
    for center in centers:
        elements.append({'id': center.id,'name' : center.name})
    return elements

def feedback_to_json(feedback):
    response = {"feedback": []}

    for element in feedback:
        response["feedback"].append({"center":element[2],"question":element[1],"score":element[0]})

    return response


def random_string(entities):
    """
    Generates a random unique 64 bits string of length 10
    :param entities: All entities in the database
    :param session: current session
    :return: random unique string
    """
    valid = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-_'

    string = ''.join((random.choice(valid) for i in range(10)))
    for entity in entities:
        if entity.name == string:
            return random_string(entities)

    return string

def update_config_file(data, entity_type):

    save_to_config = {}

    for key in data.keys():
        save_to_config[key] = []
        for question in data[key]:
            save_to_config[key].append({"id":question["id"],"displayAs":question["displayAs"]})

    if entity_type == "patient":
        with open('config_files/patient_config.json', 'w') as output_file:
            json.dump(save_to_config, output_file)
    else:
        with open('config_files/center_config.json', 'w') as output_file:
            json.dump(save_to_config, output_file)
