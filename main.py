from src.api import HeadHunter
from src.cls import DBManager
from psycopg2.errors import DuplicateTable


if __name__ == "__main__":

    print('''Эта программа предназначена для работы с вакансиями, хранящимися в базе данных.
Выберите, указав цифру, что хотите сделать или напишите "выйти", чтобы закончить сеанс.\n
1. Получить список всех компаний и количество вакансий в каждой компании;
2. Получить список всех вакансий с указанием названия компании, названия вакансии и зарплаты, а также ссылки на вакансию;
3. Получить среднюю зарплату по вакансиям;
4. Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям;
5. Получить список всех вакансий, в названии которых содержатся переданные в метод слова, например "python".

Загрузка...''')

    try:
        connection, cursor = DBManager.get_connection()
        DBManager.create_tables(cursor)
        DBManager.get_emp_data_saved(cursor, HeadHunter.get_employers_info())
        DBManager.get_vac_data_saved(cursor, HeadHunter.get_vacancies())
        connection.commit()
    except DuplicateTable:
        connection, cursor = DBManager.get_connection()

    while True:
        user_choice = input('\nВаш выбор: ').lower()

        if user_choice == 'выйти':

            connection.close()
            print('\nВы вышли из программы. Сеанс завершен.')
            break

        elif int(user_choice) == 1:

            print('\nВыгружаем информацию по вашему запросу...\n')
            for info in DBManager.get_companies_and_vacancies_count(cursor):
                print(f'Название компании: {info[0]}. Кол-во вакансий: {info[1]}.')
            print('\nЧто-то ещё?')

        elif int(user_choice) == 2:

            print('\nВыгружаем информацию по вашему запросу...')
            for info in DBManager.get_all_vacancies(cursor):
                print(f'''\nНазвание компании: {info[0]}. 
Название вакансии: {info[1]}.
Размер зарплаты: {info[2]} руб.
Ссылка на вакансию: {info[3]}.''')
            print('\nЧто-то ещё?')

        elif int(user_choice) == 3:

            print('\nВыгружаем информацию по вашему запросу...\n')
            print(f'Средняя зарплата по вакансиям: {DBManager.get_avg_salary(cursor)} руб.')
            print('\nЧто-то ещё?')

        elif int(user_choice) == 4:

            print('\nВыгружаем информацию по вашему запросу...')
            for info in DBManager.get_vacancies_with_higher_salary(cursor):
                print(f'''\nНазвание компании: {info[0]}. 
Название вакансии: {info[1]}.
Размер зарплаты: {info[2]} руб.
Ссылка на вакансию: {info[3]}.''')
            print('\nЧто-то ещё?')

        elif int(user_choice) == 5:
            keyword = input('\nВведите ключевое слово: ')
            print('\nВыгружаем информацию по вашему запросу...')
            vacancies_with_keyword = DBManager.get_vacancies_with_keyword(cursor, keyword)

            if len(vacancies_with_keyword) == 0:
                print('\nТаких вакансий нет.')
            else:
                for info in vacancies_with_keyword:
                    print(f'''\nНазвание компании: {info[0]}. 
Название вакансии: {info[1]}.
Размер зарплаты: {info[2]} руб.
Ссылка на вакансию: {info[3]}.''')

            print('\nЧто-то ещё?')

        else:
            print('\nВы указали не существующий вариант выбора. Попробуйте ещё раз!')


