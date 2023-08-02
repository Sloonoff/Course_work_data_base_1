import requests


class HeadHunter:
    api = 'https://api.hh.ru/vacancies'
    employers = ('1740', '2180', '3529', '3112647', '362', '3093544', '22494', '78638', '54', '87021')

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
