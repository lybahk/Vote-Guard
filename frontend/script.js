document.getElementById('loginForm')?.addEventListener('submit', async function (e) {
    e.preventDefault();
    let userData = {
        email: document.getElementById('email').value,
        password: document.getElementById('password').value
    };
    let response = await fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData)
    });
    let data = await response.json();
    if (data.success) window.location.href = "vote.html";
    else document.getElementById('message').innerText = data.message;
});

async function fetchResults() {
    let response = await fetch('/get_results');
    let data = await response.json();
    document.getElementById('results').innerText = JSON.stringify(data, null, 2);
}
