import gradio as gr
from smolagents import LiteLLMModel, ToolCallingAgent, tool
from api_tools import get_users, get_products, get_user_by_id 
import json 
import requests


# 1. BEYİN
model = LiteLLMModel(
    model_id="ollama/llama3.1",
    api_base="http://localhost:11434"
)

# 2. YETENEKLER (Pis işi artık Python yapıyor, LLM sadece metin kuruyor)
@tool
def get_users_list() -> str:
    """Use this tool ONLY when the user explicitly asks for the full list of users. DO NOT use this tool for greetings or casual chat."""
    raw_data = get_users() # İnternetten devasa veri gelir
    try:
        data = json.loads(raw_data) # Python bunu listeye çevirir
        # Sadece isimleri alıp virgülle birleştiriyoruz
        isimler = [kisi.get("name", "Bilinmeyen") for kisi in data]
        return "Users found: " + ", ".join(isimler)
    except:
        return "Data format error."

@tool
def get_products_list() -> str:
    """Use this tool ONLY when the user explicitly asks for a list of products. DO NOT use for casual chat."""
    raw_data = get_products()
    try:
        data = json.loads(raw_data)
        # Sadece ilk 10 ürünün başlığını (title) alıyoruz ki LLM yorulmasın
        urunler = [urun.get("title", "Bilinmeyen Urun") for urun in data]
        return f"Found {len(urunler)} products: " + ", ".join(urunler)
    except Exception as e:
        return "Data format error."

@tool
def find_user_by_id(user_id: int) -> str:
    """Use this tool ONLY when the user asks for a specific user by their ID number.
    
    Args:
        user_id: The ID number of the user to find
    """
    raw_data = get_user_by_id(user_id)
    try:
        kisi = json.loads(raw_data)
        isim = kisi.get("name", "Bilinmeyen")
        email = kisi.get("email", "Bilinmeyen Email")
        return f"User found. Name: {isim}, Email: {email}"
    except:
        return "User not found."


@tool
def get_github_repos(username: str) -> str:
    """Use this tool to list the public GitHub repositories of a specific GitHub user.
    Args:
        username: The GitHub username to search for (e.g., 'torvalds', 'microsoft')
    """
    try:
        url = f"https://api.github.com/users/{username}/repos"
        response = requests.get(url)
        
        if response.status_code != 200:
            return f"User '{username}' not found or GitHub API limit reached."
            
        data = response.json()
        
        # LLM yorulmasın diye sadece en popüler/ilk 5 repoyu alıyoruz
        repo_isimleri = [repo.get("name") for repo in data[:5]] 
        
        if not repo_isimleri:
            return f"No public repositories found for user {username}."
            
        return f"Top repositories for {username}: " + ", ".join(repo_isimleri)
    except Exception:
        return "Could not fetch GitHub data."



@tool
def get_tech_news() -> str:
    """Use this tool when the user asks for the latest technology news, top tech stories, or Hacker News headlines."""
    try:
        # Önce en popüler haberlerin ID'lerini çekiyoruz
        url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        response = requests.get(url)
        story_ids = response.json()[:5] # Sadece ilk 5 haber
        
        titles = []
        # Her bir ID için haberin başlığını çekiyoruz
        for story_id in story_ids:
            story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
            story_res = requests.get(story_url)
            story_data = story_res.json()
            titles.append(story_data.get("title", "Unknown Title"))
            
        return "Latest Tech News: \n- " + "\n- ".join(titles)
    except Exception:
        return "Could not fetch tech news."


# 3. AJAN OLUŞTURMA (Yeni İngilizce araç isimleri eklendi)
agent = ToolCallingAgent(
    tools=[get_users_list, get_products_list, find_user_by_id, get_github_repos, get_tech_news],
    model=model
)


# 4. ARAYÜZ VE GİZLİ TALİMAT (İngilizce Optimizasyonu)
def ajanla_sohbet(mesaj, gecmis):
    tam_mesaj = f"""You are a helpful and intelligent AI assistant. 
If the user just says hello or greets you, DO NOT use any tools. Just respond naturally.
Only use tools when the user explicitly asks for data.

IMPORTANT RULE: The data returned from tools is long and complex JSON. DO NOT print the raw JSON. Analyze it internally and provide only a short, clean, bulleted list of names or key details.

User's message: {mesaj}"""
    
    cevap = agent.run(tam_mesaj)
    return cevap

arayuz = gr.ChatInterface(
    fn=ajanla_sohbet,
    title="Local Data Assistant 🚀",
    description="Locally running AI assistant powered by MCP architecture and Web Services.",
    examples=["Hello!", "List the users", "Find the user with ID 3"]
)

arayuz.launch()