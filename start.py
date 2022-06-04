import os, sys
from parsers.parse_teacher_sp import DataTeacherSp
from parsers.parse_teacher_mmsa import DataTeacherMmsa
from parsers.parse_teacher_schedule import DataTeacherSchedule
from models.models_db import DatabaseCreate
from utilities.develop_csv import DevelopAdditionalCSV
from utilities.develop_scientific_plan import DevelopScientificPlan
from config import Folders


def produce_parsers() -> None:
    """
    Function which is dedicated to create the csv values from the parsers
    Input:  None
    Output: we developed all possible values to the parsers
    """
    try:
        os.path.exists(Folders.folder_storage) or os.mkdir(Folders.folder_storage)
        for cls in [
            DataTeacherSp,
            DataTeacherMmsa,
            DevelopAdditionalCSV,
            DataTeacherSchedule,
            DevelopScientificPlan,
        ]:
            a = cls()
            a.start_parse()

    except Exception as e:
        exc_type, _, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(e)
        print('============================================================================')
        print(exc_type, fname, exc_tb.tb_lineno)
        print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')

def produce_database_creation() -> None:
    """
    Function which is dedicated to create the connection and basic values
    Input:  None
    Output: we created the database values to it
    """
    #TODO continue to work from here
    DatabaseCreate().develop_database()


if __name__ == '__main__':
    produce_parsers()
    produce_database_creation()