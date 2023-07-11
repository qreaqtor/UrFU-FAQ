import {createElement} from '../render.js';

const createTemplate = (theme) => (
  `<li class="main__themes-item">
    <a class="main__themes-item-link" href="#">${theme.title}</a>
  </li>`
);


export default class ThemeView {
  constructor(theme, themeNumber) {
    this.theme = theme;
    this.getElement().addEventListener('click', this.setTheme(themeNumber));
  }

  getTemplate() {
    return createTemplate(this.theme);
  }

  getElement() {
    if (!this.element) {
      this.element = createElement(this.getTemplate());
    }

    return this.element;
  }

  setListener(callBack) {
    this.element.addEventListener('click', callBack) // не очень хорошо
  }

  setTheme(themeNumber) {
    return () => {
      const themeElements = document.querySelectorAll('.main__themes-item');
      for (const themeElement of themeElements) {
        themeElement.classList.remove('main__themes-item-active');
      }
      themeElements[themeNumber].classList.add('main__themes-item-active');
    };
  }

  removeElement() {
    this.element = null;
  }
}