import os
import pandas as pd
from bs4 import BeautifulSoup
from parsers.parse_teacher import ParseTeachers
from config import ( 
    Keys,
    Folders, 
    IasaSP,
)


class DataTeacherSp(ParseTeachers):
    """
    class which is dedicated to develop the parsing of the teachers of the SP Teachers
    """
    def __init__(self) -> None:
        super(ParseTeachers, self).__init__()
        self.file_csv = os.path.join(
            Folders.folder_storage,
            IasaSP.df_name
        )

    @staticmethod
    def configure_names(name:str) -> str:
        """
        Static method which is dedicated to configure name for the selected names
        Input:  name = parsed name values
        Output: string with normalized values
        """
        return ' '.join(f.capitalize() for f in name.split())

    @staticmethod
    def configure_characteristics(text:str) -> dict:
        """
        Static mecthod which is dedicated to make all possible characteristics
        Input:  text = calculated values of the 
        Output: dictionary of the selected values
        """
        for r, rp in [
            ['\xa0', ''],
            ['::', ':'],
            ['Старший викладач', ''],
        ]:
            text = text.replace(r, rp)
        value_present, value_index = [], []
        for i, n in enumerate(IasaSP.list_ul):
            if n in text:
                value_present.append(i)
                text = text.replace(n, '')
        for k in [f for f in IasaSP.rechange_keys.keys() if f not in IasaSP.list_ul]:
            if k in text:
                value_index.append([k, text.index(k)])
                text = text.replace(k, IasaSP.sep)
        dict_return = {
            IasaSP.rechange_keys.get(elem, elem): text_s.strip()
            for elem, text_s in zip(
                [k[0] for k in sorted(value_index, key=lambda x: x[1])], 
                [f for f in text.split(IasaSP.sep) if f]
            )
        }
        dict_return['next'] = value_present
        return dict_return

    def start_parse_html(self) -> list:
        """
        Method which is dedicated to start parsing html values
        Input:  None
        Output: we developed the values of it
        """
        value_html = self.get_html_sync(IasaSP.link_start)
        soup = BeautifulSoup(value_html, 'html.parser')
        soup = soup.find('div', {"class":"entry-content"})
        names = soup.find_all('p', {"class":"professor-name"})
        subjects = [
            '|'.join(j.text for j in f.find_all('li')) 
            for f in soup.find_all('ul')
        ]
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
        value_dicts = [
            self.configure_characteristics(
                ''.join(
                    i.text for i in f if any(k in i.text for k in IasaSP.rechange_keys.keys())
                )
            ) 
            for f in teachers
        ]

        for value_dict, name in zip(value_dicts, names):
            value_dict[Keys.name] = name
            lists = value_dict.pop('next', [])
            for l in lists:
                value_dict.update(
                    {
                        IasaSP.rechange_keys.get(
                            IasaSP.list_ul[l],
                            l
                        ): subjects.pop(0)
                    }
                )
        return value_dicts

    def start_parse(self) -> None:
        """
        Method which is dedicated to develop the parse all values of it
        Input:  None
        Output: we parsed the values of the selected values
        """
        if self.get_check_development(self.file_csv):
            return
        prev = self.start_parse_html()
        self.develop_csv(
            pd.DataFrame(
                {
                    k: [i.get(k, '') for i in prev]
                    for k in IasaSP.rechange_keys.values()
                } 
            ),
            self.file_csv
        )