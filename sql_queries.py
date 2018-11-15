from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Address, Base, Patient, Question, Score, Entity, Center, Response

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

def fill_table(session):

    new_entity = Entity(type="center", name="Senter 1")
    new_center = Center(contact_person = "mail@address.com", phone_number=12345678, entity=new_entity)
    new_address = Address(street_name="testname", street_number=51, post_code=1236, entity=new_entity)
    new_question = Question(label="Spørsmål 1", value="spørsmål1", info="Mer info")
    new_Score = Score(score=50.0, entity=new_entity, question=new_question)

    new_entity2 = Entity(type="patient", name="Top Secret")
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

def insert_question(label, value, info, score, session):

    new_question = Question(label=label, value=value, info=info, score=score)
    session.add(new_question)
    session.commit()


def insert_patient_answers(session):

    new_patient = Patient(code="1234",date_of_birth="11.11.11")
    session.add(new_patient)

    new_address = Address(street_name="gatenavn", street_number=101, post_code="1337", patient=new_patient)
    session.add(new_address)

    q = session.query(Question).first()

    new_score = Score(patient=new_patient, question=q, score=10.0)
    session.add(new_score)

    session.commit()

def set_new_question_score_for_center(session, name, question):

    center_id = session.query(Entity.id).filter(Entity.name == name).first()
    question_id = session.query(Question.id).filter(Question.value == question).first()

    session.query(Score).filter(Score.entity_id == center_id[0]).filter(Score.question_id == question_id[0]).update({"score": 67.0})
    session.commit()

def get_first_question(session):

   question = session.query(Question).first()
   return question_to_dict(question)


def get_all_questions(session):

    questions = session.query(Question).all()
    elements = []
    for q in questions:
        elements.append(question_to_dict(q))
    response = {'questions': elements}
    return response

def get_patient_scores_by_name(session, name):

    q = session.query(Entity.name, Question.label, Score.score).join(Score).join(Question).filter(Entity.type == "patient").filter(Entity.name == name).all()

    print(q)

def get_center_scores_by_name(session, name):

    q = session.query(Entity.name, Question.label, Score.score).join(Score).join(Question).filter(Entity.type == "center").filter(Entity.name == name).all()

    print(q)

def question_to_dict(q):

    return {'id':q.id, 'label': q.label, 'value': q.value, 'info': q.info}


session = init()
fill_table(session)
get_patient_scores_by_name(session, "Top Secret")
get_center_scores_by_name(session, "Senter 1")
set_new_question_score_for_center(session, "Senter 1", "spørsmål1")

#.filter(Entity.type == "center")