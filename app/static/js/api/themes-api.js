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
        const xhr = new XMLHttpRequest();
        xhr.open('GET', '/all_questions/');
        xhr.onload = function() {
          if (xhr.status === 200) {
            const response = xhr.responseText;
            resolve(response);
          }
        };
        xhr.send();
    });
  };
  
  const getApiAnswers = () => {
    return new Promise((resolve, reject) => {
        const xhr = new XMLHttpRequest();
        xhr.open('GET', '/all_answers/');
        xhr.onload = function() {
          if (xhr.status === 200) {
            const response = xhr.responseText;
            resolve(response);
          }
        };
        xhr.send();
    });
  };
  
  export { getApiAnswers, getApiQuestions, getApiThemes };
  