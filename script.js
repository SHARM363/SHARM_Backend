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
let balance = 0;
let energy = 1500;
const maxEnergy = 1500;

const balanceEl = document.getElementById("balance");
const energyText = document.getElementById("energyText");
const energyFill = document.getElementById("energyFill");
const tapBtn = document.getElementById("tapBtn");

function updateUI() {
    balanceEl.textContent = balance;
    energyText.textContent = `${energy} / ${maxEnergy}`;
    energyFill.style.width = `${(energy / maxEnergy) * 100}%`;
}

tapBtn.addEventListener("click", () => {
    if (energy <= 0) return;

    balance += 1;
    energy -= 1;
    showFloatingPlus();
    
    if (window.Telegram?.WebApp?.HapticFeedback) {
        Telegram.WebApp.HapticFeedback.impactOccurred("light");
    }

    updateUI();
});

setInterval(() => {
    if (energy < maxEnergy) {
        energy += 1;
        updateUI();
    }
}, 1000);

updateUI();
function showFloatingPlus() {
    const plus = document.createElement("div");
    plus.className = "floating-plus";
    plus.innerText = "+1";

    const rect = tapBtn.getBoundingClientRect();

    plus.style.left = rect.left + rect.width / 2 + "px";
    plus.style.top = rect.top + "px";

    document.body.appendChild(plus);

    setTimeout(() => {
        plus.remove();
    }, 800);
}
