import {createElement} from '../render.js';

const createTemplate = () => (
  `<div class="main__continer">
  </div>`
);


export default class MainContainerView {
  getTemplate() {
    return createTemplate;
  }

  getElement() {
    if (!this.element) {
      this.element = createElement(this.getTemplate());
    }

    return this.element;
  }

  removeElement() {
    this.element = null;
  }
}