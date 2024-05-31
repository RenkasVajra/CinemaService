let darkThemeButton = document.querySelector('.theme-button-dark');
let lightThemeButton = document.querySelector('.theme-button-light');
let serifFontButton = document.querySelector('.font-button-serif');
let sansSerifFontButton = document.querySelector('.font-button-sans-serif');
let themeSwitcher = document.querySelector('.theme-switcher');

// Проверяем, есть ли сохраненная тема
const savedTheme = localStorage.getItem('theme');
if (savedTheme) {
    if (savedTheme === 'dark') {
        document.body.classList.add('dark');
        darkThemeButton.classList.add('active');
        lightThemeButton.classList.remove('active');
    } else {
        document.body.classList.remove('dark');
        lightThemeButton.classList.add('active');
        darkThemeButton.classList.remove('active');
    }
}

darkThemeButton.onclick = function () {
    document.body.classList.add('dark');
    darkThemeButton.classList.add('active');
    lightThemeButton.classList.remove('active');
    localStorage.setItem('theme', 'dark'); // Сохраняем тему в LocalStorage
};

lightThemeButton.onclick = function () {
    document.body.classList.remove('dark');
    lightThemeButton.classList.add('active');
    darkThemeButton.classList.remove('active');
    localStorage.setItem('theme', 'light'); // Сохраняем тему в LocalStorage
};

serifFontButton.onclick = function () {
    document.body.classList.add('serif');
    sansSerifFontButton.classList.remove('active');
    serifFontButton.classList.add('active');
}

sansSerifFontButton.onclick = function () {
  document.body.classList.remove('serif');
  sansSerifFontButton.classList.add('active');
  serifFontButton.classList.remove('active');
};

let articleSections = document.querySelectorAll('.blog-article.short');

for (let articleSection of articleSections) {
  let moreButton = articleSection.querySelector('.more');
  moreButton.onclick = function () {
    articleSection.classList.remove('short');
  };
}

let gridViewButton = document.querySelector('.card-view-button-grid');
let listdViewButton = document.querySelector('.card-view-button-list');
let cardsList = document.querySelector('.cards');


gridViewButton.onclick = function () {
  cardsList.classList.remove('standard');
  gridViewButton.classList.add('active');
  listdViewButton.classList.remove('active');
};

listdViewButton.onclick = function () {
  cardsList.classList.add('standard');
  gridViewButton.classList.remove('active');
  listdViewButton.classList.add('active');
};

let mainImage = document.querySelector('.active-photo');
let previews = document.querySelectorAll('.preview-list li a');



for (let activeImage of previews) {
activeImage.onclick = function (evt) {
  evt.preventDefault();
  mainImage.src = activeImage.href;

  let currentActive = document.querySelector('.preview-list li .active-item');
  currentActive.classList.remove('active-item');
  activeImage.classList.add('active-item');
};
}


//dddddd



function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
