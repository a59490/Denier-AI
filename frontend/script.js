const API_URL = "http://localhost:8000";

const chatForm = document.getElementById("chatForm");
const userInput = document.getElementById("userInput");
const chatMessages = document.getElementById("chatMessages");
const suggestionsContainer = document.getElementById("suggestionsContainer");
const suggestionsList = document.getElementById("suggestionsList");

let conversationHistory = [];
let suggestionsLoaded = false;

chatForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const message = userInput.value.trim();
  if (!message) return;

  // Hide suggestions after first message
  if (suggestionsContainer) {
    suggestionsContainer.classList.add("hidden");
  }

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

// Load suggestions from backend
async function loadSuggestions() {
  try {
    const response = await fetch(`${API_URL}/suggestions`);
    if (!response.ok) throw new Error();
    const data = await response.json();

    data.suggestions.forEach((suggestion) => {
      const chip = document.createElement("div");
      chip.className = "suggestion-chip";
      chip.textContent = suggestion;
      chip.addEventListener("click", () => {
        userInput.value = suggestion;
        userInput.focus();
      });
      suggestionsList.appendChild(chip);
    });

    suggestionsLoaded = true;
  } catch (error) {
    console.error("Failed to load suggestions:", error);
    // Hide suggestions container if loading fails
    if (suggestionsContainer) {
      suggestionsContainer.classList.add("hidden");
    }
  }
}

// Backend health check and load suggestions
window.addEventListener("load", async () => {
  try {
    const response = await fetch(`${API_URL}/health`);
    if (!response.ok) throw new Error();
    // Load suggestions if backend is healthy
    await loadSuggestions();
  } catch {
    addMessageToUI(
      "⚠️ Backend not reachable. Start it with: python main.py",
      "assistant"
    );
    // Hide suggestions if backend is down
    if (suggestionsContainer) {
      suggestionsContainer.classList.add("hidden");
    }
  }
});

// Ctrl+Enter sends message
userInput.addEventListener("keydown", (e) => {
  if (e.ctrlKey && e.key === "Enter") chatForm.dispatchEvent(new Event("submit"));
});
