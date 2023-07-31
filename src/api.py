import requests
import configparser

config = configparser.ConfigParser()
config.read('config.ini')


class HeadHunter:
    api = config.get('API', 'api_url')
    employers = config.get('EMPLOYERS', 'employer_ids').split(',')


    @classmethod
    def get_vacancies(cls):
        vacancies = []
        for employer in HeadHunter.employers:
            response = requests.get(HeadHunter.api, params={'employer_id': employer, 'only_with_salary': 'True'})
            vacancies = vacancies + response.json()['items']
        return vacancies

    @classmethod
    def get_employers_info(cls):
        employers = []
        for employer in HeadHunter.employers:
            response = requests.get(f'https://api.hh.ru/employers/{employer}')
            resp_list = [response.json()]
            employers = employers + resp_list
        return employers
