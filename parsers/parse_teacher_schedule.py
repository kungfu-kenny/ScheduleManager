import os
import asyncio
from pprint import pprint
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
        #TODO check the values of the length
        value_name = value_name[Keys.name].to_list()[:1]
        
        loop = asyncio.get_event_loop()
        list_html = loop.run_until_complete(
            self.get_html_all_schedule(
                value_name
            )
        )
        
        for html in list_html:
            soup = BeautifulSoup(html, 'html.parser')
            header_first = self.get_text(
                soup.find(
                    'span', 
                    {"id":"ctl00_MainContent_lblFirstTable"}
                )
            )
            header_second = self.get_text(
                soup.find(
                    'span', 
                    {'id': 'ctl00_MainContent_lblSecondTable'}
                )
            )
            
            table_first = soup.find(
                'table',
                {"id":"ctl00_MainContent_FirstScheduleTable"}
            )
            
            table_second = soup.find(
                'table',
                {"id":"ctl00_MainContent_SecondScheduleTable"}
            )


    def start_parse(self) -> None:
        """
        Method which is dedicated to develop the parse all values of it
        Input:  None
        Output: we parsed the values of the selected values
        """
        if self.get_check_development(self.file_csv):
            return
        self.check_additional()
        prev = self.start_parse_html()