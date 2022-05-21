import os
from parsers.parse_teacher_sp import DataTeacherSp


try:
    a = DataTeacherSp()
    a.start_parse()

except Exception as e:
    print(e)
    print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')