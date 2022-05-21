import os
import aiohttp
import requests
import pandas as pd


class ParseTeachers:
    """
    class which is dedicated to develop the 
    """
    def __init__(self) -> None:
        pass

    @staticmethod
    def develop_csv(df:pd.DataFrame, df_path:str) -> None:
        """
        Static method which is dedicated to create csv
        Input:  df = pandas DataFrame which was previously created
                df_path = path to the new csv file
        Output: we created csv value
        """
        df.to_csv(df_path, index=False)

    @staticmethod
    def get_check_development(path_file:str) -> bool:
        """
        Static method which is dedicated to check previous
        Input:  path_file = path of previous file created
        Output: boolean value which shows that file is present
        """
        return os.path.exists(path_file) and os.path.isfile(path_file)

    @staticmethod
    def get_html_test(value_link:str) -> str:
        """
        Method which is dedicated to get test values of the 
        Input:  value_link = link of the selected to search
        Output: text of the selected html
        """
        ret = requests.get(value_link, verify=False)
        if ret.status_code == 200:
            return ret.text
        return ''
    