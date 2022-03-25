import os
import re
import bs4
import json
import requests
import itertools
import pandas as pd
from bs4 import BeautifulSoup
from pprint import pprint
from config import (IasaSp as sp,
                    IasaMmsa as mmsa,
                    folder_csv,
                    link_iasa_personal_sp,
                    link_iasa_personal_mmsa)


class DataDriver:
    """
    class which is dedicated to work directly with data in dataframes
    or to make values which would be touched in the os
    """
    def __init__(self):
        self.get_name_csv = lambda x: f"{x}.csv"
        self.path_original = os.path.dirname(os.path.realpath(__file__))
        self.path_csv = self.get_path(self.path_original, folder_csv)
        self.check_folder(self.path_csv)

    @staticmethod
    def get_path(*path_folders:set) -> str:
        """
        Static method which is dedicated to create full path
        Input:  path_folders = set with values which would be currently used
        OutputL string with our new path
        """
        return os.sep.join(path_folders)

    @staticmethod
    def check_folder(folder_path:str) -> None:
        """
        Method which is dedicated to check presence of a folder and to 
        Input:  folder_path = path to the folder which i need to create
        Output: None, but we have crated new folder
        """
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)

    @staticmethod
    def save_df(value_df:pd.DataFrame, value_path:str, value_test:bool=True) -> None:
        """
        Static method which is dedicated to save dataframe for it
        Input:  value_df = dataframe which neds to be saved
                value_path = path which is would take
                value_test = is it test or not
        Output: We successfully created new dataframe within the folder
        """
        if not value_test:
            if not os.path.isfile(value_path):
                value_df.to_csv(value_path, index=False)
            value_name, value_ext = os.path.splitext(value_path)
            if value_ext != '.csv':
                value_df.to_csv(value_path, index=False)
            else:
                print("You have this file")
        else:
            value_df.to_csv(value_path, index=False)


class ParseDriver:
    """
    class which is dedicated to be a basic parse for the values
    """
    def __init__(self):
        self.tag = re.compile('<.*?>')
        self.remove_tags = lambda x: re.sub(self.tag, '', x)
        self.remove_special = lambda x: re.sub(r"\W+|_", ' ', x)
        self.remove_spaces = lambda x: x.strip()
        self.make_rename = lambda x: ' '.join(v.capitalize() for v in x.lower().split(' '))
        self.cut_link = lambda x: '/'.join(x.split('/')[:3])
        self.count_colision = lambda x: [index for index, value in enumerate(x) if value.isupper()]

    @staticmethod
    def make_double_surname(value_string:str) -> str:
        """
        Static method which is dedicated to make further check 
        in case of double surname.name, etc.
        Input:  value_string = string which we have previously inserted
        Output: this string but with the fixed moment
        """
        value_list = [index + 1 for index, value in enumerate(value_string) if value == '-']
        if value_list:
            for index in value_list:
                lst = list(value_string)
                letter = lst.pop(index)
                value_string = ''.join(lst)
                if letter.isalpha() and index < len(value_string):
                    value_string = value_string[:index] + letter.upper() + value_string[index:]
                else:
                    value_string = value_string[:index] + letter + value_string[index:]
        return value_string


    @staticmethod
    def develop_request(link:str) -> str:
        """
        Static method which is dedicated to check link on usefullness
        Input:  link = link which would make get request
        Output: we successfully developed the
        """
        try:
            if link:
                value_request = requests.get(link, verify=False)
                if value_request.status_code == requests.codes.ok:
                    return value_request.text
            return ""
        except Exception as e:
            #TODO add logs in the end
            print(e)
            return ""

    def proceed_parse(self, link:str=''):
        """
        Method which is dedicated to work with a parsing of a website
        Input:  link = values which is required to parse
        Output: values to the parsing
        """
        pass

    def compose_data(self):
        """
        Method which is dedicated to develop final compose of the data
        """
        pass

    def parse_manually(self, parse_object:bs4.element.Tag) -> dict:
        """
        Method which is dedicated to manuall parse broken html
        Input:  parse_object = object which we would parse
        Output: dict
        """
        pass

    def develop_special_occassions(self, value_info:list):
        """
        Method which is used for a specific purposes in cases of broken html
        Input:  value_info = already parsed values
        Output: value_info but fixed
        """
        pass


