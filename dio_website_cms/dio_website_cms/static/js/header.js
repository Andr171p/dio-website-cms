document.addEventListener('DOMContentLoaded', () => {
  const header = document.getElementById('header');
  const mobileMenu = document.getElementById('mobile-menu');

  // Обработка скроллинга
  window.addEventListener('scroll', () => {
    header.classList.toggle('bg-white/95', window.scrollY > 50);
    header.classList.toggle('backdrop-blur-md', window.scrollY > 50);
    header.classList.toggle('shadow-lg', window.scrollY > 50);
  });

  // Переключение мобильного меню
  window.toggleMobileMenu = function () {
    mobileMenu.classList.toggle('hidden');
  };

  // Закрытие мобильного меню
  window.closeMobileMenu = function () {
    mobileMenu.classList.add('hidden');
  };

  // Обработка навигации
  window.handleNavigation = function (href) {
    if (href.startsWith('#')) {
      const element = document.querySelector(href);
      if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
      }
    }
  };

  // Скролл к контактам
  window.scrollToContact = function () {
    const element = document.querySelector('#contact');
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  // Закрытие меню при клике вне
  document.addEventListener('click', (e) => {
    if (!mobileMenu.contains(e.target) && !e.target.closest('button')) {
      mobileMenu.classList.add('hidden');
    }
  });
});