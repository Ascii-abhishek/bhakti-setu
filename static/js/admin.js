// Authentication Token
let authToken = localStorage.getItem('authToken');

const loginSection = document.getElementById('loginSection');
const adminSection = document.getElementById('adminSection');
const logoutBtn = document.getElementById('logoutBtn');

// Check if already logged in
if (authToken) {
    showAdminSection();
}

// Login Form
const loginForm = document.getElementById('loginForm');
loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    try {
        const response = await fetch('/api/admin/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });
        
        if (!response.ok) {
            throw new Error('Invalid credentials');
        }
        
        const data = await response.json();
        authToken = data.access_token;
        localStorage.setItem('authToken', authToken);
        
        showAdminSection();
    } catch (error) {
        const loginError = document.getElementById('loginError');
        loginError.textContent = 'Invalid username or password';
        loginError.classList.remove('d-none');
    }
});

// Logout
logoutBtn.addEventListener('click', () => {
    localStorage.removeItem('authToken');
    authToken = null;
    showLoginSection();
});

function showAdminSection() {
    loginSection.style.display = 'none';
    adminSection.style.display = 'block';
    logoutBtn.style.display = 'block';
}

function showLoginSection() {
    loginSection.style.display = 'block';
    adminSection.style.display = 'none';
    logoutBtn.style.display = 'none';
}

// Image Upload Handler
async function uploadImage(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch('/api/admin/upload-image', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${authToken}`
            },
            body: formData
        });
        
        if (!response.ok) {
            throw new Error('Failed to upload image');
        }
        
        const data = await response.json();
        return data.url;
    } catch (error) {
        console.error('Error uploading image:', error);
        throw error;
    }
}

// Poster Image Upload
const posterImageInput = document.getElementById('posterImage');
const posterUrlInput = document.getElementById('posterUrl');
const posterPreview = document.getElementById('posterPreview');

posterImageInput.addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (file) {
        try {
            posterPreview.innerHTML = '<div class="spinner-border spinner-border-sm" role="status"></div> Uploading...';
            const url = await uploadImage(file);
            posterUrlInput.value = url;
            posterPreview.innerHTML = `<img src="${url}" class="img-thumbnail" style="max-width: 200px;"> <span class="text-success">✓ Uploaded</span>`;
        } catch (error) {
            posterPreview.innerHTML = '<span class="text-danger">Failed to upload image</span>';
        }
    }
});

// Banner Image Upload
const bannerImageInput = document.getElementById('bannerImage');
const bannerUrlInput = document.getElementById('bannerUrl');
const bannerPreview = document.getElementById('bannerPreview');

bannerImageInput.addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (file) {
        try {
            bannerPreview.innerHTML = '<div class="spinner-border spinner-border-sm" role="status"></div> Uploading...';
            const url = await uploadImage(file);
            bannerUrlInput.value = url;
            bannerPreview.innerHTML = `<img src="${url}" class="img-thumbnail" style="max-width: 200px;"> <span class="text-success">✓ Uploaded</span>`;
        } catch (error) {
            bannerPreview.innerHTML = '<span class="text-danger">Failed to upload image</span>';
        }
    }
});

// Content Form
const contentForm = document.getElementById('contentForm');
contentForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const contentData = {
        content_type: document.getElementById('contentType').value,
        language: document.getElementById('language').value,
        title: document.getElementById('title').value,
        title_en: document.getElementById('titleEn').value || null,
        header: document.getElementById('header').value || null,
        summary: document.getElementById('summary').value,
        summary_en: document.getElementById('summaryEn').value || null,
        poster_url: document.getElementById('posterUrl').value || null,
        banner_url: document.getElementById('bannerUrl').value || null,
        content_html: document.getElementById('contentHtml').value,
        content_html_en: document.getElementById('contentHtmlEn').value || null,
        audio_url: document.getElementById('audioUrl').value || null,
        tags: document.getElementById('tags').value || null,
        reference_id: document.getElementById('referenceId').value || null
    };
    
    const contentError = document.getElementById('contentError');
    const contentSuccess = document.getElementById('contentSuccess');
    contentError.classList.add('d-none');
    contentSuccess.classList.add('d-none');
    
    try {
        const response = await fetch('/api/admin/contents', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify(contentData)
        });
        
        if (!response.ok) {
            throw new Error('Failed to create content');
        }
        
        contentSuccess.textContent = 'Content added successfully!';
        contentSuccess.classList.remove('d-none');
        contentForm.reset();
        posterPreview.innerHTML = '';
        bannerPreview.innerHTML = '';
        
        // Hide success message after 3 seconds
        setTimeout(() => {
            contentSuccess.classList.add('d-none');
        }, 3000);
    } catch (error) {
        contentError.textContent = 'Failed to add content. Please try again.';
        contentError.classList.remove('d-none');
    }
});
