document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('search-form');
    const searchInput = document.getElementById('search-input');

    // Фокус на поисковую строку при загрузке
    searchInput.focus();

    // Обработка поиска
    searchForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const query = searchInput.value.trim();
        if (query) {
            // Кодируем запрос для URL
            const encodedQuery = encodeURIComponent(query);
            
            // Перенаправляем на DuckDuckGo с поисковым запросом
            window.location.href = `https://duckduckgo.com/?q=${encodedQuery}`;
        }
    });

    // Быстрый поиск при нажатии Enter
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            searchForm.dispatchEvent(new Event('submit'));
        }
    });

    // Сохранение последних поисковых запросов в localStorage
    searchInput.addEventListener('input', function() {
        localStorage.setItem('lastSearch', searchInput.value);
    });

    // Восстановление последнего поискового запроса
    const lastSearch = localStorage.getItem('lastSearch');
    if (lastSearch) {
        searchInput.value = lastSearch;
    }

    // Анимация появления элементов
    const animateElements = () => {
        const elements = document.querySelectorAll('.link-card, .feature-card');
        elements.forEach((element, index) => {
            setTimeout(() => {
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }, index * 100);
        });
    };

    // Инициализация анимации
    setTimeout(animateElements, 500);
});
