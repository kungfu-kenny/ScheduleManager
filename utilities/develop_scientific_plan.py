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
    def save(df:pd.DataFrame, path:str) -> None:
        """
        Static method which is dedicated to save new dataframe
        Input:  df = new dataframe
                path = path to it
        Output: we created dataframe values
        """
        df.to_csv(path, index=False)

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
        return {
            n: i + 1 for i, n in enumerate(set(result))
        }

    def start_parse(self) -> None:
        """
        Method which is dedicated to start parse values of the selectes
        Input:  None
        Output: we created 
        """
        self.check_additional(self.path_file)

        with open(self.path_file, 'r') as calculated_teachers:
            value_list = json.load(calculated_teachers)
        names = {
            f.get(Keys.name, '') : f.get(Keys.id)
            for f in pd.read_csv(
                os.path.join(
                    Folders.folder_storage, 
                    IasaAdditional.df_name_teacher
                )
            )[[Keys.id, Keys.name]].to_dict('records')
        }
        groups = self.develop_unique_values(value_list, Keys.groups_list)
        times = self.develop_unique_values(value_list, Keys.time_begin)
        days = self.develop_unique_values(value_list, Keys.day_begin)
        
        if not os.path.exists(
            os.path.join(Folders.folder_storage, IasaAdditional.df_name_day)
        ):
            self.save(
                pd.DataFrame(
                    {
                        Keys.id: [k for k, _ in days.items()],
                        Keys.day_begin: [v for _, v in days.items()]
                    }
                ),
                os.path.join(Folders.folder_storage, IasaAdditional.df_name_day)
            )

        if not os.path.exists(
            os.path.join(Folders.folder_storage, IasaAdditional.df_name_group)
        ):
            self.save(
                pd.DataFrame(
                    {
                        Keys.id: [k for k, _ in groups.items()],
                        Keys.group: [v for _, v in groups.items()]
                    }
                ),
                os.path.join(Folders.folder_storage, IasaAdditional.df_name_group)
            )

        if not os.path.exists(
            os.path.join(Folders.folder_storage, IasaAdditional.df_name_time)
        ):
            self.save(
                pd.DataFrame(
                    {
                        Keys.id: [k for k, _ in times.items()],
                        Keys.time_begin: [v for _, v in times.items()]
                    }
                ),
                os.path.join(Folders.folder_storage, IasaAdditional.df_name_time)
            )

        if all(
            [
                os.path.exists(
                    os.path.join(Folders.folder_storage, f)
                )
                for f in 
                [
                    IasaAdditional.df_name_teacher_day,
                    IasaAdditional.df_name_teacher_time,
                    IasaAdditional.df_name_teacher_group
                ]
            ]
        ):
            return
        teacher_group, teacher_time, teacher_day = [], [], []
        for subject in value_list:
            if not subject.get(Keys.name_subject_small):
                continue
            
            day = [
                names.get(
                    subject.get(Keys.name_teacher_searched),
                    ''
                ), 
                days.get(
                    subject.get(Keys.day_begin),
                    ''
                )
            ]
            time = [
               names.get(
                   subject.get(Keys.name_teacher_searched, ''),
                    ''
               ),
               times.get(
                   subject.get(Keys.time_begin, ''),
                   ''
               )
            ] 
            group = [
                [
                    names.get(
                        subject.get(Keys.name_teacher_searched, ''),
                        ''
                    ),
                    groups.get(
                        k,
                        ''
                    )
                ]
               for k in subject.get(Keys.groups_list, [])
            ]
            if day not in teacher_day:
                teacher_day.append(
                    day
                )
            if time not in teacher_time:
                teacher_time.append(
                    time
                )
            for f in group:
                if f not in teacher_group:
                    teacher_group.append(
                        f
                    )
        
        if not os.path.exists(
            os.path.join(Folders.folder_storage, IasaAdditional.df_name_teacher_time)
        ):
            self.save(
                pd.DataFrame(
                    {
                        Keys.id_teacher: [k for k, _ in teacher_time],
                        Keys.id_time: [v for _, v in teacher_time]
                    }
                ),
                os.path.join(Folders.folder_storage, IasaAdditional.df_name_teacher_time)
            )
        
        if not os.path.exists(
            os.path.join(Folders.folder_storage, IasaAdditional.df_name_teacher_group)
        ):
            self.save(
                pd.DataFrame(
                    {
                        Keys.id_teacher: [k for k, _ in teacher_group],
                        Keys.id_group: [v for _, v in teacher_group]
                    }
                ),
                os.path.join(Folders.folder_storage, IasaAdditional.df_name_teacher_group)
            )
        
        if not os.path.exists(
            os.path.join(Folders.folder_storage, IasaAdditional.df_name_teacher_day)
        ):
            self.save(
                pd.DataFrame(
                    {
                        Keys.id_teacher: [k for k, _ in teacher_day],
                        Keys.id_day: [v for _, v in teacher_day]
                    }
                ),
                os.path.join(Folders.folder_storage, IasaAdditional.df_name_teacher_day)
            )