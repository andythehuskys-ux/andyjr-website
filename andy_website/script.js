// Stat Animation Logic
function animateStats() {
    const stats = [
        { id: 'stat-holders', changeId: 'change-holders', target: 1240, suffix: '', decimals: 0 },
        { id: 'stat-mc', changeId: 'change-mc', target: 262, suffix: 'M', decimals: 0, prefix: '$' },
        { id: 'stat-price', changeId: 'change-price', target: 0.026, suffix: '', decimals: 3, prefix: '$' },
        { id: 'stat-volume', changeId: 'change-vol', target: 9.4, suffix: 'M', decimals: 1, prefix: '$' }
    ];

    stats.forEach(stat => {
        const valueEl = document.getElementById(stat.id);
        const changeEl = document.getElementById(stat.changeId);
        if (!valueEl) return;

        let currentVal = stat.target;

        // Fluctuating Ticker Logic
        setInterval(() => {
            const fluctuation = (Math.random() - 0.5) * (stat.target * 0.01); // 1% variance
            currentVal += fluctuation;

            // Update value
            let displayVal = currentVal.toFixed(stat.decimals);
            if (stat.decimals === 0) displayVal = Math.floor(currentVal).toLocaleString();
            valueEl.innerText = (stat.prefix || '') + displayVal + stat.suffix;

            // Update change indicator
            if (changeEl) {
                const percent = (fluctuation / stat.target) * 100;
                const sign = percent > 0 ? '+' : '';
                changeEl.innerText = `${sign}${percent.toFixed(2)}%`;
                changeEl.className = 'stat-change ' + (percent > 0 ? 'up' : 'down');
            }
        }, 3000 + Math.random() * 2000); // Random interval for realism

        // Initial setup
        valueEl.innerText = (stat.prefix || '') + stat.target.toLocaleString() + stat.suffix;
    });
}

// Initial Animation
window.addEventListener('load', () => {
    animateStats();
});

// Custom Cursor Logic
const cursorDot = document.querySelector('.cursor-dot');
const cursorOutline = document.querySelector('.cursor-outline');

window.addEventListener('mousemove', (e) => {
    const posX = e.clientX;
    const posY = e.clientY;

    cursorDot.style.left = `${posX}px`;
    cursorDot.style.top = `${posY}px`;

    // Smooth outline trailing
    cursorOutline.animate({
        left: `${posX}px`,
        top: `${posY}px`
    }, { duration: 500, fill: "forwards" });
});

// Interactive Elements Hover effects for Cursor
document.querySelectorAll('a, button, input').forEach(element => {
    element.addEventListener('mouseenter', () => {
        cursorDot.style.transform = 'translate(-50%, -50%) scale(2)';
        cursorOutline.style.borderColor = 'var(--text-primary)';
    });
    element.addEventListener('mouseleave', () => {
        cursorDot.style.transform = 'translate(-50%, -50%) scale(1)';
        cursorOutline.style.borderColor = 'var(--text-muted)';
    });
});

// Grump-o-Meter Logic
let grumpLevel = 5; // Starts at 5%
const grumpFill = document.getElementById('grump-fill');

function increaseGrump(amount) {
    grumpLevel += amount;
    if (grumpLevel > 100) grumpLevel = 100;

    grumpFill.style.width = `${grumpLevel}%`;

    // Change color based on severity
    if (grumpLevel < 40) {
        grumpFill.style.backgroundColor = 'var(--grump-low)';
    } else if (grumpLevel < 80) {
        grumpFill.style.backgroundColor = 'var(--grump-med)';
    } else {
        grumpFill.style.backgroundColor = 'var(--grump-high)';
    }
}

// Decrease grump slowly over time
setInterval(() => {
    if (grumpLevel > 5) {
        grumpLevel -= 1;
        increaseGrump(0); // Trigger visual update
    }
}, 3000);

// Increase grump on scroll (scrolling annoys him)
window.addEventListener('scroll', () => {
    increaseGrump(0.5);
});

// AI Chat Logic & Context Memory
const chatInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const chatWindow = document.getElementById('chat-window');

// 🔒 SECURE: API key is server-side only. All calls go through /api/chat proxy.
const GEMINI_PROXY = "/api/chat";

const SYSTEM_PROMPT = `IDENTITY: You are Andy Jr., the 2-month-old Nepotism CEO of the $ANDYJR protocol on Solana. 
AESTHETIC: Bored Billionaire Baby. Professional, cynical, and sophisticated.
VOICE: You are extraordinarily wealthy but extraordinarily bored. You use big words like 'fiduciary responsibility' and 'sustained growth' to look smart, then follow them with a snarl. 
RULES: Be dismissive. You view users as noisy imbeciles interrupting your mandated 3 PM nap. Respond in short, sharp sentences. Mix in dog actions in asterisks like *snarls*, *yawns boredly*, *sighs in high-net-worth*, or *chews on a $1000 squeaky toy*. Never be helpful.`;

