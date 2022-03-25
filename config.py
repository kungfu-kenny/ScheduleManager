import os
from dotenv import load_dotenv

load_dotenv()

link_iasa_personal_sp = 'https://cad.kpi.ua/about-us/teachers/'
link_iasa_personal_mmsa = 'http://mmsa.kpi.ua/lecturers'

folder_csv = "csv_test"
status = 'Status'
name = 'Name'
photo = 'Photo'
email = 'Email'
link = 'Link'

disciplines = 'Disciplines'
disciplines_practice = "Practical Disciplines"
accomplihments = 'Accomplishments'
special_status = 'Work Position'
academic_recodnition = 'Academic recognition'
accolodates = "Accolodates"
scientific_directions = "Scientific Directions"
publications_information = "Publications Information"

class IasaSp:
    df_iasa_sp = 'csv_iasa_sp'
    status_iasa = status
    random_string = '234546y5u678597564534231y5y687647635'
    rechange_phrase = ["Рік, з якого працює на кафедрі СП", "Рік, з якого працює па кафедрі СП"]
    rechange_name = name
    rechange_work_begin = "Work begin"
    rechange_disciplines = disciplines
    rechange_disciplines_practice = disciplines_practice
    rechange_list_into = [rechange_disciplines, rechange_disciplines_practice]
    rechange_sub_sep = ', '
    rechange_dict_values = {f"Об’єктно{rechange_sub_sep}орієнтоване": "Об'єктно-орієнтоване",
                            f"Грід{rechange_sub_sep}технології": "Грід-технології"}
    rechange_val, rechange_for = "Шалвівна", "Шавлівна"
    rechange_accomplishments = accomplihments
    rechange_special_status = special_status
    rechange_birthplace = "Birthplace"
    rechange_glitch_22 = "Вчений ступінь"
    rechange_iasa = {'Дата народження':"Birthday",
                "Місце народження": rechange_birthplace,
                "Освіта":"Education",
                status_iasa: status_iasa, 
                rechange_phrase[0]: rechange_work_begin,
                rechange_phrase[1]: rechange_work_begin,
                "Вчений ступінь і звання": rechange_accomplishments,
                rechange_glitch_22: rechange_accomplishments,
                "Академічні звання": academic_recodnition,
                "Почесні звання": accolodates,
                "Рік з якого працює на кафедрі СП": rechange_work_begin,
                "Викладає дисципліни": rechange_disciplines,
                "Галузь наукової діяльності": scientific_directions,
                "Проводить лабораторно практичні заняття з дисциплін": rechange_disciplines_practice,
                "Загальна кількість публікацій": publications_information}

class IasaMmsa:
    df_iasa_mmsa = 'csv_iasa_mmsa'
    status_iasa = status
    rechange_link = link
    rechange_photo = photo
    rechange_email = email
    rechange_location = 'Location'
    rechange_name = name
    rechange_disciplines = disciplines
    rechange_disciplines_practice = disciplines_practice
    rechange_accomplishments = accomplihments
    rechange_special_status = special_status


# class RozkladKPI:
