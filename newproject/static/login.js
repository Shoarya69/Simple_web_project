function showRegister() {
    document.getElementById('login-form').classList.add('hidden');
    document.getElementById('register-form').classList.remove('hidden');
}
function showLogin() {
    document.getElementById('register-form').classList.add('hidden');
    document.getElementById('login-form').classList.remove('hidden');
}

// Optional: show register form if redirected to /register
if (window.location.pathname.endsWith('/register')) {
    showRegister();
}