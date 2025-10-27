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

// Load Contents
async function loadContents() {
    try {
        const response = await fetch('/api/contents?shuffle=true');
        const contents = await response.json();
        
        const contentCards = document.getElementById('contentCards');
        contentCards.innerHTML = '';
        
        contents.forEach(content => {
            const card = createContentCard(content);
            contentCards.innerHTML += card;
        });
    } catch (error) {
        console.error('Error loading contents:', error);
        const contentCards = document.getElementById('contentCards');
        contentCards.innerHTML = '<div class="col-12"><div class="alert alert-danger">Failed to load contents. Please try again later.</div></div>';
    }
}

function createContentCard(content) {
    const posterUrl = content.poster_url || 'https://via.placeholder.com/400x300?text=' + encodeURIComponent(content.title);
    const truncatedSummary = content.summary.length > 100 ? content.summary.substring(0, 100) + '...' : content.summary;
    
    return `
        <div class="col-md-6 col-lg-4 mb-4">
            <div class="card" onclick="window.location.href='/content/${content.id}'">
                <img src="${posterUrl}" class="card-img-top" alt="${content.title}">
                <div class="card-body">
                    <h5 class="card-title">${content.title}</h5>
                    <p class="card-text">${truncatedSummary}</p>
                    <span class="badge bg-primary">${content.content_type}</span>
                    <span class="badge bg-secondary">${content.language}</span>
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
    
    try {
        const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
        const contents = await response.json();
        
        const contentCards = document.getElementById('contentCards');
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
