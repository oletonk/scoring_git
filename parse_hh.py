import requests
from bs4 import BeautifulSoup

def get_html(url: str):
    """
    Получение HTML-страницы с указанием User-Agent
    """
    return requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        },
    )

def extract_candidate_data(html):
    """
    Извлечение данных о кандидате из HTML
    """
    soup = BeautifulSoup(html, 'html.parser')

    # Извлечение основных данных кандидата
    name = soup.find('h2', {'data-qa': 'bloko-header-1'}).text.strip()
    gender_age = soup.find('p').text.strip()
    location = soup.find('span', {'data-qa': 'resume-personal-address'}).text.strip()
    job_title = soup.find('span', {'data-qa': 'resume-block-title-position'}).text.strip()
    job_status = soup.find('span', {'data-qa': 'job-search-status'}).text.strip()

    # Извлечение опыта работы
    experience_section = soup.find('div', {'data-qa': 'resume-block-experience'})
    experience_items = experience_section.find_all('div', class_='resume-block-item-gap')
    experiences = []
    for item in experience_items:
        period = item.find('div', class_='bloko-column_s-2').text.strip()
        duration = item.find('div', class_='bloko-text').text.strip()
        period = period.replace(duration, f" ({duration})")

        company = item.find('div', class_='bloko-text_strong').text.strip()
        position = item.find('div', {'data-qa': 'resume-block-experience-position'}).text.strip()
        description = item.find('div', {'data-qa': 'resume-block-experience-description'}).text.strip()
        experiences.append(f"**{period}**\n\n*{company}*\n\n**{position}**\n\n{description}\n")

    # Извлечение ключевых навыков
    skills_section = soup.find('div', {'data-qa': 'skills-table'})
    skills = [skill.text.strip() for skill in skills_section.find_all('span', {'data-qa': 'bloko-tag__text'})]

    # Формирование строки в формате Markdown
    markdown = f"# {name}\n\n"
    markdown += f"**{gender_age}**\n\n"
    markdown += f"**Местоположение:** {location}\n\n"
    markdown += f"**Должность:** {job_title}\n\n"
    markdown += f"**Статус:** {job_status}\n\n"
    markdown += "## Опыт работы\n\n"
    for exp in experiences:
        markdown += exp + "\n"
    markdown += "## Ключевые навыки\n\n"
    markdown += ', '.join(skills) + "\n"

    return markdown

def extract_vacancy_data(html):
    """
    Извлечение данных о вакансии из HTML
    """
    soup = BeautifulSoup(html, "html.parser")

    # Извлечение заголовка вакансии
    title = soup.find("h1", {"data-qa": "vacancy-title"})
    title = title.text.strip() if title else "Название вакансии не указано"

    # Извлечение зарплаты
    salary = soup.find("span", {"data-qa": "vacancy-salary-compensation-type-net"})
    salary = salary.text.strip() if salary else "Зарплата не указана"

    # Извлечение опыта работы
    experience = soup.find("span", {"data-qa": "vacancy-experience"})
    experience = experience.text.strip() if experience else "Опыт работы не указан"

    # Извлечение типа занятости и режима работы
    employment_mode = soup.find("p", {"data-qa": "vacancy-view-employment-mode"})
    employment_mode = employment_mode.text.strip() if employment_mode else "Тип занятости не указан"

    # Извлечение компании
    company = soup.find("a", {"data-qa": "vacancy-company-name"})
    company = company.text.strip() if company else "Компания не указана"

    # Извлечение местоположения
    location = soup.find("p", {"data-qa": "vacancy-view-location"})
    location = location.text.strip() if location else "Местоположение не указано"

    # Извлечение описания вакансии
    description = soup.find("div", {"data-qa": "vacancy-description"})
    description = description.text.strip() if description else "Описание отсутствует"

    # Извлечение ключевых навыков
    skills = [
        skill.text.strip()
        for skill in soup.find_all(
            "div", {"class": "magritte-tag__label___YHV-o_3-0-3"}
        )
    ]

    # Формирование строки в формате Markdown
    markdown = f"""
# {title}

**Компания:** {company}
**Зарплата:** {salary}
**Опыт работы:** {experience}
**Тип занятости и режим работы:** {employment_mode}
**Местоположение:** {location}

## Описание вакансии
{description}

## Ключевые навыки
{', '.join(skills) if skills else 'Ключевые навыки не указаны'}
"""

    return markdown.strip()

def get_candidate_info(url: str):
    """
    Получение информации о кандидате по URL
    """
    response = get_html(url)
    return extract_candidate_data(response.text)

def get_job_description(url: str):
    """
    Получение описания вакансии по URL
    """
    response = get_html(url)
    return extract_vacancy_data(response.text)

# Пример использования
if __name__ == "__main__":
    # Раскомментируйте и замените на реальные URLs
    candidate_url = "https://hh.ru/resume/8c6ecc6300060770a10039ed1f7a51787a5068"
    vacancy_url = "https://hh.ru/vacancy/116909477"
    
    print(get_candidate_info(candidate_url))
    print(get_job_description(vacancy_url))