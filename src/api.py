import requests


class HeadHunter:
    api = 'https://api.hh.ru/vacancies'
    employers = ('1740', '78638',
                 '3009025', '1868342',
                 '652744', '9739229',
                 '5714322', '9632510',
                 '9288781', '23040')

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
