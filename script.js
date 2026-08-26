const API_URL = "https://sharm-backend-5547.onrender.com";

const tg = window.Telegram.WebApp;

tg.ready();
tg.expand();

const user = tg.initDataUnsafe?.user;

if (user) {
    fetch(`${API_URL}/api/auth`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            telegram_id: user.id,
            username: user.username || "",
            first_name: user.first_name || ""
        })
    })
    .then(res => res.json())
    .then(data => {
        console.log("User authenticated:", data);
    })
    .catch(err => {
        console.error("Auth error:", err);
    });
           }
