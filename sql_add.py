from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Address, Base, Patient, Question, Score, Entity, Center

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
    new_entity = Entity(type="center", name="Such Hidden")
    new_patient = Patient(date_of_birth = "10.10.10", entity=new_entity)
    new_address = Address(street_name="testname", street_number=51, post_code=1236, entity=new_entity)
    new_question = Question(label="Spørsmål 1", value="spørsmål1", info="Mer info")
    new_Score = Score(score=50.0, entity=new_entity, question=new_question)

    new_entity2 = Entity(type="patient", name="Top Secret")
    new_patient2 = Patient(date_of_birth = "03.04.05", entity=new_entity2)
    new_address2 = Address(street_name="sesame street", street_number=2, post_code=9999, entity=new_entity2)
    new_question2 = Question(label="Spørsmål 2", value="spørsmål2", info="Enda mer info")
    new_Score2 = Score(score=76.0, entity=new_entity2, question=new_question2)
    new_Score3 = Score(score=10.0, entity= new_entity, question=new_question2)

    session.add(new_entity)
    session.add(new_patient)
    session.add(new_address)
    session.add(new_question)
    session.add(new_Score)

    session.add(new_entity2)
    session.add(new_patient2)
    session.add(new_address2)
    session.add(new_question2)
    session.add(new_Score2)
    session.add(new_Score3)

    session.commit()

def add_question(label, value, info, score, session):

    new_question = Question(label=label, value=value, info=info, score=score)
    session.add(new_question)
    session.commit()


def add_patient_answers(session):
    new_patient = Patient(code="1234",date_of_birth="11.11.11")
    session.add(new_patient)

    new_address = Address(street_name="gatenavn", street_number=101, post_code="1337", patient=new_patient)
    session.add(new_address)

    q = session.query(Question).first()

    new_score = Score(patient=new_patient, question=q, score=10.0)
    session.add(new_score)

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


def question_to_dict(q):
    return {'id':q.id, 'label': q.label, 'value': q.value, 'info': q.info}


def print_tables(q):
    for (entity, score, address, question) in q:
        print("Name: %s" % entity.name,
              "\nType: %s" % entity.type,
              "\nAddress: %s" % address.street_name ,
              "\nQuestion: %s" % question.label,
              "\nScore: %s" % score.score)
        print()


session = init()
#fill_table(session)

q = (session.query(Entity, Score, Address, Question).join(Score).join(Address).join(Question).filter(Entity.type == "center").all())
#print(q[1].Entity.id)
print_tables(q)
#print(q.Entity.name, q.Entity.type, q.Patient.date_of_birth)
