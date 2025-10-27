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

// Content Form
const contentForm = document.getElementById('contentForm');
contentForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const contentData = {
        content_type: document.getElementById('contentType').value,
        language: document.getElementById('language').value,
        title: document.getElementById('title').value,
        header: document.getElementById('header').value || null,
        summary: document.getElementById('summary').value,
        poster_url: document.getElementById('posterUrl').value || null,
        content_html: document.getElementById('contentHtml').value,
        audio_url: document.getElementById('audioUrl').value || null
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
        
        // Hide success message after 3 seconds
        setTimeout(() => {
            contentSuccess.classList.add('d-none');
        }, 3000);
    } catch (error) {
        contentError.textContent = 'Failed to add content. Please try again.';
        contentError.classList.remove('d-none');
    }
});
