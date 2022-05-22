import os
import asyncio
import pandas as pd
from pprint import pprint
from bs4 import BeautifulSoup, element
from parsers.parse_teacher import ParseTeachers
from config import Folders, IasaMMSA


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
            return [[k.text.replace('\n', '').strip() for k in v] for v in value_subjects]
        return []

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
            return [[k.text.replace('\n', '').strip() for k in v] for v in value_scientific_directions]
        return []

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
            return [v for v in value_publications_info if v]
        return []

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
            value_subjects = [v for v in value_subjects if v]
            return [
                [k.text.replace('\n', '').strip() for k in v] for v in value_subjects
            ]
        return []

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
                list_teachers
            )
        )
        for html in list_html[:10]:
            soup = BeautifulSoup(html, 'html.parser')
            value_subjects_lections = self.configure_subjects_lections(soup)
            value_scientific_directions = self.configure_scientific_directions(soup)
            value_publications_info = self.configure_publications_info(soup)
            value_subjects_practices = self.configure_subjects_practice(soup)
            # pprint(value_subjects_lections)
            # print('-----------------------------------------------')
            # pprint(value_scientific_directions)
            # print('-----------------------------------------------')
            # pprint(value_publications_info)
            # print('-----------------------------------------------')
            # pprint(value_subjects_practices)
            # print('-----------------------------------------------')
            # print('cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc')

    def start_parse(self) -> None:
        """
        Main method which is dedicated to start parsing user values
        Input:  None
        Output: we created new dataframe values
        """
        if self.get_check_development(self.file_csv):
            return
        self.start_parse_html()