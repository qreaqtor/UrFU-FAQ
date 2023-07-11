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

  init (themesModel) {
    this.themesModel = themesModel;
    this.themes = this.themesModel.themesList;


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
      if (this.profile.getAuthorizationCode() == 200) {
        render(this.profile, this.mainWrapper);
      } else {
        render(this.signUp, this.mainWrapper);
      }

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

  
  switchTheme = (themeId) => {
    return () => {
      this.articlesList.removeArticles();
      const theme = this.themes[themeId-1]["id"] // получаем id темы (например: 64aacb66d3a0225df0c46c41)
      for (const question of this.themesModel.questions.filter(x => x.topic_id == theme)) { // их всех вопросов мы проходимся только по вопросам, имеющие эту тему
        render(new ArticleView(question), this.articlesList.getElement()); //либо тут, либо где то в процессе создания объекта ArticleView выдаёт оишбку
      }
    }
  }
}