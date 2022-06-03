import os
import json
import pandas as pd
from pprint import pprint
from parsers.parse_teacher_schedule import DataTeacherSchedule
from config import (
    Keys,
    Folders,
    IasaAdditional,
)


class DevelopScientificPlan:
    """
    class which is dedicated to get the values from the Scientific Plan
    """
    def __init__(self) -> None:
        self.path_file = os.path.join(
            Folders.folder_storage, 
            IasaAdditional.df_name_schedule
        )
        
    @staticmethod
    def check_additional(path_file:str) -> None:
        """
        Static method which is dedicated to check the previous files
        Input:  path_file = path to selected json values
        Output: we developed the presence of the 
        """
        if not os.path.exists(path_file) and not os.path.isfile(path_file):
            DataTeacherSchedule().start_parse()

    @staticmethod
    def develop_unique_values(value_list:list, value_key:str, value_bool:bool=False) -> list:
        """
        Static method which is dedicated to develop the groups for this faculty
        Input:  value_list = list of the selected subjects
                value_key = string values to create
                value_bool = boolean value to develop string or list
        Output: we developed the selected values
        """
        result = []
        for res in value_list:
            r = res.get(value_key)
            if not r:
                continue
            elif isinstance(r, list):
                result.extend(r)
            else:
                result.append(r)
        if value_bool:
            return ';'.join(set(result)) 
        return [
            [i + 1, n] for i, n in enumerate(set(result))
        ]

    def develop_teachers_days(self) -> dict:
        """
        Method which is dedicated to develop the most favourable days for the teachers
        Input:  None
        Output: we developed the dictionary with them
        """
        pass

    def develop_teachers_locations(self) -> dict:
        """
        Method which is dedicated to develop the most favourable locations for all of them
        Input:  None
        Output: we developed the teachers locations
        """
        pass

    def develop_teachers_cabinets(self) -> dict:
        """
        Method which is dedicated to get the personal cabinets for all of the possible users
        Input:  None
        Output: we created the dict where the teachers can work
        """
        pass

    def start_parse(self) -> None:
        """
        Method which is dedicated to start parse values of the selectes
        Input:  None
        Output: we created 
        """
        self.check_additional(self.path_file)

        with open(self.path_file, 'r') as calculated_teachers:
            value_list = json.load(calculated_teachers)
        names = pd.read_csv(
            os.path.join(
                Folders.folder_storage, 
                IasaAdditional.df_name_teacher
            )
        )[[Keys.id, Keys.name]].to_dict('records')
        pprint(value_list[0])
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        groups = self.develop_unique_values(value_list, Keys.groups_list)
        times = self.develop_unique_values(value_list, Keys.time_begin)
        days = self.develop_unique_values(value_list, Keys.day_begin)
        for name in names[:1]:
            print(name)
            
        # for name in names[:1]:
        #     list_name = [
        #         f for f in value_list 
        #         if f.get(Keys.name_teacher_searched, '') == name.get(Keys.name)
        #     ]
        #     pprint(self.develop_groups(list_name))
        # pprint(list_name)