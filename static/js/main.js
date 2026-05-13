document.addEventListener('DOMContentLoaded', () => {
    // Dark mode toggle
    const themeToggle = document.getElementById('theme-toggle');
    const body = document.body;
    const moonIcon = '🌙';
    const sunIcon = '☀️';

    // Check localStorage
    if (localStorage.getItem('theme') === 'dark') {
        body.classList.add('dark-mode');
        if(themeToggle) themeToggle.textContent = sunIcon;
    } else {
        if(themeToggle) themeToggle.textContent = moonIcon;
    }

    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            body.classList.toggle('dark-mode');
            if (body.classList.contains('dark-mode')) {
                localStorage.setItem('theme', 'dark');
                themeToggle.textContent = sunIcon;
            } else {
                localStorage.setItem('theme', 'light');
                themeToggle.textContent = moonIcon;
            }
        });
    }

    // Sidebar Toggle (Mobile & Desktop)
    const menuToggle = document.getElementById('menu-toggle');
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.querySelector('.main-content');
    
    if (menuToggle && sidebar && mainContent) {
        menuToggle.addEventListener('click', () => {
            sidebar.classList.toggle('collapsed');
            mainContent.classList.toggle('expanded');
            
            // For mobile compatibility (the old 'active' class used transform)
            if (window.innerWidth <= 768) {
                sidebar.classList.toggle('active');
            }
        });
    }

    // Live Clock
    const clockElement = document.getElementById('live-clock');
    if (clockElement) {
        setInterval(() => {
            const now = new Date();
            const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit' };
            clockElement.textContent = now.toLocaleDateString('en-US', options);
        }, 1000);
    }

    // Photo Upload Preview
    const photoInput = document.getElementById('profile_photo');
    const photoPreview = document.getElementById('photo_preview');
    if (photoInput && photoPreview) {
        photoInput.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    photoPreview.src = e.target.result;
                }
                reader.readAsDataURL(file);
            }
        });
    }

    // Client-side form validation (Register)
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            const password = document.getElementById('password').value;
            const confirm = document.getElementById('confirm_password').value;
            
            if (password.length < 8) {
                e.preventDefault();
                alert('Password must be at least 8 characters long.');
                return;
            }
            if (password !== confirm) {
                e.preventDefault();
                alert('Passwords do not match.');
            }
        });
    }
});
