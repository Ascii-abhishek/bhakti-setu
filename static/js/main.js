// Theme Management
const themeToggle = document.getElementById('themeToggle');
const themeIcon = document.getElementById('themeIcon');
let currentTheme = localStorage.getItem('theme') || 'light';

function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    if (theme === 'dark') {
        themeIcon.classList.remove('bi-sun-fill');
        themeIcon.classList.add('bi-moon-fill');
    } else {
        themeIcon.classList.remove('bi-moon-fill');
        themeIcon.classList.add('bi-sun-fill');
    }
}

setTheme(currentTheme);

themeToggle.addEventListener('click', () => {
    currentTheme = currentTheme === 'light' ? 'dark' : 'light';
    setTheme(currentTheme);
});

// Language Management
const languageToggle = document.getElementById('languageToggle');
let currentLanguage = localStorage.getItem('language') || 'hindi';

function setLanguage(lang) {
    localStorage.setItem('language', lang);
    currentLanguage = lang;
}

// Initialize language
setLanguage(currentLanguage);

languageToggle.addEventListener('click', () => {
    // Toggle between hindi and english
    currentLanguage = currentLanguage === 'hindi' ? 'english' : 'hindi';
    setLanguage(currentLanguage);
    // Reload contents in new language
    loadContents();
});

// Load Contents
async function loadContents() {
    const contentCards = document.getElementById('contentCards');
    
    // Show loader skeletons
    contentCards.innerHTML = `
        <div class="col-md-6 col-lg-4 mb-4 skeleton-card">
            <div class="card">
                <div class="skeleton skeleton-img"></div>
                <div class="card-body">
                    <div class="skeleton skeleton-title"></div>
                    <div class="skeleton skeleton-text"></div>
                    <div class="skeleton skeleton-text"></div>
                </div>
            </div>
        </div>
        <div class="col-md-6 col-lg-4 mb-4 skeleton-card">
            <div class="card">
                <div class="skeleton skeleton-img"></div>
                <div class="card-body">
                    <div class="skeleton skeleton-title"></div>
                    <div class="skeleton skeleton-text"></div>
                    <div class="skeleton skeleton-text"></div>
                </div>
            </div>
        </div>
        <div class="col-md-6 col-lg-4 mb-4 skeleton-card">
            <div class="card">
                <div class="skeleton skeleton-img"></div>
                <div class="card-body">
                    <div class="skeleton skeleton-title"></div>
                    <div class="skeleton skeleton-text"></div>
                    <div class="skeleton skeleton-text"></div>
                </div>
            </div>
        </div>
    `;
    
    try {
        // Start timer for minimum 1 second display
        const startTime = Date.now();
        
        const response = await fetch(`/api/contents?shuffle=true&language=${currentLanguage}`);
        const contents = await response.json();
        
        // Calculate remaining time to reach 1 second minimum
        const elapsedTime = Date.now() - startTime;
        const remainingTime = Math.max(0, 1000 - elapsedTime);
        
        // Wait for remaining time before showing results
        await new Promise(resolve => setTimeout(resolve, remainingTime));
        
        contentCards.innerHTML = '';
        
        contents.forEach(content => {
            const card = createContentCard(content);
            contentCards.innerHTML += card;
        });
    } catch (error) {
        console.error('Error loading contents:', error);
        contentCards.innerHTML = '<div class="col-12"><div class="alert alert-danger">Failed to load contents. Please try again later.</div></div>';
    }
}

function createContentCard(content) {
    const posterUrl = content.poster_url || 'https://via.placeholder.com/400x300?text=' + encodeURIComponent(content.title);
    const truncatedSummary = content.summary.length > 100 ? content.summary.substring(0, 100) + '...' : content.summary;
    
    // Use appropriate language fields
    const title = currentLanguage === 'english' && content.title_en ? content.title_en : content.title;
    const summary = currentLanguage === 'english' && content.summary_en ? content.summary_en : content.summary;
    const truncatedDisplaySummary = summary.length > 100 ? summary.substring(0, 100) + '...' : summary;
    
    return `
        <div class="col-md-6 col-lg-4 mb-4">
            <div class="card" onclick="window.location.href='/content/${content.id}'">
                <img src="${posterUrl}" class="card-img-top" alt="${title}">
                <div class="card-body">
                    <h5 class="card-title">${title}</h5>
                    <p class="card-text">${truncatedDisplaySummary}</p>
                    <span class="badge bg-primary">${content.content_type}</span>
                </div>
            </div>
        </div>
    `;
}

// Search Functionality
const searchInput = document.getElementById('searchInput');
const searchBtn = document.getElementById('searchBtn');

async function performSearch() {
    const query = searchInput.value.trim();
    if (!query) {
        loadContents();
        return;
    }
    
    const contentCards = document.getElementById('contentCards');
    
    // Show loader skeletons
    contentCards.innerHTML = `
        <div class="col-md-6 col-lg-4 mb-4 skeleton-card">
            <div class="card">
                <div class="skeleton skeleton-img"></div>
                <div class="card-body">
                    <div class="skeleton skeleton-title"></div>
                    <div class="skeleton skeleton-text"></div>
                    <div class="skeleton skeleton-text"></div>
                </div>
            </div>
        </div>
        <div class="col-md-6 col-lg-4 mb-4 skeleton-card">
            <div class="card">
                <div class="skeleton skeleton-img"></div>
                <div class="card-body">
                    <div class="skeleton skeleton-title"></div>
                    <div class="skeleton skeleton-text"></div>
                    <div class="skeleton skeleton-text"></div>
                </div>
            </div>
        </div>
        <div class="col-md-6 col-lg-4 mb-4 skeleton-card">
            <div class="card">
                <div class="skeleton skeleton-img"></div>
                <div class="card-body">
                    <div class="skeleton skeleton-title"></div>
                    <div class="skeleton skeleton-text"></div>
                    <div class="skeleton skeleton-text"></div>
                </div>
            </div>
        </div>
    `;
    
    try {
        // Start timer for minimum 1 second display
        const startTime = Date.now();
        
        const response = await fetch(`/api/search?q=${encodeURIComponent(query)}&language=${currentLanguage}`);
        const contents = await response.json();
        
        // Calculate remaining time to reach 1 second minimum
        const elapsedTime = Date.now() - startTime;
        const remainingTime = Math.max(0, 1000 - elapsedTime);
        
        // Wait for remaining time before showing results
        await new Promise(resolve => setTimeout(resolve, remainingTime));
        
        contentCards.innerHTML = '';
        
        if (contents.length === 0) {
            contentCards.innerHTML = '<div class="col-12"><div class="alert alert-info">No results found for your search.</div></div>';
            return;
        }
        
        contents.forEach(content => {
            const card = createContentCard(content);
            contentCards.innerHTML += card;
        });
    } catch (error) {
        console.error('Error searching contents:', error);
        contentCards.innerHTML = '<div class="col-12"><div class="alert alert-danger">Error searching contents. Please try again.</div></div>';
    }
}

searchBtn.addEventListener('click', performSearch);
searchInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        performSearch();
    }
});

// Play Random
const playRandomBtn = document.getElementById('playRandomBtn');
playRandomBtn.addEventListener('click', async () => {
    try {
        const response = await fetch('/api/random');
        const content = await response.json();
        
        if (content.audio_url) {
            const audio = new Audio(content.audio_url);
            audio.play();
        } else {
            window.location.href = `/content/${content.id}`;
        }
    } catch (error) {
        console.error('Error playing random content:', error);
        alert('Unable to play random content');
    }
});

// Load contents on page load
loadContents();
