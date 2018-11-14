from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Entity(Base):
    __tablename__ = 'entity'
    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    name = Column(String, nullable=False)

class Patient(Base):
    __tablename__ = 'patient'
    id = Column(Integer, ForeignKey('entity.id'), primary_key=True)
    date_of_birth = Column(String, nullable=False)
    entity = relationship(Entity)

class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    street_name = Column(String(250))
    street_number = Column(Integer)
    post_code = Column(Integer, nullable=False)
    entity_id = Column(Integer, ForeignKey('entity.id'))
    entity = relationship(Entity)

class Center(Base):
    __tablename__ = 'center'
    id = Column(Integer, ForeignKey('entity.id'), primary_key=True)
    phone_number = Column(Integer, nullable=False)
    entity = relationship(Entity)

class Question(Base):
    __tablename__ = 'question'
    id = Column(Integer, primary_key=True)
    label = Column(String, nullable=False)
    value = Column(String, nullable=False)
    info = Column(String, nullable=False)

class Score(Base):
    __tablename__ = 'score'
    patient_id = Column(Integer, ForeignKey('entity.id'), primary_key=True)
    question_id = Column(Integer, ForeignKey('question.id'), primary_key=True)
    score = Column(Float)
    entity = relationship(Entity)
    question = relationship(Question)


# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///valgomat.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)