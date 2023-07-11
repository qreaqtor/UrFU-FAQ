import { createElement } from '../render.js';


const createTemplate = () => (
   `<div class="main__load-article-container">
      <div class="main__load-article load-article">
        <div class="load-arctile__name">
          <input class="load-article__name-input" type="text" name="load-article__name-input" placeholder="введите название статьи...">
        </div>
        <div class="load-article__text">
          <textarea class="load-article__textarea" name="load-article__textarea" placeholder="введите содержание статьи"></textarea>
        </div>
      </div>
      <button class="main__load-article-button" type="submit" name="main__load-article-button">Загрузить</button>  
    </div>`
  );


export default class LoadArticleView {
  init() {
    this.getElement().querySelector('.main__load-article-button').addEventListener('click', this.onLoadArticleButton);
  }

  getTemplate () {
    return createTemplate();
  }

  getElement() {
    if (!this.element){
      this.element = createElement(this.getTemplate());
    }

    return this.element;
  }

  // обработчик на кнопку загрузки
  onLoadArticleButton(event) {
    event.preventDefault();

    var question = document.querySelector('.load-article__name-input').value;
    var answer = document.querySelector('.load-article__textarea').value;

    // как дальше писать запрос я не знаю
  }

  removeElement() {
    this.element = null;
  }
}