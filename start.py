import os, sys
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
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)
    print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')