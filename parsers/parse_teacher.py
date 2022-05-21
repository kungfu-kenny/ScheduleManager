import aiohttp
import requests


class ParseTeachers:
    """
    class which is dedicated to develop the 
    """
    def __init__(self) -> None:
        pass

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
    