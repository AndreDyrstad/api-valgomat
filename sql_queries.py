from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
import random
import itertools

from database import Address, Base, Patient, Question, Score, Entity, Center, Response, Connection

# Insert: Add new element to the database
# Set: Change cell/row
# Get: Get information from the database

def init():
    engine = create_engine('sqlite:///valgomat.db')
    # Bind the engine to the metadata of the Base class so that the
    # declaratives can be accessed through a DBSession instance
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    # A DBSession() instance establishes all conversations with the database
    # and represents a "staging zone" for all the objects loaded into the
    # database session object. Any change made against the objects in the
    # session won't be persisted into the database until you call
    # session.commit(). If you're not happy about the changes, you can
    # revert all of them back to the last commit by calling
    # session.rollback()
    return DBSession()


def random_string():
    """
    Generates a random unique 64 bits string of length 10
    :param session: current session
    :return: random unique string
    """
    valid = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-_'

    entities = get_all_entities()
    string = ''.join((random.choice(valid) for i in range(10)))
    for entity in entities:
        if entity.name == string:
            return random_string()

    return string



def fill_table():
    """
    Used for testing. Adds test values to the database.
    :param session: current session
    :return: None
    """

    session = init()

    new_entity = Entity(type="center", name="Senter 1")
    new_center = Center(contact_person = "mail@address.com", phone_number=12345678, entity=new_entity)
    new_address = Address(street_name="testname", street_number=51, post_code=1236, entity=new_entity)
    new_question = Question(label="Spørsmål 1", value="spørsmål1", info="Mer info")
    new_Score = Score(score=50.0, entity=new_entity, question=new_question)

    new_entity2 = Entity(type="patient", name=random_string())
    new_patient = Patient(date_of_birth = "03.04.05", entity=new_entity2)
    new_address2 = Address(street_name="sesame street", street_number=2, post_code=9999, entity=new_entity2)
    new_question2 = Question(label="Spørsmål 2", value="spørsmål2", info="Enda mer info")
    new_Score2 = Score(score=76.0, entity=new_entity2, question=new_question2)
    new_Score3 = Score(score=10.0, entity= new_entity, question=new_question2)

    new_response = Response(patient=new_patient, center=new_center, question=new_question, score=34.0)

    session.add(new_entity)
    session.add(new_center)
    session.add(new_address)
    session.add(new_question)
    session.add(new_Score)

    session.add(new_entity2)
    session.add(new_patient)
    session.add(new_address2)
    session.add(new_question2)
    session.add(new_Score2)
    session.add(new_Score3)

    session.add(new_response)

    session.commit()

    session.close()


def insert_questions_from_json():
    """
    Read questions from a json file and add it to the database.
    :param session:
    :return:
    """

    session = init()

    with open('storage/all_questions.json') as f:
        data = json.load(f)

    keys = data["questions"].keys()

    for key in keys:
        items = data["questions"][key]
        for i in range(len(items)):
            row = items[i]
            if "extra" in items[i]:
                insert_question(row["label"],row["value"],row["extra"])
            else:
                insert_question(row["label"], row["value"], None)

    new_connection = Connection(question_id=28, connected_to_id=40)
    session.add(new_connection)
    session.commit()

    session.close()

def insert_question(label, value, info):
    """
    Used to insert a new question to the database.
    :param label: Question label
    :param value: Question value
    :param info: More information about the question
    :param session: current session
    :return: None
    """
    session = init()

    new_question = Question(label=label, value=value, info=info)
    session.add(new_question)
    session.commit()
    session.close()

def insert_question_from_api(json_data):
    """
    Used to insert a new question to the database.
    :param json_data: the question we want to add
    :return: None
    """
    session = init()


    new_question = Question(label=json_data['label'], value=json_data['value'], info=json_data['info'])
    session.add(new_question)
    session.commit()
    session.close()


def insert_patient_answers(answers):
    """
    Inserts new answers from a patient.
    :param answers: patient answers
    :param session: current session
    :return: patient with anonymous name
    """

    session = init()

    new_answers = []

    for key in answers.keys():
        new_answers.append(answers[key])

    new_entity = Entity(name=random_string(), type="patient")
    new_patient = Patient(date_of_birth="11.11.11", entity=new_entity)
    new_address = Address(post_code="1337", entity=new_entity)

    session.add(new_address)
    session.add(new_patient)
    session.add(new_entity)

    for answer in answers:
        q = session.query(Question).filter(Question.value == answer).first()
        try:
            new_score = Score(entity=new_entity, question=q, score=answers[answer])
            session.add(new_score)
            session.commit()
        except:
            session.rollback()
            print("error")


    return new_entity.name

def insert_patient_response(json_data):
    """
    This method is used to insert a response from a patient.
    :param json_data: response data {score1: 5 ,..., center: CenterA, patient: PatientA}
    :return: Status message
    """
    session = init()
    #Find center and patient with input name
    center = session.query(Center).join(Entity).filter(Entity.name == json_data['center']).first()
    patient = session.query(Patient).join(Entity).filter(Entity.name == json_data['patient']).first()

    print(center, patient)

    #Add all responses to the database
    for element in json_data:
        question = session.query(Question).filter(Question.value == element).first()
        if not isinstance(json_data[element], str):
            new_response = Response(patient=patient, center=center, question=question, score=json_data[element])
            session.add(new_response)
            session.commit()

    session.close()
    return 'success'

