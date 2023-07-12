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
    <div class="article__answers">
      
    </div>
    <div class="article__date">${getNormalDate(question.date_created)}</div>
  </li>`
);


export default class ArticleView {
  constructor(question) {
    this.question = question;
    this.getElement();
    this.element.addEventListener('click', this.onArticle());
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
      if (this.isAnswersRender) {
        this.getElement().querySelector('.article__answers').innerHTML = '';
      } else {
        this.getElement().querySelector('.article__answers').innerHTML = createAnswersTeamplate(this.question.answers);
      }

      this.isAnswersRender = !this.isAnswersRender;
    }
  }

  removeElement() {
    this.element = null;
  }
}