import openai
from app.core.config import AI_TOKEN

openai.api_key = AI_TOKEN

def ask_chatgpt(prompt):
    response = openai.Completion.create(
        engine='text-davinci-003',  # Выбираем модель движка, например, 'text-davinci-003'
        prompt=prompt,
        max_tokens=50,  # Максимальное количество токенов в ответе
        temperature=0.2,  # Контролирует степень случайности ответа (0.0 - детерминированный, 1.0 - случайный)
        n=1,  # Количество вариантов ответа, которые нужно сгенерировать
        stop=None,  # Опциональное условие остановки генерации ответа
        timeout=10  # Опциональное время ожидания ответа
    )
    
    if response and response.choices:
        return response.choices[0].text.strip()
    return ""

def get_moderate_question(question):
    moderate = f'''Тематика сайта: поступление в вуз и обучение первокурсников.
Текст: '{question}'
Оцените текст следующим образом:
1. Подходит ли текст по тематике сайта, связан ли он с вопросами об адаптации в ВУЗе и обучении первокурсников?
2. Соответствует ли текст правилам и политике вашего сайта?
3. Не содержит ли текст матерных выражений, оскорблений или ругательных слов?
4. Текст является информативным и релевантным?
5. Может ли первокурсника заинтересовать ответ на этот вопрос?.
Ставь за каждый пункт оценку 1, если текст соответствует, иначе 0.
Ответ должен быть в формате строки, содержащей только оценки, разделенные запятыми за каждый пункт, и не содержать ничего кроме этого.'''
    prompt = moderate
    response = ask_chatgpt(prompt)
    return [x == '1' for x in response.split(',')]


def get_moderate_answer(answer, question):
    moderate = f'''Тематика сайта: поступление в вуз и обучение первокурсников.
Текст: '{answer}'
Оцените текст следующим образом:
1. Подходит ли текст по тематике сайта, связан ли он с ответами об адаптации в ВУЗе и обучении первокурсников?
2. Соответствует ли текст правилам и политике вашего сайта?
3. Не содержит ли текст матерных выражений, оскорблений или ругательных слов?
4. Текст является информативным и релевантным?
5. Удовлетворяет ли этот ответ вопросу: '{question}'
Ставь за каждый пункт оценку 1, если текст соответствует, иначе 0.
Ответ должен быть в формате строки, содержащей только оценки, разделенные запятыми за каждый пункт, и не содержать ничего кроме этого.'''
    prompt = moderate
    response = ask_chatgpt(prompt)
    return [x == '1' for x in response.split(',')]

def get_moderate_topic(topics, question):
    moderate = f'''Выбери к какой теме отнести вопрос: {question}
Темы: {topics}
Если нет подходящей по смыслу темы, напиши свою.
Ответ должен содержать только название темы без знаков препинания.'''
    prompt = moderate
    response = ask_chatgpt(prompt)
    print(moderate)
    return response
