const API_URL = "http://127.0.0.1:5000";

document.getElementById("signupForm")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch(`${API_URL}/signup`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();
        document.getElementById("signupMessage").innerText = data.message;

        if (!response.ok) throw new Error(data.message);

        window.location.href = "login.html";
    } catch (error) {
        document.getElementById("signupMessage").innerText = "Signup failed: " + error.message;
    }
});

document.getElementById("loginForm")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch(`${API_URL}/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();
        document.getElementById("loginMessage").innerText = data.message;

        if (!response.ok) throw new Error(data.message);

        window.location.href = "vote.html";
    } catch (error) {
        document.getElementById("loginMessage").innerText = "Login failed: " + error.message;
    }
});

document.getElementById("voteForm")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const votes = {};
    
    document.querySelectorAll("input[type='radio']:checked").forEach((input) => {
        votes[input.name] = input.value;
    });

    try {
        const response = await fetch(`${API_URL}/vote`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(votes)
        });

        const data = await response.json();
        if (!response.ok) throw new Error(data.message);

        document.getElementById("voteMessage").innerText = "Vote submitted successfully!";
        document.getElementById("voteForm").reset();
    } catch (error) {
        document.getElementById("voteMessage").innerText = "Error: " + error.message;
    }
});

async function fetchResults() {
    try {
        const response = await fetch(`${API_URL}/results`);
        if (!response.ok) throw new Error("Failed to fetch results.");

        const results = await response.json();
        const resultsElement = document.getElementById("results");

        if (resultsElement) {
            resultsElement.innerText = JSON.stringify(results, null, 2);
        }
    } catch (error) {
        console.error("Error fetching results:", error);
    }
}

