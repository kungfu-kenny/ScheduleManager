import imp
import os
import asyncio
import requests
import pandas as pd
from bs4 import BeautifulSoup, element
from parsers.parse_teacher import ParseTeachers
from config import (
    Folders,
    IasaAdditional,
)


class DataTeacherSchedule(ParseTeachers):
    """
    class which is dedicated to parse selected schedule
    """
    def __init__(self) -> None:
        super(DataTeacherSchedule, self).__init__()
        self.file_csv = os.path.join(
            Folders.folder_storage,
            IasaAdditional.df_name_schedule
        )

    def start_parse_html(self) -> list:
        """
        Method which is dedicated to develop the getting the 
        """
        k = requests.post(
            'http://rozklad.kpi.ua/Schedules/LecturerSelection.aspx',
            json={
                "ctl00_ToolkitScriptManager_HiddenField":"",
                "__VIEWSTATE":"/wEMDAwQAgAADgEMBQAMEAIAAA4BDAUDDBACAAAOAgwFCwwQAgwPAgEIQ3NzQ2xhc3MBD2J0biBidG4tcHJpbWFyeQEEXyFTQgUCAAAADAUNDBACAAAOAQwFAwwQAgwADwEBB29uZm9jdXMBHXRoaXMudmFsdWU9Jyc7dGhpcy5vbmZvY3VzPScnAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJkWCFbMSgxOXJsGpLI9ZU2imYY",
                "__EVENTTARGET":"",
                "__EVENTARGUMENT":"",
                "ctl00$MainContent$txtboxLecturer":"Петренко+Анатолій+Іванович",
                "ctl00$MainContent$btnSchedule":"Розклад+занять",
                "__EVENTVALIDATION":"/wEdAAEAAAD/////AQAAAAAAAAAPAQAAAAUAAAAIsA3rWl3AM+6E94I53LbWK4YqVqwLAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACvHV09VRintN+nMH+p4yerPBpN+",
                "hiddenInputToUpdateATBuffer_CommonToolkitScripts":"0"
            }
        )
        # print(k.status_code)
        # print('__________________________________________')
        # print(k.headers)
        # print('ccccccccccccccccccccccccccccccccccccccccccc')
        # print(k.text)
    
    def start_parse(self) -> None:
        """
        Method which is dedicated to develop the parse all values of it
        Input:  None
        Output: we parsed the values of the selected values
        """
        if self.get_check_development(self.file_csv):
            return
        prev = self.start_parse_html()