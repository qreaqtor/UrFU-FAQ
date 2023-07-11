import {createElement} from '../render.js';

const createTemplate = () => (
  `<ul class="main__articles">
  </ul>`
);


export default class ArticlesListView {
  getTemplate() {
    return createTemplate;
  }

  getElement() {
    if (!this.element) {
      this.element = createElement(this.getTemplate());
    }

    return this.element;
  }

  removeArticles() {
    this.getElement().innerHTML = '';
  }

  removeElement() {
    this.element = null;
  }
}