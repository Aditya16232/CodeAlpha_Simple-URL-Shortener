const form = document.getElementById("shorten-form");
const input = document.getElementById("long-url");
const errorBox = document.getElementById("error");
const resultBox = document.getElementById("result");
const shortLink = document.getElementById("short-link");
const copyBtn = document.getElementById("copy-btn");

function showError(message) {
    errorBox.textContent = message;
    errorBox.classList.remove("hidden");
    resultBox.classList.add("hidden");
}

function showResult(shortUrl) {
    shortLink.href = shortUrl;
    shortLink.textContent = shortUrl;
    resultBox.classList.remove("hidden");
    errorBox.classList.add("hidden");
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const longUrl = input.value.trim();

    try {
        const response = await fetch("/shorten", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ long_url: longUrl }),
        });
        const data = await response.json();

        if (!response.ok) {
            showError(data.error || "Something went wrong.");
            return;
        }
        showResult(data.short_url);
    } catch (err) {
        showError("Network error. Is the server running?");
    }
});

copyBtn.addEventListener("click", async () => {
    try {
        await navigator.clipboard.writeText(shortLink.href);
        copyBtn.textContent = "Copied!";
        setTimeout(() => {
            copyBtn.textContent = "Copy";
        }, 1500);
    } catch (err) {
        showError("Could not copy to clipboard.");
    }
});