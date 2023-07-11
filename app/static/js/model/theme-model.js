export default class ThemeModel {
  init(themes, questions, answers) {
    this.themes = themes;
    this.questions = questions;
    this.answers = answers;
    this.themesList = [];
    this.getThemesList();
  }

  getThemesList() { // переделать получше, выглядит ужасно, но работает.....        
    for (let theme of this.themes) {
      this.themesList.push({
        id: theme.id,
        title: theme.title,
        questions: Array.from({ length: this.questions.length })
          .map((x, i) => this.questions[i])
          .filter((x) => x.topic_id == theme.id)
          .map((x, i) => ({
            id: x.id,
            user_id: x.user_id,
            topic_id: x.topic_id,
            question: x.question,
            date_created: x.date_created,
            answers: Array.from({ length: this.answers.length })
              .map((y, i) => this.answers[i])
              .filter((y) => y.question_id == x.id)
          }))
      });
    }
  }

  getThemes() {
    return this.themes;
  }
}