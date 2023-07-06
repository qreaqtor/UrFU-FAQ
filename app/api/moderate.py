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

def get_moderate(text):
    moderate = f'''
    Тематика сайта: поступление в вуз и первокурсники.

    {text}
    
    Оцените текст по следующим критериям:
    1. Подходит ли текст по тематике сайта, связан ли он с вопросами и ответами о поступлении в вуз и опытом первокурсников?
    2. Соответствует ли текст правилам и политике вашего сайта?
    3. Не содержит ли текст матерных выражений, оскорблений или ругательных слов?

    Пожалуйста, оцените текст следующим образом:
    - Если текст полностью соответствует тематике сайта, не нарушает правила и не содержит запрещенного содержания, поставьте оценку 1.
    - Если текст не соответствует тематике сайта, нарушает правила или содержит запрещенное содержание, поставьте оценку 0.
    '''
    prompt = moderate
    response = ask_chatgpt(prompt)
    return False if response == '0' else True