class ParseIasaSp(ParseDriver):
    """
    class which is dedicated to work with a parse of the SP
    """
    def __init__(self):
        self.rand = sp.random_string
        self.number_min = 5
        self.number_special = 22
        self.number_transfer = 2
        self.add_m = 'м. '
        self.driver_csv = DataDriver()
        super().__init__()

    def make_transfer(self, value_input:str):
        """
        Method for removale of the html
        Input:  value_input = string with the html
        Output: string without other elements
        """
        value_input = self.remove_tags(value_input)
        return self.remove_spaces(value_input)

    def make_further_check(self, value_key:str, value_string:str, value_searched:str) -> dict:
        """
        Method which is dedicated to сheck sub columns in cases of the bad markup
        Input:  value_key = key which would be further used
                value_string = string which was parsed
                value_searched = value which was searched in that cases
        Output: value_dictionary of all of that
        """
        val_one, val_two = value_searched
        if not val_one in value_string and not val_two in value_string:
            return {value_key: self.make_transfer(value_string)}
        elif val_one in value_string and not val_two in value_string:
            value_searched = val_one 
        elif not val_one in value_string and val_two in value_string:
            value_searched = val_two
        value_key_answer, value_searched_answer = value_string.split(value_searched)
        return {value_key: self.make_transfer(value_key_answer), 
                sp.rechange_iasa[value_searched]: self.make_transfer(value_searched_answer)}

    def parse_manually(self, parse_object:bs4.element.Tag) -> dict:
        """
        Method which is dedicated to manuall parse broken html
        Input:  parse_object = object which we would parse
        Output: dict
        """
        list_column_names = [str(v) for v in parse_object.find_all('b')]
        parse_object = str(parse_object)
        list_column_names.insert(0, '</a>')
        list_split = []
        for types in list_column_names:
            if types in list_column_names:
                list_split.append(types)
                parse_object = parse_object.replace(types, self.rand)
        parse_split = parse_object.split(self.rand)
        if '</a>' in list_split:
            list_split[0] = sp.status_iasa
        list_split = [self.remove_tags(x) for x in list_split]
        list_split = [self.remove_special(x) for x in list_split]
        list_split = [self.remove_spaces(x) for x in list_split]
        list_split = [v for v in list_split if v]
        value_dict = {}
        if len(parse_split) > 1:
            for column_value, value in zip(list_split, parse_split[1:]):
                value_dict.update(self.make_further_check(
                    sp.rechange_iasa[column_value], value, sp.rechange_phrase))
        return value_dict

    def develop_special_occassions(self, value_info:list) -> list:
        """
        Method for the special ocassions for this
        Input:  value_info = all previously parsed from it
        Output: straight shined list with data
        """
        list_index_previous, list_index_current, list_resave = [], [], []
        for number, value in enumerate(value_info):
            if len(value) < self.number_min and number > 0:
                list_index_current.append(number)
                list_index_previous.append(number - 1)
                list_resave.append(value_info[number - 1][sp.status_iasa])
        for previous, current, rename in zip(list_index_previous, list_index_current, list_resave):
            value_rem = value_info[current]
            value_info[previous].update(value_rem)
            value_info[previous][sp.status_iasa] = rename
        for current in list_index_current:
            value_info.pop(current)
        for value in value_info:
            value[sp.status_iasa] = value[sp.status_iasa].replace('-', '')
            value[sp.status_iasa] = value[sp.status_iasa].replace('>', '')
        dictionary_remove = value_info.pop(self.number_special)
        value_change = dictionary_remove.pop(sp.rechange_birthplace)
        value_birthplace, value_glitch = value_change.split(sp.rechange_glitch_22)
        dictionary_remove.update({sp.rechange_birthplace:value_birthplace, 
                        sp.rechange_iasa[sp.rechange_glitch_22]: self.make_transfer(value_glitch)})
        value_info.insert(self.number_special, dictionary_remove)
        
        dictionary_remove = value_info.pop(self.number_transfer)
        value_change = dictionary_remove.pop(sp.status_iasa)
        value_birth = dictionary_remove.pop(sp.rechange_birthplace)
        dictionary_remove[sp.rechange_birthplace] = self.add_m + value_birth 
        value_stay, value_move = [self.remove_spaces(v) for v in value_change.split(',')]
        dictionary_remove[sp.status_iasa] = value_stay
        dictionary_remove[sp.rechange_accomplishments] = value_move
        value_info.insert(self.number_transfer, dictionary_remove)
        
        for value in value_info:
            list_upper_index = self.count_colision(value[sp.status_iasa])
            if len(list_upper_index) == 2:
                value_check = value.pop(sp.status_iasa)
                value_check = value_check[:list_upper_index[-1]] + sp.random_string + value_check[list_upper_index[-1]:]
                value_stay, value_move = value_check.split(sp.random_string)
                value[sp.status_iasa] = value_stay
                value[sp.rechange_special_status] = value_move
            if sp.rechange_work_begin in value.keys():
                replacement = value.pop(sp.rechange_work_begin)
                value[sp.rechange_work_begin] = self.remove_spaces(replacement.replace(":", ''))
            if sp.rechange_accomplishments in value.keys():
                replacement = value.pop(sp.rechange_accomplishments)
                value[sp.rechange_accomplishments] = self.remove_spaces(replacement.replace(":", ''))

        for value in value_info:
            for column_change in sp.rechange_list_into:
                if column_change in value.keys() and ('•' in value[column_change] or '-' in value[column_change]):
                    value_pop = value.pop(column_change)
                    value_new = sp.rechange_sub_sep.join(self.remove_spaces(v).capitalize() for v in re.split(r'-|•', value_pop) if v)
                    for value_searched, value_return in sp.rechange_dict_values.items():
                        if re.match(value_searched, value_new, re.IGNORECASE):
                            pattern = re.compile(value_searched, re.IGNORECASE)
                            value_new = pattern.sub(value_return, value_new)
                    value[column_change] = value_new
        return value_info

    def return_names(self, name_parsed:list) -> list:
        """
        Method which is dedicated to return names from parsed values
        Input:  name_parsed = names which were previously parsed
        Output: list which could be further used in analysis
        """
        titles = [n.get('title') for n in name_parsed]
        names = [self.make_rename(n) for n in titles if n]
        names = [self.make_double_surname(n) for n in names]
        return [n.replace(sp.rechange_val, sp.rechange_for) if sp.rechange_val in n else n for n in names]

    def proceed_parse(self, link:str) -> None:
        """
        Method which is dedicated to proceed parsing of the current link in cases
        Input:  link = link which i need to parse
        Output: we successfully returned new values to the csv
        """
        value_info = []
        value_html = self.develop_request(link)
        if value_html:
            value_parsed = BeautifulSoup(value_html, 'html.parser')
            value_parsed = value_parsed.find('tr')
            info_parsed = value_parsed.find_all('p')
            name_parsed = value_parsed.find_all('a')
            names = self.return_names(name_parsed)
            for info in info_parsed:
                value_info.append(self.parse_manually(info))
        value_info = [v for v in value_info if v]
        value_info = self.develop_special_occassions(value_info)
        for name, value in zip(names, value_info):
            value.update({sp.rechange_name: name})
        df = pd.read_json(json.dumps(value_info))
        df_name = self.driver_csv.get_name_csv(sp.df_iasa_sp)
        df_path = self.driver_csv.get_path(self.driver_csv.path_csv, df_name)
        self.driver_csv.save_df(df, df_path)


