import os
import asyncio
import pandas as pd
from bs4 import BeautifulSoup, element
from parsers.parse_teacher import ParseTeachers
from utilities.develop_csv import DevelopAdditionalCSV
from config import (
    Keys,
    Folders,
    IasaSP,
    IasaMMSA,
    IasaAdditional,
)


class DataTeacherSchedule(ParseTeachers):
    """
    class which is dedicated to parse selected teacher's schedule
    """
    def __init__(self) -> None:
        super(DataTeacherSchedule, self).__init__()
        self.file_csv = os.path.join(
            Folders.folder_storage,
            IasaAdditional.df_name_schedule
        )

    @staticmethod
    def check_additional() -> None:
        """
        Static method which is dedicated to additionally checked the previous data
        Input:  None
        Output: we created the previous values in this cases
        """
        additional_csv = DevelopAdditionalCSV()
        additional_csv.check_additional(
            set(
                [IasaSP.df_name, IasaMMSA.df_name]
            ).issubset(os.listdir(Folders.folder_storage))
        )
        additional_csv.parse_workers()

    @staticmethod
    def parse_table_days(table:element) -> dict:
        """
        Static method which is dedicated to created the
        Input:  table = selected table values 
        Output: dictionary which the selected values and the
        """
        if not table:
            return {}
        days = table.find_all('tr')
        days = days[0] if len(days) > 0 else []
        days = [f.text for f in days.find_all('td')]
        return {
            day: days.index(day)
            for day in days
            if day
        }

    @staticmethod
    def parse_table_time(table:element) -> dict:
        """
        Static method which is dedicated to parse time
        Input:  table = selected table values
        Output: disctionary of the selected values
        """
        if not table:
            return {}
        times = table.find_all('tr')
        times = times[1:] if len(times) > 0 else []
        times = [
            f.find('td').get_text(strip=True, separator='\n').splitlines() for f in times
        ]
        return {
            time: i + 1
            for i, (_, time) in enumerate(times)
        }

    @staticmethod
    def parse_table_subject(table:element) -> list:
        """
        Static method which is dedicated to parse table subject
        Input:  table = table which was previously parsed
        Output: we developed the subjects list of selected values
        """
        if not table:
            return []
        subjects = table.find_all('tr')
        subjects = subjects[1:] if len(subjects) > 0 else []
        subjects = [
            [j.get_text(strip=True, separator='\n').splitlines() for j in f.find_all('td')[1:]]
            for f in subjects
        ]
        value_return = []
        for day in [*zip(*subjects)]:
            ret = []
            for subject in day:
                if subject and len(subject) == 4:
                    name, person, lec_type, groups = subject
                    groups = groups.split(', ')
                elif subject and len(subject) == 3:
                    name, person, groups = subject
                    lec_type = ''
                    groups = groups.split(', ')
                else:
                    name, person, lec_type, groups = '', '', '', []
                ret.append(
                    {
                        Keys.name_subject_small: name,
                        Keys.name_teacher: person,
                        Keys.subject_type: lec_type,
                        Keys.groups_list: groups,
                    }
                )
            value_return.append(ret)
        return value_return

    @staticmethod
    def parse_table_all(days:dict, times:dict, subjects:dict, name:str, header:str) -> list:
        """
        Static method which is dedicated to develop values of the all values
        Input:  days = dictionary of the selected days
                times = dict of the time values
                subjects = list of the subject values 
                name = string of the selected name
                header = week quarter
        Output: list with the selected values
        """
        value_ret = []
        for subject, day in zip(
            subjects, 
            {k: v for k, v in sorted(days.items(), key=lambda item: item[1])}.keys()
        ):
            for sub, (t, c) in zip(
                subject,
                {k: v for k, v in sorted(times.items(), key=lambda item: item[1])}.items()
                ):
                sub.update({
                    Keys.name_teacher_searched: name,
                    Keys.time_begin: t,
                    Keys.number_count: c,
                    Keys.day_begin: day,
                    Keys.week_number: header,
                })
                value_ret.append(sub)
        return value_ret
    
    def start_parse_html(self) -> list:
        """
        Method which is dedicated to develop the getting the values of the html selected values
        Input:  None
        Output: we created list of the parsed html values
        """
        value_name = pd.read_csv(
            os.path.join(
                Folders.folder_storage, 
                IasaAdditional.df_name_teacher
            )
        )
        value_name = value_name[Keys.name].to_list()#[:]
        
        loop = asyncio.get_event_loop()
        list_html = loop.run_until_complete(
            self.get_html_all_schedule(
                value_name
            )
        )
        
        value_result = []
        for name, html in zip(value_name, list_html):
            soup = BeautifulSoup(html, 'html.parser')
            header_first = self.get_text(
                soup.find(
                    'span', 
                    {"id":"ctl00_MainContent_lblFirstTable"}
                )
            )
            table_first = soup.find(
                'table',
                {"id":"ctl00_MainContent_FirstScheduleTable"}
            )
            
            header_second = self.get_text(
                soup.find(
                    'span', 
                    {'id': 'ctl00_MainContent_lblSecondTable'}
                )
            )
            table_second = soup.find(
                'table',
                {"id":"ctl00_MainContent_SecondScheduleTable"}
            )

            dict_days_first = self.parse_table_days(table_first)
            dict_numbers_first = self.parse_table_time(table_first)
            list_schedule_first = self.parse_table_subject(table_first)
            dict_schedule_first = self.parse_table_all(
                dict_days_first,
                dict_numbers_first, 
                list_schedule_first,
                name,
                header_first
            )
            
            dict_days_second = self.parse_table_days(table_second)
            dict_numbers_second = self.parse_table_time(table_second)
            list_schedule_second = self.parse_table_subject(table_second)
            dict_schedule_second = self.parse_table_all(
                dict_days_second,
                dict_numbers_second, 
                list_schedule_second,
                name,
                header_second
            )

            value_result.extend(dict_schedule_first)
            value_result.extend(dict_schedule_second)

        return value_result

    def start_parse(self) -> None:
        """
        Method which is dedicated to develop the parse all values of it
        Input:  None
        Output: we parsed the values of the selected values
        """
        if self.get_check_development(self.file_csv):
            return
        self.check_additional()
        dictionary_used = self.start_parse_html()
        self.save_json(
            dictionary_used,
            self.file_csv
        )