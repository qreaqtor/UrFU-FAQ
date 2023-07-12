import ArticleView from '../view/article-view.js';
import ArticlesListView from '../view/articles-list-view.js';
import ThemesListView from '../view/themes-list-view.js';
import ThemeView from '../view/theme-view.js';
import LoginView from '../view/login-view.js';
import SignUpView from '../view/sign-up-view.js';
import LoadArticleView from '../view/load-article-view.js';
import MainContainerView from '../view/main-container-view.js';
import ProfileView from '../view/profile-view.js';
import { render } from '../render.js';


export default class BoardPresenter {
  constructor (mainContainer) {
    this.articlesList = new ArticlesListView();
    this.themesList = new ThemesListView();
    this.mainContainer = new MainContainerView();
    this.loadArticle = new LoadArticleView();
    this.login = new LoginView();
    this.signUp = new SignUpView();
    this.profile = new ProfileView();
    this.mainWrapper = document.querySelector('.main__wrapper');
  }

  init (themeModel) {
    this.themeModel = themeModel;
    this.themes = this.themeModel.themesList;


    render(this.mainContainer, this.mainWrapper)
    render(this.themesList, this.mainContainer.getElement());

    let i = 0;
    for (const theme of this.themes) {
      const themeView = new ThemeView(theme, i++);
      render(themeView, this.themesList.getElement());
      themeView.setListener(this.switchTheme(i));
      
    }

    render(this.articlesList, this.mainContainer.getElement());
    this.loadArticle.init();
    this.profile.init();
    this.login.init(this.switchToSignUpPage);
    this.signUp.init(this.switchToLoginPage);
  }


  switchToOtherPage = (pageNumber) => {
    if (pageNumber == 0) {
      this.mainWrapper.innerHTML = '';
      render(this.mainContainer, this.mainWrapper)
    }
    if (pageNumber == 1) {
      this.mainWrapper.innerHTML = '';
      render(this.loadArticle, this.mainWrapper);
    }
    if (pageNumber == 2) {
      this.mainWrapper.innerHTML = '';

      // логика запроса
      fetch('/users/me')
        .then(response => {
          if (response.status === 200) {
            return response.json();
          } else {
            throw new Error('Ошибка при выполнении запроса');
          }
        })
        .then(data => {
          render(this.profile, this.mainWrapper);
        })
        .catch(error => {
          render(this.signUp, this.mainWrapper);
          console.error(error);
        });
    }
  }


  switchToLoginPage = () => {
    this.mainWrapper.innerHTML = '';
    render(this.login, this.mainWrapper);
  }
  switchToSignUpPage = () => {
    this.mainWrapper.innerHTML = '';
    render(this.signUp, this.mainWrapper);
  }

  
  // исправил отображение ответов должно работать
  // очень важно работать с this.themes так у него вложенная структура 
  // в каждой теме массив questions соответвующей теме по id
  // в каждом вопросе массив answers cоответвующей теме по id
  // в this.themesModel.questions.filter(x => x.topic_id == theme) 
  // были только вопросы а поля answer не было из-за чего у нас не получилось их отрисовать
  switchTheme = (themeId) => {
    return () => {
      this.articlesList.removeArticles();
      const themeTrueId = this.themes[themeId-1]["id"];
      const theme = this.themes.filter(x => x.id == themeTrueId)[0];
      for (const question of theme.questions) {
        render(new ArticleView(question), this.articlesList.getElement());
      }
    }
  }


  // записать получение вопросов с сервера
  // гриша сказал что с сервера приходит список QuestionOut 
  // поэтому я постарался сразу под него все подстроить
  // и ответы на вопросы искать в this.themeModel.answers 
  async getSearchQuestions() {
    const search_data = document.querySelector('.header__search input').value;
  
    try {
      const response = await fetch('/search/' + search_data);
    
      if (response.status === 200) {
        const data = await response.json();
        let questions = data;
  
        questions = questions.map((x, i) => ({
          id: x.id,
          user_id: x.user_id,
          topic_id: x.topic_id,
          question: x.question,
          date_created: x.date_created,
          answers: Array.from({ length: this.themeModel.answers.length })
            .map((y, j) => this.themeModel.answers[j])
            .filter((y) => y.question_id == x.id)      
        }));
  
        return questions;
      } else {
        throw new Error('Ошибка при выполнении запроса');
      }
    } catch (error) {
      console.error(error);
    }
  }

  
  // отрисовывает вопросы на странице
  setSearchQuestions() {
    return async () => {
      const questions = await this.getSearchQuestions();
      this.switchToOtherPage(0);
      this.articlesList.removeArticles();
      for (const question of questions) {
        render(new ArticleView(question), this.articlesList.getElement());
      }
    }
  }
}