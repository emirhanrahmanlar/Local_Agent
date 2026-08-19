# Local AI Agent with Tool Calling 🚀

A completely local, privacy-first AI assistant built with Python. This project leverages the **Ollama** engine and **Smolagents** to create an intelligent agent capable of understanding natural language and executing real-time tools—all running entirely on the local machine without relying on external LLM API keys (like OpenAI or Anthropic).

## 🌟 Features

- **100% Local Execution:** Powered by Llama 3.1 (8B) via Ollama, ensuring zero data leakage and complete privacy.
- **Dynamic Tool Calling:** The agent intelligently selects and executes Python functions based on conversational context.
- **Real-Time API Integrations:** 
  - 📰 **Hacker News API:** Fetches the top trending technology stories instantly.
  - 🐙 **GitHub API:** Retrieves public repositories for specific users.
  - 🗄️ **Mock Data APIs:** Simulates database fetching for users and products.
- **Web UI:** Interactive and user-friendly chat interface built with **Gradio**.

## 🛠️ Tech Stack

- **Language:** Python 3
- **LLM Engine:** [Ollama](https://ollama.com/) (Llama 3.1)
- **Agent Framework:** [Smolagents](https://github.com/huggingface/smolagents)
- **UI Framework:** Gradio
- **HTTP Client:** Requests

## 🚀 How to Run

1. **Install Ollama** and download the model:
   ```bash
   ollama run llama3.1
2. Install the required Python packages:
    pip install gradio smolagents requests
3. Start the agent:
    python3 agent.py
4. Open the Web UI:
Open the provided local URL (usually http://127.0.0.1:7860) in your browser and start chatting!


-- Example Prompts to Try ---
"Get top tech news"
"List GitHub repos for torvalds"
"List the users"
"List all products"
Developed by Emirhan Rahmanlar