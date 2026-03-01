const video = document.getElementById('webcam');
const terminal = document.getElementById('results');
const carbonDisplay = document.getElementById('stat-carbon');
const overlay = document.getElementById('login-overlay');

// 1. Initialize Optical Feed
if (navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => { video.srcObject = stream; })
        .catch(err => { terminal.innerHTML = `<div class="text-red-500">> CAMERA SENSOR ERROR</div>`; });
}

// 2. Authentication: The Fix for the "Stuck" Screen
async function login() {
    const user = document.getElementById('username').value;
    const pass = document.getElementById('password').value;

    if (!user || !pass) {
        alert("Enter Operator ID and Access Code");
        return;
    }

    try {
        const response = await fetch('/api/auth', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: user, password: pass })
        });

        const data = await response.json();

        if (data.success) {
            // NUCLEAR OPTION: Remove the overlay from the DOM entirely
            if (overlay) {
                overlay.style.opacity = '0';
                setTimeout(() => {
                    overlay.remove(); // This deletes the login screen so you can't get stuck
                }, 500);
            }
            
            carbonDisplay.innerText = `${data.saved.toFixed(2)} kg`;
            console.log("✅ SYSTEM: Operator " + data.username + " Authorized.");
        } else {
            alert("ACCESS DENIED: Invalid Credentials");
        }
    } catch (err) {
        console.error("Auth Failure:", err);
        alert("CRITICAL: Server Not Responding. Is app.py running?");
    }
}

// 3. Inference / Scanning
async function capture() {
    // If the overlay still exists, don't allow scanning
    if (document.getElementById('login-overlay')) return;

    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);
    const base64Image = canvas.toDataURL('image/jpeg');

    terminal.innerHTML = `<div class="text-cyan-400 animate-pulse">> ANALYZING SPECIMEN...</div>` + terminal.innerHTML;

    try {
        const res = await fetch('/api/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ image: base64Image })
        });
        const result = await res.json();

        carbonDisplay.innerText = `${result.total_carbon.toFixed(2)} kg`;
        
        let color = "text-green-400";
        if (result.category === "Hazardous") color = "text-red-500";
        if (result.category === "Recyclable") color = "text-cyan-400";

        const logEntry = `
            <div class="p-3 border-l-2 border-gray-800 bg-white/5 mb-2">
                <p class="${color} font-bold text-xs uppercase">${result.category}</p>
                <p class="text-[10px] text-gray-500">${result.timestamp} | CONF: ${result.confidence}%</p>
            </div>
        `;
        
        // Remove the "Analyzing" text and prepend the result
        terminal.innerHTML = logEntry + terminal.innerHTML.replace(`<div class="text-cyan-400 animate-pulse">> ANALYZING SPECIMEN...</div>`, "");
    } catch (err) {
        terminal.innerHTML = `<div class="text-red-500">> NEURAL ENGINE TIMEOUT</div>` + terminal.innerHTML;
    }
}

// Hotkey: Spacebar
document.addEventListener('keydown', (e) => {
    if (e.code === 'Space') {
        e.preventDefault();
        capture();
    }
});