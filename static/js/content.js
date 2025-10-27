// Get content ID from URL
const urlParts = window.location.pathname.split('/');
const contentId = urlParts[urlParts.length - 1];

// Load Content
async function loadContent() {
    try {
        const response = await fetch(`/api/contents/${contentId}`);
        if (!response.ok) {
            throw new Error('Content not found');
        }
        
        const content = await response.json();
        displayContent(content);
        
        // Store content ID for next button
        localStorage.setItem('currentContentId', contentId);
    } catch (error) {
        console.error('Error loading content:', error);
        const contentDisplay = document.getElementById('contentDisplay');
        contentDisplay.innerHTML = '<div class="alert alert-danger">Content not found or failed to load.</div>';
    }
}

function displayContent(content) {
    const contentDisplay = document.getElementById('contentDisplay');
    
    const posterHtml = content.poster_url ? 
        `<img src="${content.poster_url}" class="img-fluid mb-4 rounded" alt="${content.title}">` : '';
    
    contentDisplay.innerHTML = `
        <div class="content-detail">
            ${posterHtml}
            ${content.header ? `<h6 class="text-muted">${content.header}</h6>` : ''}
            <h1>${content.title}</h1>
            <div class="mb-3">
                <span class="badge bg-primary">${content.content_type}</span>
                <span class="badge bg-secondary">${content.language}</span>
            </div>
            <p class="lead">${content.summary}</p>
            <hr>
            <div class="content-html">
                ${content.content_html}
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

// Next Button
const nextBtn = document.getElementById('nextBtn');
nextBtn.addEventListener('click', async () => {
    try {
        const response = await fetch('/api/random');
        const content = await response.json();
        window.location.href = `/content/${content.id}`;
    } catch (error) {
        console.error('Error loading next content:', error);
    }
});

// Load content on page load
loadContent();
