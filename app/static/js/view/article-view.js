import { createElement } from '../render.js';

const createAnswersTeamplate = (answers) => {
  let result = '';
  for (let answer of answers) {
    result += `
    <div class="article__text">
      ${answer.answer}
    </div>`
  }
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

    <div class="article__date">${getNormalDate(question.date_created)}</div>
  </li>`
);


export default class ArticleView {
  constructor(question) {
    this.question = question;
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

  removeElement() {
    this.element = null;
  }
}