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

const createTemplate = (question) => (
 `<li class="main__article article">
    <div class="article__name">
      <p class="aticle__name-text">${question.question}</p>
    </div>
    ${createAnswersTeamplate(question.answers)}
    <div class="article__date">${question.date_created}</div>
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