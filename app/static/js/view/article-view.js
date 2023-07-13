import { createElement } from '../render.js';

const createAnswersTeamplate = (answers) => {
  let result = '';
  for (let answer of answers) {
    result += `
    <div class="article__text">
      ${answer.answer}
    </div>
    <div class="article__text-underline"></div>`
  }
  result += `
  <div class="article__load-answer">
    <textarea class="article__load-answer-textarea" name="article__load-answer-textarea" placeholder="добавить ответ на вопрос..."></textarea>
  </div>
  <button class="article__load-answer-button" type="submit" name="article__load-answer-button">Отправить</button>
  `
  return result;
};

const getNormalDate = (date) => { 
  return date.split('T')[0].split('-').reverse().join('.'); 
} // Ещё часовой пояс надо учитывать

const createTemplate = (question) => (
 `<li class="main__article article">
    <div class="article__name">
      <p class="aticle__name-text">${question.question}</p>
    </div>
    <div class="article__answers">
      
    </div>
    <div class="article__date">${getNormalDate(question.date_created)}</div>
  </li>`
);


export default class ArticleView {
  constructor(question) {
    this.question = question;
    this.getElement();
    this.onArticleFunc = this.onArticle();
    this.element.addEventListener('click', this.onArticleFunc);
    this.isAnswersRender = false;
  }

  getTemplate () {
    return createTemplate(this.question);
  }

  getElement() {
    if (!this.element){
      this.element = createElement(this.getTemplate());
    }

    return this.element;
  }

  onArticle() {
    return () => {
      this.element.querySelector('.article__answers').innerHTML = createAnswersTeamplate(this.question.answers);
      this.element.style.cursor = "auto";
      this.element.removeEventListener('click', this.onArticleFunc);

      this.element.querySelector('.article__load-answer-button').addEventListener('click', this.onLoadButton());
    }
  }

  onLoadButton() {
    return () => {
      const textarea = this.element.querySelector('.article__load-answer-textarea');

      const text = textarea.value;
      const question_id = this.question.id;

      const url = "/new_answer";
      const data = {
      "question_id": question_id,
      "answer": text
    };

    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
    .then(response => {
      if (response.ok) {
        return response.json(); // Получить JSON-объект из ответа
      } else {
        throw new Error(response.status + ' ' + response.statusText);
      }
    })
    .then(jsonData => {
      if ('criteria' in jsonData) {
        alert('Что-то пошло не так:\n' + jsonData.criteria.join('\n'))
      } else {
        textarea.value = '';
        alert('Успешно создан ответ!')
      }
    })
    .catch(error => {
      alert(error);
    });
    }
  }

  removeElement() {
    this.element = null;
  }
}