import os
import pandas as pd
from bs4 import BeautifulSoup
from parsers.parse_teacher import ParseTeachers
from config import Folders


class DataTeacherMmsa(ParseTeachers):
    """
    class which is dedicated to start parsing another branch of the iasa teachers
    """
    def __init__(self) -> None:
        super(DataTeacherMmsa, self).__init__()

    def start_parse_html(self) -> list:
        """
        
        """
        pass

    def start_parse(self) -> None:
        """
        Main method which is dedicated to start parsing user values
        Input:  None
        Output: we created new dataframe values
        """
        pass