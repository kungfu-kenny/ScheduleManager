import os
from parsers.parse_teacher_sp import DataTeacherSp
from config import Folders


try:
    os.path.exists(Folders.folder_storage) or os.mkdir(Folders.folder_storage)
    a = DataTeacherSp()
    a.start_parse()

except Exception as e:
    print(e)
    print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')