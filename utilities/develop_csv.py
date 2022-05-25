import os
import re
import pandas as pd
from parsers.parse_teacher_sp import DataTeacherSp
from parsers.parse_teacher_mmsa import DataTeacherMmsa
from config import (
    Folders,
    Keys,
    IasaSP,
    IasaMMSA,
    IasaAdditional,
)


class DevelopAdditionalCSV:
    """
    class which is dedicated to develop additional csv for the databases
    """
    def __init__(self) -> None:
        self.path_sp = os.path.join(Folders.folder_storage, IasaSP.df_name)
        self.path_mmsa = os.path.join(Folders.folder_storage, IasaMMSA.df_name)
        self.path_all = os.path.join(Folders.folder_storage, IasaAdditional.df_name_teacher)

    @staticmethod
    def check_presence(path:str) -> bool:
        """
        Static method which is dedicated to check that file exists
        Input:  path = path the csv
        Output: boolean value to presence
        """
        return os.path.exists(path) and os.path.isfile(path)

    @staticmethod
    def check_additional(value_previous:bool=False) -> None:
        """
        Static method which is dedicated to develop additional check
        Input:  value_previous = boolean value which is dedicated to check
        Output: we developed the additional check
        """
        if not value_previous:
            return
        for cls in [DataTeacherSp, DataTeacherMmsa]:
            a = cls()
            a.start_parse()

    @staticmethod
    def save(df:pd.DataFrame, path:str) -> None:
        """
        Static method which is dedicated to save new dataframe
        Input:  df = new dataframe
                path = path to it
        Output: we created dataframe values
        """
        df.to_csv(path, index=False)

    def parse_specialization(self) -> None:
        """
        Method which is dedicated to created csv table of the specialization
        Input:  None
        Output: we developed the specialization
        """
        path = os.path.join(Folders.folder_storage, IasaAdditional.df_name_specialization)
        if self.check_presence(path):
            return
        df = pd.read_csv(self.path_mmsa)
        value_spec = []
        for k in [Keys.subject_theory, Keys.subject_practice, Keys.science_spectre]:
            value_spec.extend(df[k].unique())
        chairs, specs = ['SP'], [IasaSP.specialization]
        for m in value_spec:
            if not isinstance(m, str):
                continue
            for f in m.split('|'):
                req = re.search(r'\[(.*?)\]', f).group(1)
                if req not in specs:
                    specs.append(req)
                    chairs.append('MMSA')
        self.save(
            pd.DataFrame(
                {
                    Keys.id: [i for i in range(1, len(specs) + 1)],
                    Keys.specialization: specs,
                    Keys.chair: chairs
                }
            ),
            path
        )

    def parse_subjects(self) -> None:
        """
        Method which is dedicated to parse all subjects from the dataframes
        Input:  None
        Output: we developed the selected subjects
        """
        path = os.path.join(Folders.folder_storage, IasaAdditional.df_name_subject)
        if self.check_presence(path):
            return
        subjects = []
        for name, chair in zip([self.path_sp, self.path_mmsa], ['SP', 'MMSA']):
            df = pd.read_csv(name)
            value_subjects = []
            for k in [Keys.subject_theory, Keys.subject_practice]:
                value_subjects.extend(df[k].unique())
            for f in value_subjects:
                if not isinstance(f, str):
                    continue
                for check in f.split('|'):
                    subject = check.strip() if chair == 'SP' else check.split('[')[0].strip()
                    if not subject in subjects:
                        subjects.append(subject)
        self.save(
            pd.DataFrame(
                {
                    Keys.id: [i for i in range(1, len(subjects) + 1)],
                    Keys.subject: subjects,
                }
            ),
            path
        )


    def parse_spectre(self) -> None:
        """
        Method which is dedicated to parse scientific spectre
        Input:  None
        Output: we developed the spectre of it
        """
        path = os.path.join(Folders.folder_storage, IasaAdditional.df_name_spectre)
        if self.check_presence(path):
            return
        spectres = []
        for name, chair in zip([self.path_sp, self.path_mmsa], ['SP', 'MMSA']):
            df = pd.read_csv(name)
            for f in df[Keys.science_spectre].unique():
                if not isinstance(f, str):
                    continue
                sep = ',' if chair == 'SP' else '|'
                for check in f.split(sep):
                    spectre = check.strip() if chair == 'SP' else check.split('[')[0].strip()
                    if not spectre in spectres:
                        spectres.append(spectre)
        self.save(
            pd.DataFrame(
                {
                    Keys.id: [i for i in range(1, len(spectres) + 1)],
                    Keys.spectre: spectres
                }
            ),
            path
        )

    def parse_workers(self) -> None:
        """
        Method which is dedicated to develop addtional csv for the creating merged values
        Input:  None
        Output: we created csv for the further df
        """
        if self.check_presence(self.path_all):
            return
        df_sp = pd.read_csv(self.path_sp)
        df_mmsa = pd.read_csv(self.path_mmsa)
        df_sp[Keys.chair] = 'SP'
        df_mmsa[Keys.chair] = 'MMSA'
        df_teachers = pd.concat(
            [
                df_sp,
                df_mmsa,
            ]
        )

        df_teachers[Keys.id] = [i for i in range(1, df_teachers.shape[0]+1)]
        df_teachers = df_teachers.fillna(' ')
        self.save(
            df_teachers,
            self.path_all
        )

    def parse_database_subject(self) -> None:
        """
        Method which is dedicated to develop dataframes of the subjects
        Input:  None
        Output: dataframe with selected id values
        """
        path = os.path.join(Folders.folder_storage, IasaAdditional.df_name_teacher_subject)
        if self.check_presence(path):
            return
        df_used = pd.read_csv(
            os.path.join(
                Folders.folder_storage, 
                IasaAdditional.df_name_subject
            )
        )
        id_subject = df_used[[Keys.id, Keys.subject]].values.tolist()
        df_used = pd.read_csv(self.path_all)
        id_used = df_used[
            [
                Keys.id, 
                Keys.subject_theory, 
                Keys.subject_practice
            ]
        ].values.tolist()
        teachers, subjects = [], []
        for id_teacher, theory, practice in id_used:
            for id_sub, subject in id_subject:
                if any(subject in f for f in [theory, practice]):
                    teachers.append(id_teacher)
                    subjects.append(id_sub)
        self.save(
            pd.DataFrame(
                {
                    Keys.id_teacher: teachers,
                    Keys.id_subject: subjects,
                }
            ),
            path
        )

    def parse_database_spectre(self) -> None:
        """
        Method which is dedicated to develop dataframes of the spectre
        Input:  None
        Output: dataframe with the selected id values
        """
        path = os.path.join(Folders.folder_storage, IasaAdditional.df_name_teacher_spectre)
        if self.check_presence(path):
            return
        df_used = pd.read_csv(
            os.path.join(
                Folders.folder_storage, 
                IasaAdditional.df_name_spectre
            )
        )
        id_spectre = df_used[[Keys.id, Keys.spectre]].values.tolist()
        df_used = pd.read_csv(self.path_all)
        id_used = df_used[[Keys.id, Keys.science_spectre]].values.tolist()
        teachers, spectres = [], []
        for id, spectre in id_used:
            for id_s, spectre_possible in id_spectre:
                if spectre_possible in spectre:
                    teachers.append(id)
                    spectres.append(id_s)

        self.save(
            pd.DataFrame(
                {
                    Keys.id_teacher: teachers,
                    Keys.id_spectre: spectres,
                }
            ),
            path
        )

    def parse_database_specialization(self) -> None:
        """
        Method which is dedicated to develop datafranes
        Input:  None
        Output: dataframe with the selected id values
        """
        path = os.path.join(Folders.folder_storage, IasaAdditional.df_name_teacher_specialization)
        if self.check_presence(path):
            return
        df_used = pd.read_csv(
            os.path.join(
                Folders.folder_storage, 
                IasaAdditional.df_name_specialization
            )
        )
        id_specialization = df_used[[Keys.id, Keys.specialization]].values.tolist()
        df_used = pd.read_csv(self.path_all)
        id_used = df_used[
            [
                Keys.id, 
                Keys.chair, 
                Keys.subject_theory, 
                Keys.subject_practice, 
                Keys.science_spectre
            ]
        ].values.tolist()
        
        teacher, specialization = [], []
        i = id_specialization[[f[1] for f in id_specialization].index(IasaSP.specialization)][0]
        
        for id_teacher, chair, theory, practice, spectre in id_used:
            if chair == 'SP':
                teacher.append(id_teacher)
                specialization.append(i)
            else:
                for id_spec, spec in id_specialization:
                    if any(spec in f for f in [theory, practice, spectre]):
                        teacher.append(id_teacher)
                        specialization.append(id_spec)
        
        self.save(
            pd.DataFrame(
                {
                    Keys.id_teacher: teacher,
                    Keys.id_spec: specialization,
                }
            ),
            path
        )

    def start_parse(self) -> None:
        """
        Method which is dedicated to create the csv values for the all of it
        Input:  None
        Output: we created the csv values for the additional values
        """
        self.check_additional(
            set(
                [IasaSP.df_name, IasaMMSA.df_name]
            ).issubset(os.listdir(Folders.folder_storage))
        )
        
        self.parse_workers()
        self.parse_spectre()
        self.parse_subjects()
        self.parse_specialization()
        
        self.parse_database_spectre()
        self.parse_database_subject()
        self.parse_database_specialization()