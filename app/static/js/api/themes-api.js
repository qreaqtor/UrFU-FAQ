const getApiThemes = () => {
    return new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest();
      xhr.open('GET', '/all_topics/');
      xhr.onload = function() {
        if (xhr.status === 200) {
          const response = xhr.responseText;
          resolve(response);
        }
      };
      xhr.send();
    });
  };
  
  const getApiQuestions = () => {
    return new Promise((resolve, reject) => {
      // Ваш код для выполнения GET-запроса getApiQuestions()
    });
  };
  
  const getApiAnswers = () => {
    return new Promise((resolve, reject) => {
      // Ваш код для выполнения GET-запроса getApiAnswers()
    });
  };
  
  export { getApiAnswers, getApiQuestions, getApiThemes };
  