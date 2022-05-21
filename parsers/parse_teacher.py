import asyncio
import os
import aiohttp
import requests
import pandas as pd
from config import IasaMMSA


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
    def get_html_sync(value_link:str) -> str:
        """
        Method which is dedicated to get sync values of the 
        Input:  value_link = link of the selected to search
        Output: text of the selected html
        """
        ret = requests.get(value_link, verify=False)
        if ret.status_code == 200:
            return ret.text
        return ''

    @staticmethod
    async def get_html_async(value_link:str, session:object) -> str:
        """
        Async static method which is dedicated to get html values
        Input:  value_link = link of the previously used
                session = previously created session of the values
        Output: we developed the html async values
        """
        async with session.get(value_link) as resp:
            if resp.status == 200:
                return await resp.text()
        return ''

    async def get_html_all(self, value_links:list) -> list:
        """
        Async method which is dedicated to get previously created lists
        Input:  value_links = list of selected links to get links
        Output: list of previously dedicated html texts
        """
        semaphore = asyncio.Semaphore(IasaMMSA.thread)
        async with semaphore:
            async with aiohttp.ClientSession(trust_env=True) as session:
                tasks = [
                    asyncio.create_task(
                        self.get_html_async(value_link, session)
                    )
                    for value_link in value_links
                ]
                return await asyncio.gather(*tasks)