import os
import asyncio
import pandas as pd
from bs4 import BeautifulSoup, element
from parsers.parse_teacher import ParseTeachers
from config import (
    Keys,
    Folders, 
    IasaMMSA, 
)


class DataTeacherMmsa(ParseTeachers):
    """
    class which is dedicated to start parsing another branch of the iasa teachers
    """
    def __init__(self) -> None:
        super(DataTeacherMmsa, self).__init__()
        self.file_csv = os.path.join(
            Folders.folder_storage,
            IasaMMSA.df_name
        )

    def configure_subjects_lections(self, value_parsed:element.Tag) -> list:
        """
        Method which is dedicated to return subjects which are lectures to selected specialization
        Input:  value_parsed = parsed previously value
        Output: list with format [specialization, subject]
        """
        value_subjects = value_parsed.find('div', {'id':'block-views-discipline-by-lecturer-block'})
        if value_subjects:
            value_subjects = value_subjects.find(class_='view-discipline-by-lecturer')
            value_subjects = value_subjects.find('table')
            value_subjects = value_subjects.find_all('tr')
            value_subjects = [v.find_all('td') for v in value_subjects]
            value_subjects = [v for v in value_subjects if v]
            value_subjects = [[k.text.replace('\n', '').strip() for k in v] for v in value_subjects]
            return '|'.join(f"{subject[1]}[{subject[0]}]" for subject in value_subjects)
        return ''

    def configure_scientific_directions(self, value_parsed:element.Tag) -> list:
        """
        Method which is dedicated to return scientific directions of the lecturer
        Input:  value_parsed = parsed previously page
        Output: list of the 
        """
        value_scientific_directions = value_parsed.find('div', {'id':'block-views-a8d2aa34f6c1a0321bd21a41ba6252d5'})
        if value_scientific_directions:
            value_scientific_directions = value_scientific_directions.find(class_='view-research-areas-by-lecturer')
            value_scientific_directions = value_scientific_directions.find('table')
            value_scientific_directions = value_scientific_directions.find_all('tr')
            value_scientific_directions = [v.find_all('td') for v in value_scientific_directions]
            value_scientific_directions = [v for v in value_scientific_directions if v]
            value_scientific_directions = [
                [k.text.replace('\n', '').strip() for k in v] 
                for v in value_scientific_directions
            ]
            return '|'.join(f"{subject[1]}[{subject[0]}]" for subject in value_scientific_directions)
        return ''

    def configure_publications_info(self, value_parsed:element.Tag) -> list:
        """
        Method which is dedicated to return information about the 
        Input:  value_parsed = parsed previously value
        Output: list with format of the publications
        """
        value_publications_info = value_parsed.find('div', {'id':'block-views-publications-by-lecturer-block'})
        if value_publications_info:
            value_publications_info = value_publications_info.find(class_='view-id-publications_by_lecturer')
            value_publications_info = [v.strip() for v in value_publications_info.text.split('\n')]
            return '|'.join(v for v in value_publications_info if v)
        return ''

    def configure_subjects_practice(self, value_parsed:element.Tag) -> list:
        """
        Method which is dedicated to return subjects which are practices to selected specialization
        Input:  value_parsed = parsed previously value
        Output: list with format [specialization, subject]
        """
        value_subjects = value_parsed.find('div', {'id': 'block-views-discipline-by-lecturer-block-1'})
        if value_subjects:
            value_subjects = value_subjects.find(class_='view-discipline-by-lecturer')
            value_subjects = value_subjects.find('table')
            value_subjects = value_subjects.find_all('tr')
            value_subjects = [v.find_all('td') for v in value_subjects]
            value_subjects = [
                [k.text.replace('\n', '').strip() for k in v] 
                for v in [v for v in value_subjects if v]
            ]
            return '|'.join(f"{subject[1]}[{subject[0]}]" for subject in value_subjects)
        return ''

    @staticmethod
    def configure_status(value_parsed:element.Tag) -> str:
        """
        Static method which is dedicated to parse status on a cafdra status
        of a worker
        Input:  value_parsed = value which was prveiously used
        Output: status of the teacher
        """
        return ', '.join(
            f.text for f in [
                value_parsed.find(class_='field-name-field-s-person-faculty-type'),
                value_parsed.find(class_='field-name-field-degree')
            ] if f
        )

    @staticmethod
    def configure_accolodates(value_parsed:element.Tag) -> str:
        """
        Static method is about to return biography from some of them
        Input:  value_parsed = previously parsed values
        Output: text about the person
        """
        value_accolodates = value_parsed.find(class_='field-type-text-with-summary')
        return value_accolodates.text if value_accolodates else ''

    @staticmethod
    def configure_work_position(value_parsed:element.Tag) -> str:
        """
        Static method which is dedicated to parse work position of the person inside the faculty
        Input:  value_parsed = previously parsed values
        Output: teext about the work position
        """
        value_work_position = value_parsed.find(class_='field-name-field-s-person-staff-type')
        return value_work_position.text if value_work_position else ''
        
    def start_parse_html(self) -> list:
        """
        Method which is dedicated to parse selected values
        """
        soup = BeautifulSoup(
            self.get_html_sync(IasaMMSA.link_start), 
            'html.parser'
        )
        soup = soup.find('div', {"class": "view-content"})
        list_teachers = [
            f"http://mmsa.kpi.ua{f.get('href', '')}" if f.get('href', '') else ''
            for f in soup.find_all('a')
        ]
        loop = asyncio.get_event_loop()
        list_html = loop.run_until_complete(
            self.get_html_all(
                list_teachers[:]#50]
            )
        )
        value_return = []
        for html, link in zip(list_html, list_teachers):
            soup = BeautifulSoup(html, 'html.parser')
            value_parsed_info = soup.find(class_='group-header mmsa-column12')
            value_return.append(
                {
                    Keys.name: soup.find('h1', {"class":"mmsa-sub-title"}).text,
                    Keys.link: link,
                    Keys.accolodates_scientific: self.configure_status(value_parsed_info),
                    Keys.accolodates_academic: self.configure_accolodates(value_parsed_info),
                    Keys.tasks: self.configure_work_position(value_parsed_info),
                    Keys.subject_theory: self.configure_subjects_lections(soup),
                    Keys.science_spectre: self.configure_scientific_directions(soup),
                    Keys.publications: self.configure_publications_info(soup),
                    Keys.subject_practice: self.configure_subjects_practice(soup),
                }
            )
        return value_return

    def start_parse(self) -> None:
        """
        Main method which is dedicated to start parsing user values
        Input:  None
        Output: we created new dataframe values
        """
        if self.get_check_development(self.file_csv):
            return
        prev = self.start_parse_html()
        self.develop_csv(
            pd.DataFrame(
                {
                    k: [i.get(k, '') for i in prev]
                    for k in IasaMMSA.rechange_list
                } 
            ),
            self.file_csv
        )