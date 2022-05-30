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
    id_chair = 'ID_chair'
    id_faculty = 'ID_faculty'
    id_spectre = 'ID_spectre'
    id_teacher = 'ID_teacher'
    id_subject = 'ID_subject'
    id_spec = 'ID_specialization'
    birthplace = "Birthplace"
    birthdate = "Birthdate"
    education = "Education"
    accolodates_scientific = "Accolodates_Scientific"
    accolodates_academic = "Accolodates_Academic"
    accolodates_honor = "Accolodates_Honor"
    year = "Year_Working"
    subject_theory = "Subject_Theory"
    subject_practice = "Subject_Practice"
    science_spectre = "Science_Spectre"
    publications = "Publications"
    tasks = "Tasks"
    name = "Name"
    link = "Link"
    chair = 'Chair'
    spectre = "Spectre"
    subject = 'Subject'
    abbreviation = 'Abbreviation'
    specialization = "Specialization"
    name_subject_small = "Name_Subject_Small"
    name_teacher = 'Name_Teacher'
    subject_type = "Subject_Type"
    groups_list = "Groups_List"
    name_teacher_searched = "Name_Teacher_Searched"
    time_begin = "Time_Begin"
    number_count = "Number_Count"
    day_begin = "Day_Begin"
    week_number = "Week_Number"

class IasaFaculty:
    abbreviation = 'ІПСА'
    name = 'Інститут Прикладного Системного Аналізу'
    name_sp, name_mmsa = 'SP', 'MMSA'
    dict_name = {
        name_sp: "СП",
        name_mmsa: "ММСА",
    }
    dict_id = {
        name_sp: 1,
        name_mmsa: 2,
    }
    dict_df = {
        Keys.id: [1, 2],
        Keys.name: ["Системне Проєктування", "Математичні Методи Системного Аналізу"],
        Keys.abbreviation:["СП", "ММСА"]
    }

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

class IasaSchedule:
    link = 'http://rozklad.kpi.ua/Schedules/LecturerSelection.aspx'
    key_name = "ctl00$MainContent$txtboxLecturer"
    data = {
        "ctl00_ToolkitScriptManager_HiddenField": "",
        "__EVENTTARGET": "",
        "__EVENTARGUMENT":	"",
        "ctl00$MainContent$btnSchedule": "Розклад занять",
        "hiddenInputToUpdateATBuffer_CommonToolkitScripts":	"1",
        "__VIEWSTATE":	"/wEMDAwQAgAADgEMBQAMEAIAAA4BDAUDDBACAAAOAgwFCwwQAgw"\
            "PAgEIQ3NzQ2xhc3MBD2J0biBidG4tcHJpbWFyeQEEXyFTQgUCAAAADAUNDBACAAAOA"\
            "QwFAwwQAgwADwEBB29uZm9jdXMBHXRoaXMudmFsdWU9Jyc7dGhpcy5vbmZvY3VzPScn"\
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"\
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"\
            "AAAAAAAAAAAAAAAAAAAAAJkWCFbMSgxOXJsGpLI9ZU2imYY",
        "__EVENTVALIDATION": "/wEdAAEAAAD/////AQAAAAAAAAAPAQAAAAUAAAAIsA3rWl3AM+6E94I53LbWK4YqVqwL"\
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"\
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"\
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"\
            "AAAAAACvHV09VRintN+nMH+p4yerPBpN+",
    }

class IasaAdditional:
    df_name_chair = "teachers_chair.csv"
    df_name_faculty = 'teachers_faculty.csv'
    df_name_specialization = 'teachers_specialization.csv'
    df_name_subject = 'teachers_subject.csv'
    df_name_spectre = 'teachers_spectre.csv'
    df_name_schedule = 'teachers_schedule.json'
    df_name_teacher = 'teachers_all.csv'
    df_name_teacher_subject = 'teachers_foreign_subject.csv'
    df_name_teacher_spectre = 'teachers_foreign_spectre.csv'
    df_name_teacher_specialization = 'teachers_foreign_specialization.csv'
    df_name_faculty_chair = 'teachers_foreign_faculty_chair.csv'