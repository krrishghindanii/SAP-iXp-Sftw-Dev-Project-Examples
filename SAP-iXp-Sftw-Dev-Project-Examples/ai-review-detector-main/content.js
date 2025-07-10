(async function () {
    const hostname = location.hostname;
    const allowed = ["amazon.", "flipkart.", "ebay.", "aliexpress.", "walmart."];
    if (!allowed.some(domain => hostname.includes(domain))) return;

    const box = document.createElement("div");
    box.id = "ai-review-detector-box";
    box.style.position = "fixed";
    box.style.bottom = "20px";
    box.style.right = "20px";
    box.style.width = "400px";
    box.style.background = "#fff";
    box.style.border = "2px solid gold";
    box.style.padding = "16px";
    box.style.borderRadius = "12px";
    box.style.fontWeight = "bold";
    box.style.fontFamily = "Arial, sans-serif";
    box.style.zIndex = "99999";
    box.style.fontSize = "14px";
    box.style.boxShadow = "0 0 12px rgba(0,0,0,0.15)";
    box.innerHTML = "<div id='ai-header'><strong>Analyzing reviews...</strong></div><div id='eta'>Estimated time remaining: <span id='time-left'>~10s</span></div>";

    document.body.appendChild(box);

    let startTime = Date.now();
    const interval = setInterval(() => {
        const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
        const remaining = Math.max(0, (10 - elapsed)).toFixed(1);
        const timeLeft = document.getElementById("time-left");
        if (timeLeft) timeLeft.innerText = `~${remaining}s`;
        if (remaining <= 0) clearInterval(interval);
    }, 300);

    // Simulate review fetching
    const total = 879; // Placeholder for real count
    const ai = 137;    // Placeholder for GPT result
    const percent = ((ai / total) * 100).toFixed(1);

    setTimeout(() => {
        box.innerHTML = `
            <strong style='font-size:16px;'>Analysis Complete</strong><br><br>
            <strong>Total reviews collected:</strong> ${total}<br>
            <strong>AI-generated reviews:</strong> ${ai} / ${total} (${percent}%)<br><br>
            <strong>Sample AI Reviews:</strong>
            <ul style='margin-top:6px;'>
                <li>This product exceeded all my expectations and feels like magic in a box.</li>
                <li>Truly the best thing I've ever bought. A masterpiece of engineering!</li>
                <li>I don’t usually write reviews, but this one deserves it — perfection.</li>
            </ul>
        `;
    }, 5000);
})();
