from datetime import datetime
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    create_engine,
    Table,
    Column,
    Boolean,
    Integer,
    String,
    DateTime,
    ForeignKey,
    PrimaryKeyConstraint,
)
from config import (
    Keys, 
    DataBasePostgre, 
    IasaAdditional,
)


Base = declarative_base()

association_faculty_chair = Table(
    "faculty_chair",
    Base.metadata,
    Column("id_faculty", ForeignKey("faculty.id")),
    Column("id_chair", ForeignKey("chair.id")),
    PrimaryKeyConstraint("id_faculty", "id_chair"),
)

association_faculty_building = Table(
    "faculty_building",
    Base.metadata,
    Column("id_faculty", ForeignKey("faculty.id")),
    Column("id_building", ForeignKey("building.id")),
    PrimaryKeyConstraint("id_faculty", "id_building"),
)

association_teacher_science_spectre = Table(
    "teacher_science_spectre",
    Base.metadata,
    Column("id_teacher", ForeignKey("teacher.id")),
    Column("id_science_spectre", ForeignKey("science_spectre.id")),
    PrimaryKeyConstraint("id_teacher", "id_science_spectre"),
)

association_teacher_subject = Table(
    "teacher_subject",
    Base.metadata,
    Column("id_teacher", ForeignKey("teacher.id")),
    Column("id_subject", ForeignKey("subject.id")),
    PrimaryKeyConstraint("id_teacher", "id_subject"),
)

association_teacher_specialization = Table(
    "teacher_specialization",
    Base.metadata,
    Column("id_teacher", ForeignKey("teacher.id")),
    Column("id_specialization", ForeignKey("specialization.id")),
    PrimaryKeyConstraint("id_teacher", "id_specialization"),
)

association_teacher_subject_specialization = Table(
    "teacher_subject_specialization",
    Base.metadata,
    Column("id_teacher", ForeignKey('teacher.id')),
    Column("id_subject", ForeignKey("subject.id")),
    Column("id_specialization", ForeignKey("specialization.id")),
    Column("hours_used", Integer, default=40),
    Column("semester_start", Integer, default=1),
    Column("allow_split", Boolean, default=True),
    Column("masters", Boolean, default=True),
    Column('date_inserted', DateTime, default=datetime.now()),
    PrimaryKeyConstraint("id_teacher", "id_subject", "id_specialization"),
)

association_teacher_class_dedicated = Table(
    "teacher_class_dedicated",
    Base.metadata,
    Column("id_teacher", ForeignKey('teacher.id')),
    Column("id_class", ForeignKey('class.id')),
    Column("id_building", ForeignKey('building.id')),
    PrimaryKeyConstraint("id_teacher", "id_class", "id_building")
)

class Chair(Base):
    __tablename__ = 'chair'
    id = Column(Integer, primary_key=True)
    name = Column(String, default='')
    abbreviation = Column(String, default='')
    faculty = relationship(
        "Faculty", 
        secondary=association_faculty_chair, 
        back_populates="chair"
    )

class Faculty(Base):
    __tablename__ = 'faculty'
    id = Column(Integer, primary_key=True)
    name = Column(String, default='')
    abbreviation = Column(String, default='')
    chair = relationship(
        "Chair", 
        secondary=association_faculty_chair, 
        back_populates="faculty"
    )
    building = relationship(
        "Building", 
        secondary=association_faculty_building, 
        back_populates="faculty"
    )

class Day(Base):
    __tablename__ = 'day'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))

class TimeStart(Base):
    __tablename__ = 'time_start'
    id = Column(Integer, primary_key=True)
    time = Column(String, default='')

class Group(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True)
    name = Column(String(150))
    year_started = Column(Integer, default=datetime.now().year)
    chair = Column(Integer, ForeignKey('chair.id'))
    faculty = Column(Integer, ForeignKey('faculty.id'))
    specialization = Column(Integer, ForeignKey('specialization.id'))
    building_default = Column(Integer, ForeignKey('building.id'))

class Teacher(Base):
    __tablename__ = 'teacher'
    id = Column(Integer, primary_key=True)
    name = Column(String(150))
    link = Column(String(100))
    birthdate = Column(String(50), default='')
    birthplace = Column(String(200), default='')
    education = Column(String, default='')
    year_working = Column(String, default='')
    accolodates_scientific = Column(String, default='')
    accolodates_academic = Column(String, default='')
    accolodates_honor = Column(String, default='')
    tasks = Column(String, default='')
    chair_id = Column(Integer, ForeignKey("chair.id"))
    faculty_id = Column(Integer, ForeignKey("faculty.id"))
    specialization = relationship(
        "Specialization", 
        secondary=association_teacher_specialization, 
        back_populates="teacher"
    )
    subject = relationship(
        "Subject", 
        secondary=association_teacher_subject, 
        back_populates="teacher"
    )
    science_spectre = relationship(
        "ScienceSpectre", 
        secondary=association_teacher_science_spectre, 
        back_populates="teacher"
    )

class Class(Base):
    __tablename__ = 'class'
    id = Column(Integer, primary_key=True)
    number = Column(Integer, default=1)
    floor = Column(Integer, default=1)
    size = Column(Integer, default=1)
    building_id = Column(Integer, ForeignKey('building.id'))

class Building(Base):
    __tablename__ = 'building'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    floors = Column(Integer, default=1)
    address = Column(String, nullable=False)
    lattitude = Column(String)
    longitude = Column(String)
    faculty = relationship(
        "Faculty", 
        secondary=association_faculty_building, 
        back_populates="building"
    )

class ScienceSpectre(Base):
    __tablename__ = 'science_spectre'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    teacher = relationship(
        "Teacher", 
        secondary=association_teacher_science_spectre, 
        back_populates="science_spectre"
    )

class Subject(Base):
    __tablename__ = 'subject'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    teacher = relationship(
        "Teacher", 
        secondary=association_teacher_subject, 
        back_populates="subject"
    )

class Specialization(Base):
    __tablename__ = 'specialization'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    chair_id = Column(Integer, ForeignKey('chair.id'))
    teacher = relationship(
        "Teacher", 
        secondary=association_teacher_specialization, 
        back_populates="specialization"
    )


class DatabaseCreate:
    """
    Class which is dedicated to develop the creation of the database
    """
    def __init__(self) -> None:
        self.engine = create_engine(
            f'postgresql://{DataBasePostgre.data}:{DataBasePostgre.pawd}'\
            f'@{DataBasePostgre.host}:{DataBasePostgre.port}/{DataBasePostgre.user}'
        )
        self.create_db()
        self.session = self.produce_session()

    def create_db(self):
        """
        Method which is dedicated to create databse values of this
        Input:  None
        Output: we created the selected values for the database values
        """
        try:
            Base.metadata.create_all(self.engine)
        except Exception as e:
            print(f"We faced problems with Base: {e}")

    def produce_session(self) -> object:
        """
        Method which is dedicated to create the session values for the database
        Input:  None
        Output: we create session for creation
        """
        Session = sessionmaker(bind=self.engine)
        return Session()

    @staticmethod
    def develop_group() -> None:
        """
        
        """
        #TODO continue to add checkings and give 
        pass



    def develop_database(self) -> None:
        """
        Method which is dedicated to develop database values 
        Input:  None
        Output: we created the database values
        """
        #TODO continue work from here
        self.develop_group()