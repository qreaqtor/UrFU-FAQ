import { createElement } from '../render.js';


const createTemplate = () => (
   `<div class="main__login login">
      <div class="login__title">Вход</div>
      <div class="login__email login__input-block">
        <p class="login__email-text login__text">Электронная почта</p>
        <input class="login__email-input login__input" type="email" name="login__email-input" placeholder="введите вашу почту...">
      </div>
      <div class="login__password login__input-block">
        <p class="login__password-text login__text">Пароль</p>
        <input class="login__password-input login__input" type="password" name="login__password-input" placeholder="введите пароль...">
      </div>

      <button class="login__button" type="submit" name="login__button">Войти</button>
      <div class="login__hint">
        <div class="login__hint-text">нет аккаунта?</div>
        <div class="login__hint-link"><a href="#">нажми сюда</a></div>
      </div>
    </div>`
  );


export default class LoginView {
  init(callback) {
    this.getElement().querySelector('.login__hint-link').addEventListener('click', callback);
    // Код Алексея
    this.element.querySelector('.login__button').addEventListener('click', this.onLoginButton);
  }


  getTemplate() {
    return createTemplate();
  }


  getElement() {
    if (!this.element){
      this.element = createElement(this.getTemplate());
    }
    return this.element;
  }

  // обработчик на кнопке Код Алексея
  onLoginButton(event) {
    event.preventDefault(); 

    var email = document.querySelector('.login__email-input').value;
    var password = document.querySelector('.login__password-input').value;

    // Создаем объект FormData и добавляем в него значения полей ввода
    var formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);

    // Создаем объект запроса
    var request = new XMLHttpRequest();
    request.open('POST', '/auth/jwt/login'); // возможно нужно изменить путь
    request.send(formData);

    // Обработка ответа сервера (вы можете настроить свою логику обработки здесь)
    request.onload = function() {
      if (request.status === 204) {
        alert("Успешный вход")
      } else {
        alert("Неудачный вход, попробуйте ещё раз")
      }
    };
  }

  removeElement() {
    this.element = null;
  }
}