def insert_new_center(json_data):
    """
    Inserts a new center to the database.
    All the questions answered is also added to the database with a default score of 50.
    :param json_data: json_data from the frontend application
    :return: None
    """
    session = init()
    questions = get_all_questions()["questions"]

    new_entity = Entity(type="center", name=json_data["navn"])
    new_center = Center(contact_person =json_data["kontaktinformasjon"] , phone_number=json_data["telefonnummer"], entity=new_entity)
    new_address = Address(street_name="testname", street_number=51, post_code=1236, entity=new_entity)


    session.add(new_entity)
    session.add(new_center)
    session.add(new_address)
    session.commit()


    keys = json_data.keys()

    for key in keys:
        for question in questions:
            if isinstance(json_data[key], list):
                for data in json_data[key]:
                    if data == question["value"]:
                        q = session.query(Question).filter(Question.value == data).first()
                        new_score = Score(entity=new_entity, question=q, score=50.0)
                        session.add(new_score)
                        session.commit()

            elif key == question["value"] and not json_data[key] == 'false':
                q = session.query(Question).filter(Question.value == question["value"]).first()
                new_score = Score(entity=new_entity, question=q, score=50.0)
                session.add(new_score)
                session.commit()

    session.close()


def set_new_question_score_for_center( name, question, score):
    """
    Change the score for a center according to the input value
    :param session: current session
    :param name: center name (not id)
    :param score: new score
    :param question: value of question you want to change.
    :return: Status
    """

    session = init()

    center_id = session.query(Entity.id).filter(Entity.name == name).first()
    question_id = session.query(Question.id).filter(Question.value == question).first()

    try:
        session.query(Score).filter(Score.entity_id == center_id[0]).filter(Score.question_id == question_id[0]).update({"score": score})
        session.commit()
        session.close()
        return "Success"
    except:
        session.rollback()
        session.close()
        return "Error"


def get_all_connections():
    session = init()

    q = session.query(Connection).all()

    session.close()
    return q

def get_all_questions():
    """
    Gets all the questions from the database
    :param session: current session
    :return: dict of questions
    """

    session = init()

    questions = session.query(Question).all()

    session.close()

    return questions_to_json(questions)

def get_all_centers():
    """
    Get all centers from the database
    :return: list of centers
    """
    session = init()

    q = session.query(Entity).filter(Entity.type == "center").all()
    session.close()

    return q

def get_patient_scores_by_name( name):
    """
    Gives a list of all the questions answered by a patient as well as scores for each question
    :param session: current session
    :param name: parient name
    :return: list of scores
    """

    session = init()

    q = session.query(Entity.name, Question.label, Score.score).join(Score).join(Question).filter(Entity.type == "patient").filter(Entity.name == name).all()

    session.close()

    return q

def get_center_scores_by_name(name):
    """
    Gives a list of every question answered by the center as well as scores for each question
    :param session: current session
    :param name: name of center
    :return: list of scores
    """
    session = init()

    q = session.query(Entity.name, Question.label, Score.score).join(Score).join(Question).filter(Entity.type == "center").filter(Entity.name == name).all()

    session.close()

    return q

def get_all_center_scores():
    """
    Get all scores from all the centers
    :return: list of element: Center name, question value, score
    """
    session = init()

    q = session.query(Entity, Question, Score).join(Score).join(Question).filter(Entity.type == "center").all()

    session.close()

    return q

def get_all_questions_for_response_site_given_name(patient_name):
    """
    Find all the questions where a specific patient gave a score of 5 or higher
    :param patient_name: name of the patient
    :return: a list of all questions with the score 5 or higher
    """
    session = init()

    q = session.query(Question).join(Score).join(Entity).filter(Entity.name == patient_name).filter(Score.score > 5.0).all()

    questions = questions_to_json(q)
    centers = centers_to_json(get_all_centers())

    questions["centers"] = centers

    session.close()

    return questions

def get_all_entities():
    """
    Get a list of all entities
    :return: list of entities
    """

    session = init()

    q = session.query(Entity).all()

    session.close()

    return q


def question_to_dict(q):
    """
    Converts a question object to a dict
    :param q: current question
    :return: dict with question information
    """

    return {'id':q.id, 'label': q.label, 'value': q.value, 'info': q.info}

def questions_to_json(questions):
    """
    Converts a list of questions to json
    :param questions: questions to convert
    :return: json of dicts with questions
    """
    elements = []
    for q in questions:
        elements.append(question_to_dict(q))
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

#print(get_all_questions_for_response_site_given_name("to6ZVEjCEs"))
#session = init()
#insert_questions_from_json()
#fill_table()
#get_patient_scores_by_name( "Top Secret")
#get_center_scores_by_name( "Senter 1")
#set_new_question_score_for_center( "Senter 1", "spørsmål1")

#.filter(Entity.type == "center")

#print(random_string())
