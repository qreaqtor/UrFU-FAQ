import {createElement} from '../render.js';

const createTemplate = () => (
  `<ul class="main__themes">
  </ul>`
);


export default class ThemesListView {
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