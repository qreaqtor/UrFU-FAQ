import {createElement} from '../render.js';

const createTemplate = () => (
 `<div class="header__menu">
    <div class="header__logo"><p>Практика</p></div>
    <div class="header__search">
      <input type="text" name="header-search" placeholder="поиск...">
    </div>
    <nav class="header__menu">
      <div class="header__menu-item header__menu-item-active"><a class="header__menu-item-link" href="#">статьи</a></div>
      <div class="header__menu-item"><a class="header__menu-item-link" href="#">создать</a></div>
      <div class="header__menu-item"><a class="header__menu-item-link" href="#">профиль</a></div>
    </nav>
  </div>`
);


export default class MenuView {
  init(menuCallback, searchCallback) {
    this.getElement();
    this.setListeners(menuCallback);
    this.element.querySelector('.header__search input').addEventListener('keydown', this.onSearch(searchCallback))
  }
  
  getTemplate() {
    return createTemplate;
  }

  getElement() {
    if (!this.element) {
      this.element = createElement(this.getTemplate());
    }

    return this.element;
  }

  setMenu(menuNumber, callback) {
    return () => {
      const menuElements = document.querySelectorAll('.header__menu-item');
      for (const menuElement of menuElements) {
        menuElement.classList.remove('header__menu-item-active');
      }
      menuElements[menuNumber].classList.add('header__menu-item-active');
      callback(menuNumber);
    };
  }

  setListeners(callback) {
    const menuElements = document.querySelectorAll('.header__menu-item');
    let i = 0;
    for (const menuElement of menuElements) {
      menuElement.addEventListener('click', this.setMenu(i++, callback));
    }
  }

  // обработчик события на поиске при копке Enter
  onSearch(callback) {
    return (event) => {
      if (event.code == "Enter") {
        callback();
      }
    }
  }

  removeElement() {
    this.element = null;
  }
}