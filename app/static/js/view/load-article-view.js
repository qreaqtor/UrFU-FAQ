import { createElement } from '../render.js';


const createTemplate = () => (
   `<div class="main__load-article-container">
      <div class="main__load-article load-article">
        <div class="load-arctile__name">
          <input class="load-article__name-input" type="text" name="load-article__name-input" placeholder="введите название вопроса...">
        </div>
        <div class="load-article__text">
          <textarea class="load-article__textarea" name="load-article__textarea" placeholder="введите содержание вопроса"></textarea>
        </div>
      </div>
      <button class="main__load-article-button" type="submit" name="main__load-article-button">Опубликовать</button>  
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
    event.preventDefault()

    const question = document.querySelector('.load-article__name-input').value;
    const answer = document.querySelector('.load-article__textarea').value;

    const url = "/new_question";
    const data = {
      "question": question
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
        alert('Что-то пошло не так:\n' + jsonData)
      } else {
        alert('Успешно создан вопрос!')
      }
    })
    .catch(error => {
      alert(error);
    });
  }

  removeElement() {
    this.element = null;
  }
}
