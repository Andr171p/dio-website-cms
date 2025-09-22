document.addEventListener('DOMContentLoaded', function() {
    try {
        // Получаем элементы
        const slides = document.querySelectorAll('.hero-slide');
        const dots = document.querySelectorAll('.carousel-dot');
        const navBlocks = document.querySelectorAll('.nav-block');
        const heroSection = document.querySelector('.hero-container');
        
        console.log('Slides found:', slides.length);
        console.log('Dots found:', dots.length);
        console.log('Nav blocks found:', navBlocks.length);

        // Если нет слайдов, выходим
        if (slides.length === 0) {
            console.warn('No slides found');
            return;
        }
        
        let currentSlide = 0;
        let autoSlideInterval = null;

        /**
         * Показывает конкретный слайд
         * @param {number} index - Индекс слайда для показа
         */
        function showSlide(index) {
            // Проверяем валидность индекса
            if (index < 0 || index >= slides.length) {
                console.error('Invalid slide index:', index);
                return;
            }
            
            console.log('Showing slide:', index);
            
            // Скрыть все слайды
            slides.forEach(slide => {
                slide.classList.remove('active');
            });
            
            // Обновить точки навигации
            dots.forEach(dot => {
                dot.classList.remove('active');
            });
            
            // Показать выбранный слайд
            slides[index].classList.add('active');
            
            // Активировать соответствующую точку
            if (dots[index]) {
                dots[index].classList.add('active');
            }
            
            currentSlide = index;
        }

        /**
         * Запускает автоматическое переключение слайдов
         */
        function startAutoSlide() {
            if (slides.length <= 1) return;
            
            stopAutoSlide();
            
            autoSlideInterval = setInterval(() => {
                const nextSlide = (currentSlide + 1) % slides.length;
                showSlide(nextSlide);
            }, 5000);
        }

        /**
         * Останавливает автоматическое переключение
         */
        function stopAutoSlide() {
            if (autoSlideInterval) {
                clearInterval(autoSlideInterval);
                autoSlideInterval = null;
            }
        }

        /**
         * Обработчик клика по навигационным элементам
         * @param {number} index - Индекс целевого слайда
         */
        function handleNavigationClick(index) {
            console.log('Navigation clicked:', index);
            stopAutoSlide();
            showSlide(index);
            startAutoSlide();
        }

        // Инициализация - показываем первый слайд
        showSlide(0);
        
        // Добавляем обработчики для точек навигации
        dots.forEach((dot, index) => {
            dot.addEventListener('click', function(e) {
                e.preventDefault();
                handleNavigationClick(index);
            });
            
            // Добавляем ARIA атрибуты для доступности
            dot.setAttribute('role', 'button');
            dot.setAttribute('aria-label', `Показать слайд ${index + 1}`);
        });

        // Добавляем обработчики для навигационных блоков
        navBlocks.forEach((block, index) => {
            block.addEventListener('click', function(e) {
                e.preventDefault();
                handleNavigationClick(index);
            });
            
            // Добавляем ARIA атрибуты
            block.setAttribute('role', 'button');
            block.setAttribute('tabindex', '0');
            block.setAttribute('aria-label', `Показать слайд ${index + 1}: ${block.querySelector('h3')?.textContent || ''}`);
            
            // Добавляем поддержку клавиатуры
            block.addEventListener('keypress', function(e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    handleNavigationClick(index);
                }
            });
        });

        // Автопереключение для нескольких слайдов
        if (slides.length > 1) {
            startAutoSlide();
            
            // Пауза при наведении мыши
            if (heroSection) {
                heroSection.addEventListener('mouseenter', stopAutoSlide);
                heroSection.addEventListener('mouseleave', startAutoSlide);
                
                // Пауза при фокусе (для доступности)
                heroSection.addEventListener('focusin', stopAutoSlide);
                heroSection.addEventListener('focusout', startAutoSlide);
            }
        }

        // Добавляем обработку касаний для мобильных устройств
        let touchStartX = 0;
        let touchEndX = 0;
        
        if (heroSection) {
            heroSection.addEventListener('touchstart', function(e) {
                touchStartX = e.changedTouches[0].screenX;
            }, { passive: true });

            heroSection.addEventListener('touchend', function(e) {
                touchEndX = e.changedTouches[0].screenX;
                handleSwipe();
            }, { passive: true });
        }

        /**
         * Обрабатывает свайп-жесты
         */
        function handleSwipe() {
            const minSwipeDistance = 50;
            
            if (touchStartX - touchEndX > minSwipeDistance) {
                // Свайп влево - следующий слайд
                const nextSlide = (currentSlide + 1) % slides.length;
                handleNavigationClick(nextSlide);
            } else if (touchEndX - touchStartX > minSwipeDistance) {
                // Свайп вправо - предыдущий слайд
                const prevSlide = (currentSlide - 1 + slides.length) % slides.length;
                handleNavigationClick(prevSlide);
            }
        }

        // Добавляем глобальные обработчики ошибок
        window.addEventListener('error', function(e) {
            console.error('JavaScript Error:', e.error);
        });

        // Экспортируем функции для отладки (опционально)
        window.carouselAPI = {
            showSlide,
            startAutoSlide,
            stopAutoSlide,
            nextSlide: () => handleNavigationClick((currentSlide + 1) % slides.length),
            prevSlide: () => handleNavigationClick((currentSlide - 1 + slides.length) % slides.length)
        };

    } catch (error) {
        console.error('Carousel initialization error:', error);
    }
});