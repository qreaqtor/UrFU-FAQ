import { createElement } from '../render.js';


const createTemplate = (profile) => (
   `<div class="main__profile profile">
      <p class="profile__title">Личные данные</p>
      <div class="profile__data">
        <div class="profile__first-name">
          <p class="profile__first-name-text profile__text">Имя</p>
          <input class="profile__first-name-input profile__input" type="text" name="profile__first-name-input" placeholder="введите ваше имя..." value="${profile.name}">
        </div>
        <div class="profile__second-name">
          <p class="profile__second-name-text profile__text">Фамилия</p>
          <input class="profile__second-name-input profile__input" type="text" name="profile__second-name-input" placeholder="введите вашу фамилию..." value="${profile.surname}">
        </div>
        <div class="profile__email">
          <p class="profile__email-text profile__text">Электронная почта</p>
          <input class="profile__email-inpu profile__input" type="email" name="profile__email-input" placeholder="введите вашу почту..." value="${profile.email}">
        </div>
      </div>
      <button class="profile__button" type="submit">Сохранить</button>
    </div>`
  );


export default class ArticleView {
  init() {
    
  }

  getTemplate () {
    this.profile = this.getProfileDate();
    return createTemplate(this.profile);
  }

  getElement() {
    if (!this.element){
      this.element = createElement(this.getTemplate());
    }

    return this.element;
  }

  // запрос на проверку авторизации пользователя
  getAuthorizationCode = () => {
    return 200;
  }

  // получение данных пользователя
  getProfileDate = () => {
    return {
      name: "Иван",
      surname: "Иванов",
      email: "ivan.ivanov@gmail.com",
      hashed_password: "123",
      is_active: true,
      is_superuser: false,
      is_verified: false
    }
  }

  removeElement() {
    this.element = null;
  }
}