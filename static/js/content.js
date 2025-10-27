// Get content ID from URL
const urlParts = window.location.pathname.split('/');
const contentId = urlParts[urlParts.length - 1];
let currentContent = null;

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

// Language Management for Content
const languageToggle = document.getElementById('languageToggle');
let contentLanguage = 'hindi'; // Default for individual content

languageToggle.addEventListener('click', async () => {
    // Toggle language
    const targetLanguage = contentLanguage === 'hindi' ? 'english' : 'hindi';
    
    try {
        // Check if content is available in target language
        const checkResponse = await fetch(`/api/contents/${contentId}/check-language/${targetLanguage}`);
        const checkData = await checkResponse.json();
        
        if (!checkData.available) {
            // Show toast notification
            const toastElement = document.getElementById('languageToast');
            const toast = new bootstrap.Toast(toastElement, {
                autohide: true,
                delay: 2000
            });
            toast.show();
            return;
        }
        
        // Load content in target language
        const response = await fetch(`/api/contents/${contentId}/language/${targetLanguage}`);
        if (!response.ok) {
            throw new Error('Content not available in this language');
        }
        
        const content = await response.json();
        contentLanguage = targetLanguage;
        currentContent = content;
        displayContent(content);
        
    } catch (error) {
        console.error('Error switching language:', error);
        const toastElement = document.getElementById('languageToast');
        const toast = new bootstrap.Toast(toastElement, {
            autohide: true,
            delay: 2000
        });
        toast.show();
    }
});

// Load Content
async function loadContent() {
    try {
        const response = await fetch(`/api/contents/${contentId}`);
        if (!response.ok) {
            throw new Error('Content not found');
        }
        
        const content = await response.json();
        currentContent = content;
        contentLanguage = content.language;
        displayContent(content);
        
        // Store content ID for navigation
        localStorage.setItem('currentContentId', contentId);
    } catch (error) {
        console.error('Error loading content:', error);
        const contentDisplay = document.getElementById('contentDisplay');
        contentDisplay.innerHTML = '<div class="alert alert-danger">Content not found or failed to load.</div>';
    }
}

function displayContent(content) {
    const contentDisplay = document.getElementById('contentDisplay');
    
    // Determine which fields to use based on current language
    let title, summary, contentHtml;
    
    if (contentLanguage === 'english') {
        // Use English fields if available, otherwise fall back to default
        title = content.title_en || content.title;
        summary = content.summary_en || content.summary;
        contentHtml = content.content_html_en || content.content_html;
    } else {
        title = content.title;
        summary = content.summary;
        contentHtml = content.content_html;
    }
    
    // Use banner for content page, poster only for tiles
    const bannerHtml = content.banner_url ? 
        `<img src="${content.banner_url}" class="img-fluid mb-4 rounded" alt="${title}">` : '';
    
    // Parse tags
    const tagsHtml = content.tags ? content.tags.split(',').map(tag => 
        `<span class="tag-badge">${tag.trim()}</span>`
    ).join('') : '';
    
    // Format date
    const createdDate = new Date(content.created_at).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
    
    contentDisplay.innerHTML = `
        <div class="content-detail">
            ${bannerHtml}
            ${content.header ? `<h6 class="text-muted">${content.header}</h6>` : ''}
            <h1>${title}</h1>
            <div class="mb-3">
                <span class="badge bg-primary">${content.content_type}</span>
            </div>
            <p class="lead">${summary}</p>
            <hr>
            <div class="content-html">
                ${contentHtml}
            </div>
            <div class="content-meta">
                <div class="content-tags">
                    ${tagsHtml}
                </div>
                <div class="content-date">
                    ${createdDate}
                </div>
            </div>
        </div>
    `;
    
    // Setup play button
    const playBtn = document.getElementById('playBtn');
    if (content.audio_url) {
        playBtn.style.display = 'block';
        playBtn.onclick = () => {
            const audio = new Audio(content.audio_url);
            audio.play();
        };
    } else {
        playBtn.style.display = 'none';
    }
}

// Navigation Buttons
const nextBtn = document.getElementById('nextBtn');
const prevBtn = document.getElementById('prevBtn');

nextBtn.addEventListener('click', async () => {
    try {
        const response = await fetch('/api/random');
        const content = await response.json();
        window.location.href = `/content/${content.id}`;
    } catch (error) {
        console.error('Error loading next content:', error);
    }
});

prevBtn.addEventListener('click', () => {
    window.history.back();
});

// Load content on page load
loadContent();
