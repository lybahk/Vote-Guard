const API_URL = "http://127.0.0.1:5000";


document.getElementById("signupForm")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const response = await fetch(`${API_URL}/signup`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    });

    const data = await response.json();
    document.getElementById("signupMessage").innerText = data.message;

    if (response.ok) window.location.href = "login.html";
});


document.getElementById("loginForm")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const response = await fetch(`${API_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    });

    const data = await response.json();
    document.getElementById("loginMessage").innerText = data.message;

    if (response.ok) window.location.href = "vote.html";
});

document.getElementById("voteForm")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const votes = {};

    document.querySelectorAll("input[type='radio']:checked").forEach((input) => {
        votes[input.name] = input.value;
    });

    const response = await fetch(`${API_URL}/vote`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(votes)
    });

    const data = await response.json();
    document.getElementById("voteMessage").innerText = data.message;
});


async function fetchResults() {
    const response = await fetch(`${API_URL}/results`);
    const results = await response.json();
    document.getElementById("results").innerText = JSON.stringify(results, null, 2);
}
