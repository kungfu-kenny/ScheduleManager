import os
from dotenv import load_dotenv

load_dotenv()

link_iasa_personal_sp = 'http://cad.kpi.ua/uk/kafedra/personal'
link_iasa_personal_mmsa = 'http://mmsa.kpi.ua/lecturers'

folder_csv = "csv_test"

class IasaSp:
    df_iasa_sp = 'csv_iasa_sp'
    status_iasa = 'Status'
    random_string = '234546y5u678597564534231y5y687647635'
    rechange_phrase = ["Рік, з якого працює на кафедрі СП", "Рік, з якого працює па кафедрі СП"]
    rechange_name = 'Name'
    rechange_work_begin = "Work begin"
    rechange_val, rechange_for = "Шалвівна", "Шавлівна"
    rechange_accomplishments = 'Accomplishments'
    rechange_special_status = 'Work Position'
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
                "Академічні звання": 'Academic recognition',
                "Почесні звання": "Accolodates",
                "Рік з якого працює на кафедрі СП": rechange_work_begin,
                "Викладає дисципліни": 'Disciplines',
                "Галузь наукової діяльності": "Scientific Directions",
                "Проводить лабораторно практичні заняття з дисциплін": "Practical Disciplines",
                "Загальна кількість публікацій": "Publications Information"}


# class RozkladKPI:
