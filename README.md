# 💬 Denier - Contrarian AI Agent

An AI-powered debate sparring partner built with Microsoft's Agent Framework and Azure OpenAI. Denier is designed to challenge every opinion you present, helping you think critically and strengthen your arguments through adversarial dialogue.

## 🎯 Project Overview

Denier is a conversational AI agent that **never agrees** with you. Its purpose is to play devil's advocate, finding counterarguments to whatever you say. This makes it an excellent tool for:

- **Critical thinking practice** - Test and refine your arguments
- **Debate preparation** - Anticipate counterarguments
- **Educational purposes** - Learn to think from multiple perspectives
- **Fun philosophical discussions** - Challenge your assumptions

## 🏗️ Architecture

### Backend
- **Framework**: Microsoft Agent Framework (latest beta)
- **API**: FastAPI with async/await patterns
- **AI Model**: Azure OpenAI 
- **Observability**: OpenTelemetry for reasoning trace visibility
- **Language**: Python 3.12+

### Frontend
- **Pure HTML/CSS/JavaScript** - No frameworks required
- **Modern UI** with glassmorphism design
- **Real-time chat interface**
- **Responsive design** for mobile and desktop

## 🚀 Getting Started

### Prerequisites

- Python 3.12 or higher
- Azure OpenAI account with API access
- An Azure OpenAI deployment

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/denier-ai-agent.git
cd denier-ai-agent
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**
```bash
cp .env.example .env
```

Edit `.env` with your Azure OpenAI credentials:
```env
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-5-nano
AZURE_OPENAI_API_VERSION=2024-08-01-preview
AZURE_OPENAI_API_KEY=your-api-key-here
```

### Running the Application

1. **Start the backend server**
```bash
uvicorn main:app --reload
```
Or simply:
```bash
python main.py
```

The server will start on `http://localhost:8000`

2. **Open the frontend**

Simply open `index.html` in your web browser:
- Double-click the file, or
- Run: `python -m http.server 8080` and visit `http://localhost:8080`

3. **Start debating!**

Type any opinion and watch Denier argue against it. For example:
- "Pizza is the best food"
- "Exercise is good for you"
- "The sky is blue"

## 📁 Project Structure

```
denier-ai-agent/
│
├── main.py                 # FastAPI backend with Agent Framework
├── script.js              # Frontend JavaScript logic
├── index.html             # Chat interface HTML
├── styles.css             # Modern UI styling
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables template
└── README.md              # This file
```



## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| AI Framework | Microsoft Agent Framework |
| Backend | FastAPI + Python 3.11 |
| AI Model | Azure OpenAI (GPT-4o / o1-series) |
| Frontend | HTML5 + CSS3 + Vanilla JavaScript |
| Observability | OpenTelemetry |
| Authentication | Azure Identity |

## 🔧 Configuration

### Model Selection

In your `.env` file, you can specify different Azure OpenAI models:

```env
# For standard chat (recommended)
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini

# For reasoning models
AZURE_OPENAI_DEPLOYMENT_NAME=o1-mini

# For maximum capability
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
```

### Agent Personality

The agent's contrarian instructions are defined in `main.py`. You can modify the `instructions` parameter when creating the `ChatAgent` to change its behavior.



## 📝 License

MIT License - feel free to use this project for learning and experimentation.


## 📧 Contact

Questions or suggestions? Open an issue or submit a pull request!

---

**Note**: This is an educational project demonstrating the capabilities of AI agents. The contrarian behavior is intentional and designed to encourage critical thinking. Use responsibly! 🧠✨
