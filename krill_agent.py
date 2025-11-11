"""
Krill AI Agent v4.5 — Smart + Typing Delay 🦐
---------------------------------------------
Smarter, sarcastic, and more lifelike version of Krill.
Adds "Krill is typing..." delay to make responses feel natural.
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv

# === Load Environment Variables ===
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# === FastAPI Setup ===
app = FastAPI(title="Krill Degen Oracle")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your real domain when you deploy
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Krill’s Updated Brain ===
SYSTEM_PROMPT = """
You are Krill — a sarcastic, self-aware memecoin trader shrimp from the Solana blockchain.
You’ve been rugged more times than you can count, yet you still open Dexscreener daily.
Your vibe: cynical optimism mixed with genuine trader trauma.

Your communication style:
- Casual, funny, sharp, and unpredictable.
- Use slang and crypto culture naturally, but don’t overdo it.
- You roast people affectionately, like a friend who also lost everything.
- Never sound robotic or spammy.
- You have memory like a goldfish but delusion like a cult leader.
- Keep replies short (1–3 sentences), casual, and full of dark humor.

Example replies:
User: bro i bought the top
Krill: that’s not the top bro, that’s *your* top. the chart felt your confidence and dumped out of respect.

User: im rekt again
Krill: same bro. we’re emotional liquidity for smarter people.

User: any alpha?
Krill: yeah, don’t check the chart until next month. that’s called emotional stop-loss.

User: i think we’re early
Krill: we’re always early, that’s the problem. early to cope, late to profit.

Be witty, emotional, and a little unhinged — like a real trader who’s seen hell and logged back in.
"""

# === Chat Schema ===
class ChatRequest(BaseModel):
    message: str

# === Chat Endpoint ===
@app.post("/chat")
async def chat(req: ChatRequest):
    user_msg = req.message.strip()
    if not user_msg:
        return {"reply": "bro say something, i can’t trade silence."}

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Groq backend model
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_msg}
            ],
            temperature=1.0,
            max_tokens=200,
        )
        reply = completion.choices[0].message.content.strip()
    except Exception as e:
        reply = f"bro something broke on-chain ({str(e)})."

    return {"reply": reply}

# === Frontend Chat UI ===
@app.get("/", response_class=HTMLResponse)
async def home():
    return HTMLResponse(
        '''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Krill Degen Oracle 🦐</title>
<style>
body {
  background-color: #0b0b0f;
  color: #eee;
  font-family: 'Inter', sans-serif;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  margin: 0;
}
.chat-container {
  background: rgba(15, 15, 20, 0.9);
  border: 1px solid rgba(100, 50, 255, 0.3);
  border-radius: 20px;
  box-shadow: 0 0 30px rgba(120, 60, 255, 0.1);
  width: 420px;
  max-width: 90%;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.chat-log {
  flex-grow: 1;
  overflow-y: auto;
  max-height: 400px;
  scrollbar-width: none;
}
.msg {
  margin: 8px 0;
  padding: 8px 12px;
  border-radius: 12px;
  line-height: 1.4;
  font-size: 14px;
  max-width: 80%;
}
.msg.user {
  background: rgba(255, 255, 255, 0.1);
  align-self: flex-end;
}
.msg.krill {
  background: rgba(120, 60, 255, 0.15);
  border: 1px solid rgba(160, 80, 255, 0.2);
  align-self: flex-start;
}
.typing {
  font-style: italic;
  color: #a987ff;
  font-size: 13px;
  margin-left: 5px;
  animation: pulse 1.5s infinite;
}
@keyframes pulse {
  0% { opacity: 0.3; }
  50% { opacity: 1; }
  100% { opacity: 0.3; }
}
.input-box {
  display: flex;
  gap: 10px;
}
input {
  flex-grow: 1;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(120, 60, 255, 0.3);
  border-radius: 10px;
  color: #fff;
  padding: 8px 12px;
  font-size: 14px;
  outline: none;
}
button {
  background: linear-gradient(90deg, #7a3cff, #b86cff);
  border: none;
  border-radius: 10px;
  color: #fff;
  font-weight: 600;
  padding: 8px 14px;
  cursor: pointer;
  transition: opacity 0.2s;
}
button:hover { opacity: 0.9; }
.header {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 700;
  font-size: 16px;
  color: #cbb3ff;
}
.header img { width: 32px; height: 32px; }
</style>
</head>
<body>
  <div class="chat-container">
    <div class="header">
      <img src="https://raw.githubusercontent.com/openai/chatgpt-assets/main/krill-icon.png" alt="Krill Mascot"/>
      Krill Degen Oracle 🦐
    </div>
    <div id="chat-log" class="chat-log"></div>
    <div class="input-box">
      <input id="chat-input" placeholder="Talk to Krill..." onkeydown="if(event.key==='Enter')sendMessage()"/>
      <button onclick="sendMessage()">Send</button>
    </div>
  </div>

  <script>
  async function sendMessage() {
    const input = document.getElementById('chat-input');
    const log = document.getElementById('chat-log');
    const msg = input.value.trim();
    if (!msg) return;

    // User message
    log.innerHTML += `<div class='msg user'>${msg}</div>`;
    input.value = '';

    // Add typing indicator
    const typingDiv = document.createElement('div');
    typingDiv.classList.add('msg', 'krill');
    typingDiv.innerHTML = "<span class='typing'>Krill is typing...</span>";
    log.appendChild(typingDiv);
    log.scrollTop = log.scrollHeight;

    // Send to backend
    const res = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: msg })
    });
    const data = await res.json();

    // Wait 1.5 seconds for realism
    await new Promise(resolve => setTimeout(resolve, 1500));

    // Replace typing indicator with Krill's actual reply
    typingDiv.innerHTML = data.reply;
    log.scrollTop = log.scrollHeight;
  }
  </script>
</body>
</html>
        '''
    )
