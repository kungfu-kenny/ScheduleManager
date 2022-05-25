import os
from dotenv import load_dotenv


load_dotenv()

class Folders:
    folder_here = os.getcwd()
    folder_storage = os.path.join(
        folder_here,
        'storage'
    )

class Keys:
    id = 'ID'
    id_spectre = 'ID_spectre'
    id_teacher = 'ID_teacher'
    id_subject = 'ID_subject'
    id_spec = 'ID_specialization'
    birthplace = "Birthplace"
    birthdate = "Birthdate"
    education = "Education"
    accolodates_scientific = "Accolodates Scientific"
    accolodates_academic = "Accolodates Academic"
    accolodates_honor = "Accolodates Honor"
    year = "Year Working"
    subject_theory = "Subject Theory"
    subject_practice = "Subject Practice"
    science_spectre = "Science Spectre"
    publications = "Publications"
    tasks = "Tasks"
    name = "Name"
    link = "Link"
    chair = 'Chair'
    spectre = "Spectre"
    subject = 'Subject'
    specialization = "Specialization"

class IasaMMSA:
    thread = 15
    df_name = 'teachers_mmsa.csv'
    link_start = 'http://mmsa.kpi.ua/lecturers'
    rechange_list = [
        Keys.name,
        Keys.link, 
        Keys.accolodates_scientific,
        Keys.accolodates_academic,
        Keys.tasks,
        Keys.subject_theory,
        Keys.science_spectre,
        Keys.publications,
        Keys.subject_practice,
    ] 

class IasaSP:
    df_name = 'teachers_sp.csv'
    link_start = 'https://cad.kpi.ua/about-us/teachers/'
    link_download_xls = 'http://cad.kpi.ua/wp-content/uploads/2022/01/расп2сем1-5курс21-22СП.xls'
    sep = 'ghrfbnikjfghdjubikvxtrcsfeslkrdaijuwzhXC:Ogfhdyzrcjukvx ehgjkybudfzxcrl'
    specialization = 'Інтелектуальні сервiс-орiєнтованi розподілені обчислювання'
    disp_theory, disp_practice = "Викладає дисципліни:", "Проводить лабораторно-практичні заняття з дисциплін:"
    list_ul = [disp_theory, disp_practice]
    rechange_keys = {
        "Дата народження:": Keys.birthdate,
        "Місце народження:": Keys.birthplace,
        "Освіта:": Keys.education,
        "Вчений ступінь і звання:": Keys.accolodates_scientific,
        "Академічні звання:": Keys.accolodates_academic,
        "Почесні звання:": Keys.accolodates_honor,
        "Рік з якого працює на кафедрі СП:": Keys.year,
        disp_theory: Keys.subject_theory,
        disp_practice: Keys.subject_practice,
        "Галузь наукової діяльності:": Keys.science_spectre,
        "Загальна кількість публікацій:": Keys.publications,
        "Задачі та напрямки діяльності:": Keys.tasks,
        "122131242455657632537845365334212423214234234`123": Keys.name,
        "rtghfyyjtruhgfbnngbmtuhjfky iukgtyihjmnhyuitgkjlmn,o": Keys.link,
    }

class IasaAdditional:
    df_name_specialization = 'teachers_specialization.csv'
    df_name_subject = 'teachers_subject.csv'
    df_name_spectre = 'teachers_spectre.csv'
    df_name_teacher = 'teachers_all.csv'
    df_name_teacher_subject = 'teachers_foreign_subject.csv'
    df_name_teacher_spectre = 'teachers_foreign_spectre.csv'
    df_name_teacher_specialization = 'teachers_foreign_specialization.csv'