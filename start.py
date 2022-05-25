import os
from parsers.parse_teacher_sp import DataTeacherSp
from parsers.parse_teacher_mmsa import DataTeacherMmsa
from utilities.develop_csv import DevelopAdditionalCSV
from config import Folders


try:
    os.path.exists(Folders.folder_storage) or os.mkdir(Folders.folder_storage)
    for cls in [
        DataTeacherSp,
        DataTeacherMmsa,
        DevelopAdditionalCSV,
    ]:
        a = cls()
        a.start_parse()

except Exception as e:
    #TODO add here the exception workers
    print(e)
    print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')