import openai
from app.core.config import AI_TOKEN

openai.api_key = AI_TOKEN

def ask_chatgpt(prompt):
    response = openai.Completion.create(
        engine='text-davinci-003',  # Выбираем модель движка, например, 'text-davinci-003'
        prompt=prompt,
        max_tokens=50,  # Максимальное количество токенов в ответе
        temperature=0.7,  # Контролирует степень случайности ответа (0.0 - детерминированный, 1.0 - случайный)
        n=1,  # Количество вариантов ответа, которые нужно сгенерировать
        stop=None,  # Опциональное условие остановки генерации ответа
        timeout=10  # Опциональное время ожидания ответа
    )
    
    if response and response.choices:
        return response.choices[0].text.strip()
    else:
        return ""

moderate = '''
Модерация поступления в вуз. Пожалуйста, проверьте текст на соответствие тематике сайта и правилам комментирования. Оцените текст: 1 если он подходит по тематике сайта и не нарушает правил, 0 если не подходит по тематике или нарушает правила.
'''

def get_moderate(text):
    prompt = moderate + text
    response = ask_chatgpt(prompt)
    return False if response == '0' else True
