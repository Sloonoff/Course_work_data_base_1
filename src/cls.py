import psycopg2
from decimal import Decimal


class DBManager:

    @classmethod
    def get_connection(cls):
        connection = psycopg2.connect(host='localhost', database='CW_DB', user='postgres', password='Nodar126')
        cur = connection.cursor()
        return connection, cur

    @classmethod
    def create_tables(cls, cur):
        cur.execute('CREATE TABLE employers'
                    '('
                    '     employer_id int PRIMARY KEY,'
                    '     employer_name varchar(255),'
                    '     vacancies_count int'
                    ');'
                    ''
                    'CREATE TABLE vacancies'
                    '('
                    '     vacancy_id int PRIMARY KEY,'
                    '     employer_id int REFERENCES employers(employer_id),'
                    '     vacancy_name varchar(255),'
                    '     vacancy_salary int,'
                    '     vacancy_url varchar(255)'
                    ');')

    @classmethod
    def get_companies_and_vacancies_count(cls, cur):
        """Получаем список всех компаний и количество вакансий у каждой компании."""
        cur.execute('SELECT employer_name, vacancies_count FROM employers')
        companies_and_vacancies = cur.fetchall()
        return companies_and_vacancies

    @classmethod
    def get_all_vacancies(cls, cur):
        """Получает список всех вакансий с указанием названия компании, названия вакансии
         и зарплаты и ссылки на вакансию."""
        cur.execute('SELECT employer_name, vacancy_name, vacancy_salary, vacancy_url FROM vacancies '
                    'JOIN employers USING (employer_id)')
        all_vacancies = cur.fetchall()
        return all_vacancies

    @classmethod
    def get_avg_salary(cls, cur):
        """Получаем среднюю зарплату по вакансиям."""
        cur.execute('SELECT AVG(vacancy_salary) FROM vacancies')
        avg_salary = cur.fetchall()[0][0]
        avg_salary = Decimal(avg_salary)
        return avg_salary.quantize(Decimal("1.00"))

    @classmethod
    def get_vacancies_with_higher_salary(cls, cur):
        """Получаем список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        cur.execute('SELECT employer_name, vacancy_name, vacancy_salary, vacancy_url FROM vacancies '
                    'JOIN employers USING (employer_id)'
                    'WHERE vacancy_salary > (SELECT AVG(vacancy_salary) FROM vacancies)')
        high_sal_vac = cur.fetchall()
        return high_sal_vac

    @classmethod
    def get_vacancies_with_keyword(cls, cur, keyword):
        """Получаем список всех вакансий, в названии которых содержатся переданные
         в метод слова, например 'python'."""
        cur.execute("SELECT employer_name, vacancy_name, vacancy_salary, vacancy_url FROM vacancies "
                    "JOIN employers USING (employer_id) "
                    f"WHERE vacancy_name LIKE '%{keyword}%'")
        vacancies_with_keyword = cur.fetchall()
        return vacancies_with_keyword

    @classmethod
    def get_emp_data_saved(cls, cur, employers):
        cur.execute('SELECT employer_id FROM employers')
        employers_in_db = cur.fetchall()

        for employer_in_db in range(len(employers_in_db)):
            employers_in_db[employer_in_db] = employers_in_db[employer_in_db][0]

        for employer in employers:
            if int(employer['id']) not in employers_in_db:
                info = (employer['id'], employer['name'], employer['open_vacancies'])
                cur.execute('INSERT INTO employers VALUES (%s, %s, %s)', tuple(info))

    @classmethod
    def get_vac_data_saved(cls, cur, vacancies):
        cur.execute('SELECT vacancy_id FROM vacancies')
        vacs_in_db = cur.fetchall()

        for vac_in_db in range(len(vacs_in_db)):
            vacs_in_db[vac_in_db] = vacs_in_db[vac_in_db][0]

        for vacancy in vacancies:

            if int(vacancy['id']) in vacs_in_db:
                continue
            else:
                if vacancy['salary']['to'] is None:

                    if vacancy['salary']['currency'] != 'RUR':
                        vac_salary = str(int(vacancy['salary']['from']) * 90)
                    else:
                        vac_salary = str(vacancy['salary']['from'])

                elif vacancy['salary']['currency'] != 'RUR':
                    vac_salary = str(int(vacancy['salary']['to']) * 90)

                else:
                    vac_salary = str(vacancy['salary']['to'])

                info = (vacancy['id'], vacancy['employer']['id'], vacancy['name'], vac_salary, vacancy['alternate_url'])
                cur.execute('INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s)', tuple(info))
