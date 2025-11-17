const API_URL = "http://localhost:8000";

const chatForm = document.getElementById("chatForm");
const userInput = document.getElementById("userInput");
const chatMessages = document.getElementById("chatMessages");

let conversationHistory = [];

chatForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const message = userInput.value.trim();
  if (!message) return;

  // Add user message
  addMessageToUI(message, "user");
  conversationHistory.push({ role: "user", content: message });
  userInput.value = "";
  userInput.focus();

  try {
    const response = await fetch(`${API_URL}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ messages: conversationHistory }),
    });

    if (!response.ok) throw new Error(`HTTP error ${response.status}`);
    const data = await response.json();
    const assistantMessage = data.response;

    addMessageToUI(assistantMessage, "assistant");
    conversationHistory.push({ role: "assistant", content: assistantMessage });
  } catch (error) {
    console.error(error);
    addMessageToUI(
      "⚠️ Error: Could not connect to backend. Make sure it's running on http://localhost:8000.",
      "assistant"
    );
  }
});

function addMessageToUI(message, role) {
  const messageDiv = document.createElement("div");
  messageDiv.className = `message ${role}`;

  const avatarDiv = document.createElement("div");
  avatarDiv.className = "avatar";
  avatarDiv.textContent = role === "user" ? "🧑" : "🤖";

  const contentDiv = document.createElement("div");
  contentDiv.className = "message-content";
  contentDiv.textContent = message;

  if (role === "user") {
    messageDiv.appendChild(contentDiv);
    messageDiv.appendChild(avatarDiv);
  } else {
    messageDiv.appendChild(avatarDiv);
    messageDiv.appendChild(contentDiv);
  }

  chatMessages.appendChild(messageDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Backend health check
window.addEventListener("load", async () => {
  try {
    const response = await fetch(`${API_URL}/health`);
    if (!response.ok) throw new Error();
  } catch {
    addMessageToUI(
      "⚠️ Backend not reachable. Start it with: python main.py",
      "assistant"
    );
  }
});

// Ctrl+Enter sends message
userInput.addEventListener("keydown", (e) => {
  if (e.ctrlKey && e.key === "Enter") chatForm.dispatchEvent(new Event("submit"));
});