class ParseIasaMmsa(ParseDriver):
    """
    class which is dedicated to basically parse from the 
    """
    def __init__(self):
        self.join_link = lambda *x: ''.join(x)
        super().__init__()

    def parse_manually(self, parse_object:bs4.element.Tag) -> dict:
        """
        Method which is dedicated to manually parse 
        Input:  parse_object
        """
        pass

    def proceed_links(self, link:str) -> set:
        """
        Method which is dedicated to start work with links
        Input:  link = link of th main parse string
        Output: list of the names and list with links of this names 
        """
        value_info = []
        value_html = self.develop_request(link)
        if value_html:
            value_parsed = BeautifulSoup(value_html, 'html.parser')
            value_parsed = value_parsed.find(class_="view-content")
            value_parsed = value_parsed.find_all('a')
            value_names = [a.text for a in value_parsed]
            link_original = self.cut_link(link)
            value_link = [self.join_link(link_original, a.get('href')) for a in value_parsed]
            return value_names, value_link
        return [], []

    def return_phone(self, value_parsed:bs4.element.Tag) -> str:
        """
        Method which is dedicated to parse phone numbers from the
        Input:  value_parsed = parsed html from the site
        Output: string of the phone number
        """
        value_email = value_parsed.find(class_='field-name-field-s-person-phone-display')
        if value_email:
            return value_email.find(class_='field-items').text
        return ''

    def return_homeplace(self, value_parsed:bs4.element.Tag) -> str:
        """
        Method which is dedicated to parse the homeplace in the campus
        Input:  value_parsed = value which was parsed
        Output: homeplace of the 
        """
        value_email = value_parsed.find(class_='field-name-field-s-person-office-location')
        if value_email:
            return value_email.find(class_='field-items').text
        return ''

    def return_email(self, value_parsed:bs4.element.Tag) -> str:
        """
        Method which is dedicated to parse email of the teacher
        Input:  value_parsed = value which was parsed
        """
        value_email = value_parsed.find(class_='field-type-email')
        if value_email:
            return value_email.find(class_='field-items').text
        return ''

    def return_photo(self, value_parsed:bs4.element.Tag) -> str:
        """
        Method which is dedicated to parse photo of the teacher
        Input:  value_parsed = value which was parsed
        Output: string with an image
        """
        value_img = value_parsed.find('img')
        return value_img['src'] if value_img else ''
    
    def return_status(self, value_parsed:bs4.element.Tag) -> str:
        """
        Method which is dedicated to parse status on a cafdra status
        of a worker
        Input:  value_parsed = value which was prviously used
        Output: status of the teacher
        """
        value_status = value_parsed.find(class_='field-name-field-s-person-faculty-type')
        if value_status:
            return value_status.text
        return ''

    def return_accomplishments(self, value_parsed:bs4.element.Tag) -> str:
        """
        Method which is dedicated to parse accomplihments
        Input:  value_parsed = value which was previously used
        Output: accomplishment
        """
        value_accomplishments = value_parsed.find(class_='field-name-field-degree')
        if value_accomplishments:
            return value_accomplishments.text
        return ''

    def return_accolodates(self, value_parsed:bs4.element.Tag) -> str:
        """
        Method is about to return biography from some of them
        Input:  value_parsed = previously parsed values
        Output: text about the person
        """
        value_accolodates = value_parsed.find(class_='field-type-text-with-summary')
        if value_accolodates:
            return value_accolodates.text
        return ''

    def return_work_position(self, value_parsed:bs4.element.Tag) -> str:
        """
        Method which is dedicated to parse work position of the person inside the faculty
        Input:  value_parsed = previously parsed values
        Output: teext about the work position
        """
        value_work_position = value_parsed.find(class_='field-name-field-s-person-staff-type')
        if value_work_position:
            return value_work_position.text
        return ''

    def return_subjects_lections(self, value_parsed:bs4.element.Tag) -> list:
        """
        Method which is dedicated to return subjects which are lectures to selected specialization
        Input:  value_parsed = parsed previously value
        Output: list with format [specialization, subject]
        """
        value_subjects = value_parsed.find('div', {'id':'block-views-discipline-by-lecturer-block'})
        if value_subjects:
            value_subjects = value_subjects.find(class_='view-discipline-by-lecturer')
            value_subjects = value_subjects.find('table')
            value_subjects = value_subjects.find_all('tr')
            value_subjects = [v.find_all('td') for v in value_subjects]
            value_subjects = [v for v in value_subjects if v]
            return [[self.remove_spaces(k.text.replace('\n', '')) for k in v] for v in value_subjects]
        return []

    def return_subjects_practice(self, value_parsed:bs4.element.Tag) -> list:
        """
        Method which is dedicated to return subjects which are practices to selected specialization
        Input:  value_parsed = parsed previously value
        Output: list with format [specialization, subject]
        """
        value_subjects = value_parsed.find('div', {'id': 'block-views-discipline-by-lecturer-block-1'})
        if value_subjects:
            value_subjects = value_subjects.find(class_='view-discipline-by-lecturer')
            value_subjects = value_subjects.find('table')
            value_subjects = value_subjects.find_all('tr')
            value_subjects = [v.find_all('td') for v in value_subjects]
            value_subjects = [v for v in value_subjects if v]
            return [[self.remove_spaces(k.text.replace('\n', '')) for k in v] for v in value_subjects]
        return []

    def return_publications_info(self, value_parsed:bs4.element.Tag) -> list:
        """
        Method which is dedicated to return information about the 
        Input:  value_parsed = parsed previously value
        Output: list with format of the publications
        """
        value_publications_info = value_parsed.find('div', {'id':'block-views-publications-by-lecturer-block'})
        if value_publications_info:
            value_publications_info = value_publications_info.find(class_='view-id-publications_by_lecturer')
            value_publications_info = [self.remove_spaces(v) for v in value_publications_info.text.split('\n')]
            return [v for v in value_publications_info if v]
        return []

    def return_scientific_directions(self, value_parsed:bs4.element.Tag) -> list:
        """
        Method which is dedicated to return scientific directions of the lecturer
        Input:  value_parsed = parsed previously page
        Output: list of the 
        """
        value_scientific_directions = value_parsed.find('div', {'id':'block-views-a8d2aa34f6c1a0321bd21a41ba6252d5'})
        if value_scientific_directions:
            value_scientific_directions = value_scientific_directions.find(class_='view-research-areas-by-lecturer')
            value_scientific_directions = value_scientific_directions.find('table')
            value_scientific_directions = value_scientific_directions.find_all('tr')
            value_scientific_directions = [v.find_all('td') for v in value_scientific_directions]
            value_scientific_directions = [v for v in value_scientific_directions if v]
            return [[self.remove_spaces(k.text.replace('\n', '')) for k in v] for v in value_scientific_directions]
        return []

    def proceed_parse(self, link:str) -> None:
        """
        Method which is dedicated to procced parsing of the current link in cases
        Input:  link = link of the
        Output: we successfully saved parsed value in 
        """
        value_info = []
        value_names, value_links = self.proceed_links(link)
        if value_names and value_links:
            for value_link in value_links:
                value_html = self.develop_request(value_link)
                value_dictionary = {}
                if value_html:
                    value_parsed = BeautifulSoup(value_html, 'html.parser')
                    value_contact = value_parsed.find(class_='mmsa-column3 mmsa-secondary-content')
                    value_contact = value_contact.find(class_='block block-ds-extras')
                    value_contact = value_contact.find_all(class_='mmsa-content-container')[-1]
                    
                    value_photo = self.return_photo(value_contact)
                    value_email = self.return_email(value_contact)
                    value_phone = self.return_phone(value_contact)
                    value_homeplace = self.return_homeplace(value_contact)
                    
                    value_parsed_info = value_parsed.find(class_='group-header mmsa-column12')
                    value_status = self.return_status(value_parsed_info)
                    value_accomplishments = self.return_accomplishments(value_parsed_info)
                    value_accolodates = self.return_accolodates(value_parsed_info)
                    value_work_position = self.return_work_position(value_parsed_info)

                    value_subjects_lections = self.return_subjects_lections(value_parsed)
                    value_scientific_directions = self.return_scientific_directions(value_parsed)
                    value_publications_info = self.return_publications_info(value_parsed)
                    value_subjects_practices = self.return_subjects_practice(value_parsed)
                    
                    value_dictionary = self.develop_special_occassions(value_dictionary)
                    #TODO add to one pattern of the phone
                    #TODO add to one pattern of the homespace
                    #TODO add to one pattern of the work position
                value_info.append(value_dictionary)
            df = pd.read_json(json.dumps(value_info))
            df_name = self.driver_csv.get_name_csv(mmsa.df_iasa_mmsa)
            df_path = self.driver_csv.get_path(self.driver_csv.path_csv, df_name)
            self.driver_csv.save_df(df, df_path)

                
    def develop_special_occassions(self, value_info:dict) -> dict:
        """
        Method which is dedicated to react in cases of the specific purposes
        Input:  value_info = list with parsed values
        Output: value_info but it resended its flaws
        """
        #TODO insert from the biography values from theit possible values
        return value_info




if __name__ == "__main__":
    a = ParseIasaSp()
    v = a.proceed_parse(link_iasa_personal_sp)
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    # a = ParseIasaMmsa()
    # v = a.proceed_parse(link_iasa_personal_mmsa)