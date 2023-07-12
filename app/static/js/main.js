import MenuView from './view/menu-view.js';
import BoardPresenter from './presenter/board-presenter.js';
import ThemeModel from './model/theme-model.js';

import { getAnswers, getQuestions, getThemes } from './mock/themes.js';
import { getApiAnswers, getApiQuestions, getApiThemes } from './api/themes-api.js';
import { render } from './render.js';

const headerElement = document.querySelector('.header');
const mainElement = document.querySelector('.main');
const boardPresenter = new BoardPresenter(mainElement.querySelector('.main__container'));

const themeModel = new ThemeModel();
const menu = new MenuView();

render(menu, headerElement.querySelector('.header__container'));

async function initialize() {
    const themesResponse = await getApiThemes();
    const themes = JSON.parse(themesResponse);

    const questionsResponce = await getApiQuestions();
    const questions = JSON.parse(questionsResponce);

    const answersResponce = await getApiAnswers();
    const answers = JSON.parse(answersResponce);

    themeModel.init(themes, questions, answers);
    menu.init(boardPresenter.switchToOtherPage, boardPresenter.setSearchQuestions());
    boardPresenter.init(themeModel);
}

initialize();