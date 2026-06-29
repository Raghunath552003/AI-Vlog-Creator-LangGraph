# 🎬 AI Vlog Content Creator Using LangGraph and LLMs

An AI-powered multi-agent application that automatically researches any topic, writes a ready-to-record vlog script, and generates a complete YouTube SEO package — built using LangGraph, LangChain, and OpenAI GPT-4o-mini.

---

## 🧠 How It Works

Three AI agents work together in a LangGraph pipeline, passing results through shared state:

```
START → Research Agent → Vlog Writer Agent → SEO Optimizer Agent → END
```

### Agent 1 — Research Agent
- Searches the internet using **SerpAPI** (Google Search)
- Falls back to **GPT-4o-mini** knowledge if SerpAPI unavailable
- Returns: topic overview, key facts, latest trends, and insights

### Agent 2 — Vlog Writer Agent
- Takes research summary from Agent 1
- Uses **GPT-4o-mini** to write a full vlog script
- Structure: Hook → Intro → Main segments → Outro/CTA
- Includes stage directions in [brackets]

### Agent 3 — SEO Optimizer Agent
- Takes finished vlog script from Agent 2
- Generates complete **YouTube SEO package:**
  - 3 title options (under 70 characters each)
  - 150-word video description with keywords
  - 15 relevant tags
  - Thumbnail concept with colors and text overlay

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| **Python** | Core programming language |
| **LangGraph** | Multi-agent graph framework |
| **LangChain** | LLM interface and tool wrappers |
| **OpenAI GPT-4o-mini** | Powers all three agents |
| **SerpAPI** | Google Search API for Research Agent |
| **Streamlit** | Web UI — dark themed browser interface |
| **python-dotenv** | Loads API keys securely from .env file |

---

## 🗂️ Project Structure

```
AI-Vlog-Creator/
├── main.py              # Three agents + LangGraph graph
├── app.py               # Streamlit web UI
├── requirements.txt     # Python dependencies
├── .env.example         # API key template
├── .gitignore           # Prevents secrets from uploading
└── README.md            # This file
```

---

## 🔄 Graph Flow

```
┌─────────────────────────────────────────────┐
│                                             │
│   START                                     │
│     │                                       │
│     ▼                                       │
│   Research Agent                            │
│   (SerpAPI + GPT fallback)                  │
│     │                                       │
│     ▼                                       │
│   Vlog Writer Agent                         │
│   (GPT-4o-mini, temp=0.7)                   │
│     │                                       │
│     ▼                                       │
│   SEO Optimizer Agent                       │
│   (GPT-4o-mini, temp=0.5)                   │
│     │                                       │
│     ▼                                       │
│   END                                       │
│                                             │
└─────────────────────────────────────────────┘
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/AI-Vlog-Creator-LangGraph.git
cd AI-Vlog-Creator-LangGraph
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your API keys
Create a `.env` file in project root:
```
OPENAI_API_KEY=sk-proj-your-openai-key-here
SERPAPI_API_KEY=your-serpapi-key-here
```

Get your keys from:
- OpenAI → https://platform.openai.com/api-keys
- SerpAPI → https://serpapi.com/manage-api-key

### 5. Run in terminal
```bash
python main.py
```

### 6. Run as web app
```bash
streamlit run app.py
```
Opens at `http://localhost:8501`

---

## 📦 Dependencies

```
langgraph>=0.2.0
langchain>=0.3.0
langchain-openai>=0.2.0
langchain-community>=0.3.0
google-search-results>=2.4.2
python-dotenv>=1.0.1
streamlit>=1.35.0
```

---

## 🔑 Environment Variables

| Variable | Description | Required |
|---|---|---|
| `OPENAI_API_KEY` | OpenAI API key for GPT-4o-mini | ✅ Yes |
| `SERPAPI_API_KEY` | SerpAPI key for Google Search | ⚡ Optional |

> Note: If SERPAPI_API_KEY is not set, Research Agent automatically falls back to GPT-4o-mini knowledge.

---

## 🖥️ Web UI Features

- 🌑 Dark themed interface
- 📊 Real-time agent status badges
- 🔍 Web source cards with titles and snippets
- 📝 Vlog script in styled display box
- 🎯 SEO package in orange accented box
- ⬇️ Download buttons for script and SEO package

---

## 📊 Shared State (GraphState)

```python
class VlogState(TypedDict):
    topic           : str        # User input topic
    search_results  : List[dict] # Raw web search results
    research_summary: str        # Formatted research text
    vlog_script     : str        # Generated vlog script
    seo_output      : str        # YouTube SEO package
```

---

## 💡 Example Output

**Input:** `Artificial Intelligence trends 2026`

**Research Agent finds:**
- Latest AI developments from web
- Key facts and trends
- Real world applications

**Vlog Writer Agent generates:**
- Attention grabbing hook
- Structured main content with 4-5 segments
- Strong outro with call to action
- Stage directions throughout

**SEO Agent generates:**
- 3 YouTube title options
- Full 150 word description
- 15 relevant tags
- Thumbnail design concept

---

## 🗺️ Roadmap

- [x] Research Agent with SerpAPI + GPT fallback
- [x] Vlog Writer Agent
- [x] SEO Optimizer Agent
- [x] Streamlit Web UI with dark theme
- [x] Download buttons for script and SEO
- [ ] RAG — read from PDFs and websites
- [ ] Auto save scripts to local folder
- [ ] Deploy to Streamlit Cloud
- [ ] Add more agents for thumbnail generation

---

## 🤝 Author

**Sirekolam Raghunath Reddy**
- GitHub: https://github.com/Raghunath552003

---

## 📄 License

MIT License — free to use and modify.
