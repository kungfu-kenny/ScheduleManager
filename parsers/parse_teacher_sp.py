import os
from pprint import pprint
from bs4 import BeautifulSoup
from parsers.parse_teacher import ParseTeachers
from config import IasaSP


class DataTeacherSp(ParseTeachers):
    """
    class which is dedicated to develop the parsing of the teachers of the SP Teachers
    """
    def __init__(self) -> None:
        super(ParseTeachers, self).__init__()
        self.file_csv = 1

    @staticmethod
    def configure_names(name:str) -> str:
        return ' '.join(f.capitalize() for f in name.split())

    @staticmethod
    def configure_characteristics(text:str) -> dict:
        """
        Static mecthod which is dedicated to make all possible characteristics
        Input:  text = calculated values of the 
        Output: 
        """
        pass

    def start_parse_html(self) -> dict:
        """
        Method which is dedicated to start parsing html values
        Input:  None
        Output: we developed the values of it
        """
        value_html = self.get_html_test(IasaSP.link_start)
        soup = BeautifulSoup(value_html, 'html.parser')
        soup = soup.find('div', {"class":"entry-content"})
        names = soup.find_all('p', {"class":"professor-name"})
        subjects = [[j.text for j in f.find_all('li')] for f in soup.find_all('ul')]
        teacher, teachers = [], []
        for f in soup.find_all('p'):
            if f not in names:
                teacher.append(f)
            else:
                teachers.append(teacher)
                teacher = []
        teachers = [f for f in teachers if f]
        names = [self.configure_names(f.text) for f in names]
        status_job, status_science = [], []
        for f in [k.pop(0) for k in teachers]:
            status = [j.text for j in f.find_all('em')]
            if len(status) == 2:
                science, job = status
            elif len(status) == 1:
                science, job = status[0], ''
            status_job.append(job)
            status_science.append(science)
        for f in teachers[:1]:
            texted = ''.join(i.text for i in f)
            print(texted)
            print('cccccccccccccccccccccccccccccccccccccccccccc')
            

    def start_parse(self) -> None:
        """
        Method which is dedicated to develop the parse all values of it
        Input:  None
        Output:   
        """
        self.start_parse_html()