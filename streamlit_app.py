import os
import openai
import streamlit as st
from dotenv import load_dotenv

from parse_hh import get_candidate_info, get_job_description

# Попытка загрузить переменные из .env (для локальной разработки)
load_dotenv()

# Получение API-ключа 
# Приоритет: переменные Streamlit Cloud, затем .env
client = openai.Client(
    api_key=st.secrets.get('OPENAI_API_KEY') or os.getenv('OPENAI_API_KEY')
)


# Системный промпт
SYSTEM_PROMPT = """
Проскорь кандидата, насколько он подходит для данной вакансии.

Сначала напиши короткий анализ, который будет пояснять оценку.
Отдельно оцени качество заполнения резюме (понятно ли, с какими задачами сталкивался кандидат и каким образом их решал?). Эта оценка должна учитываться при выставлении финальной оценки - нам важно нанимать таких кандидатов, которые могут рассказать про свою работу
Потом представь результат в виде оценки от 1 до 10.
""".strip()

# Функция для запроса к GPT
def request_gpt(system_prompt, user_prompt):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=1000,
        temperature=0,
    )
    return response.choices[0].message.content

# Заголовок приложения
st.title("CV Scoring App")

# Поля ввода для URL вакансии и резюме
job_description_url = st.text_area("Enter the job description url")
cv_url = st.text_area("Enter the CV url")

# Кнопка для scoring
if st.button("Score CV"):
    with st.spinner("Scoring CV..."):
        # Проверка, что оба URL введены
        if not job_description_url or not cv_url:
            st.error("Пожалуйста, введите URL вакансии и резюме")
        else:
            try:
                # Получение описания вакансии и резюме
                job_description = get_job_description(job_description_url)
                cv = get_candidate_info(cv_url)

                # Отображение распаршенных данных
                st.subheader("Описание вакансии:")
                st.write(job_description)
                
                st.subheader("Резюме кандидата:")
                st.write(cv)

                # Формирование промпта для GPT
                user_prompt = f"# ВАКАНСИЯ\n{job_description}\n\n# РЕЗЮМЕ\n{cv}"
                
                # Получение оценки от GPT
                response = request_gpt(SYSTEM_PROMPT, user_prompt)

                # Отображение результата
                st.subheader("Оценка соответствия:")
                st.write(response)

            except Exception as e:
                st.error(f"Произошла ошибка при обработке: {e}")