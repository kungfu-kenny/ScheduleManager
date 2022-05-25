from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (create_engine,
                        Table,
                        Column,
                        Integer,
                        String,
                        ForeignKey,
                        PrimaryKeyConstraint)


Base = declarative_base()

class Teacher(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(150))
    link = Column(String(100))
    birthdate = Column(String(50))
    birthplace = Column(String(200))
    #TODO continue work from here