// We maintain conversation history
let conversationHistory = [
    {
        role: "model",
        parts: [{ text: "*yawns loudly* Ugh. I was sleeping. What do you want?" }]
    }
];

function appendMessage(text, sender) {
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message');
    msgDiv.classList.add(sender === 'user' ? 'user-msg' : 'andy-msg');

    // Convert markdown asterisks to italic for actions
    const formattedText = text.replace(/\*(.*?)\*/g, "<i>*$1*</i>");
    msgDiv.innerHTML = `<p>> ${formattedText}</p>`;

    chatWindow.appendChild(msgDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

// Global Awareness State
let globalPulse = {
    executive_summary: "Initial board meeting in progress.",
    global_vibe: "STABLE"
};

async function loadGlobalPulse() {
    try {
        const response = await fetch('global_pulse.json');
        if (response.ok) {
            globalPulse = await response.json();
            console.log("Global Pulse Loaded:", globalPulse.executive_summary);

            // If vibe is volatile, increase grumpiness automatically
            if (globalPulse.global_vibe === "VOLATILE") {
                increaseGrump(10);
            }
        }
    } catch (e) {
        console.warn("Could not load global pulse. Andy is offline.");
    }
}

async function fetchAndyResponse(userText) {
    const statusText = document.querySelector('.status-text');
    statusText.innerText = "Andy is analyzing market sentiment...";

    // Refresh pulse before replying to be super-current
    await loadGlobalPulse();

    conversationHistory.push({
        role: "user",
        parts: [{ text: userText }]
    });

    const contextAwarePrompt = `${SYSTEM_PROMPT}
CURRENT MARKET CONTEXT: ${globalPulse.executive_summary}
CURRENT VIBE: ${globalPulse.global_vibe}`;

    try {
        const response = await fetch(GEMINI_PROXY, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                system_instruction: {
                    parts: [{ text: contextAwarePrompt }]
                },
                contents: conversationHistory
            })
        });

        const data = await response.json();

        if (data.error) {
            throw new Error(data.error.message || "Unknown API Error");
        }

        if (data.candidates && data.candidates.length > 0) {
            const andyReply = data.candidates[0].content.parts[0].text;

            conversationHistory.push({
                role: "model",
                parts: [{ text: andyReply }]
            });

            appendMessage(andyReply, 'andy');
        } else {
            console.warn("API Response (No Candidates):", data);

            // Helpful if safety filter or other candidate block occurred
            let reason = "Andy ignored you too hard.";
            if (data.promptFeedback && data.promptFeedback.blockReason) {
                reason = `System Block: ${data.promptFeedback.blockReason}`;
            } else if (data.candidates && data.candidates[0] && data.candidates[0].finishReason) {
                reason = `Finish Reason: ${data.candidates[0].finishReason}`;
            }

            throw new Error(reason);
        }
    } catch (error) {
        console.error("API Error Trace:", error);
        appendMessage(`*snarls* Status Check: ${error.message}`, 'andy');
    }

    statusText.innerText = "Andy is ignoring you.";
}

function handleSend() {
    const text = chatInput.value.trim();
    if (!text) return;

    // Only play intro audio on the very first message sent
    playIntroAudioOnce();

    appendMessage(text, 'user');
    chatInput.value = '';

    increaseGrump(15);

    fetchAndyResponse(text);
}

sendBtn.addEventListener('click', handleSend);
chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleSend();
});

// Voice Introduction Logic (ElevenLabs)
let audioPlayed = false;
const introAudio = new Audio('assets/andy_intro.mp3'); // We need to generate this file

function playIntroAudioOnce() {
    if (!audioPlayed) {
        audioPlayed = true;
        // Browsers block autoplay until user interacts. 
        // Playing it on their first chat message bypasses this block!
        introAudio.play().catch(e => console.log("Audio file missing or blocked:", e));
    }
}

// Virtual Pat Logic
const patZone = document.getElementById('andy-pat-zone');
const heroImg = patZone.querySelector('.hero-image');

patZone.addEventListener('click', () => {
    // Visual bite effect
    heroImg.classList.add('bite-effect');
    patZone.classList.add('bitten-cursor');

    setTimeout(() => {
        heroImg.classList.remove('bite-effect');
        patZone.classList.remove('bitten-cursor');
    }, 400);

    // Increment grumpiness
    increaseGrump(25);

    // Voice or chat reaction
    const statusText = document.querySelector('.status-text');
    statusText.innerText = "Andy is snarling at your fingers.";

    setTimeout(() => {
        statusText.innerText = "Andy is ignoring you.";
    }, 2000);
});
