import os
from parsers.parse_teacher_sp import DataTeacherSp
from parsers.parse_teacher_mmsa import DataTeacherMmsa
from config import Folders


# try:
os.path.exists(Folders.folder_storage) or os.mkdir(Folders.folder_storage)
for cls in [
    DataTeacherSp,
    DataTeacherMmsa,
]:
    a = cls()
    a.start_parse()

# except Exception as e:
#     print(e)
#     print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')