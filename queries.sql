CREATE TABLE employers
(
    employer_id int PRIMARY KEY,
    employer_name varchar(255),
    vacancies_count int
);

CREATE TABLE vacancies
(
    vacancy_id int PRIMARY KEY,
    employer_id int REFERENCES employers(employer_id),
    vacancy_name varchar(255),
    vacancy_salary int,
    vacancy_url varchar(255)
);

SELECT employer_name, vacancies_count FROM employers;

SELECT employer_name, vacancy_name, vacancy_salary, vacancy_url FROM vacancies
JOIN employers USING (employer_id);

SELECT AVG(vacancy_salary) FROM vacancies;

SELECT employer_name, vacancy_name, vacancy_salary, vacancy_url FROM vacancies
JOIN employers USING (employer_id)
WHERE vacancy_salary > (SELECT AVG(vacancy_salary) FROM vacancies);

SELECT employer_name, vacancy_name, vacancy_salary, vacancy_url FROM vacancies
JOIN employers USING (employer_id)
WHERE vacancy_name LIKE '%keyword%';