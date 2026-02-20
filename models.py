from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Professor(Base):
    __tablename__ = "professors"

    pid = Column(Integer, primary_key=True, index=True)
    pname = Column(String, index=True)
    age = Column(Integer)
    course = Column(String)


    students = relationship("Student", back_populates="professor")


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    course = Column(String)
    professor_id = Column(Integer, ForeignKey("professors.pid"))
    professor = relationship("Professor", back_populates="students")