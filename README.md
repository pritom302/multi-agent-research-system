# Multi-Agent Research System

A team of specialised AI agents that research a topic end to end: it searches the web, scrapes the best source, writes a structured report, and has a critic review it. It comes with a clean dark-themed Streamlit interface.

## How it works

```
Topic ──► Search Agent ──► Reader Agent ──► Writer ──► Critic ──► Report + Feedback
```

| Step | Agent | What it does |
|------|-------|--------------|
| 1 | **Search Agent** | Finds recent, reliable information about the topic |
| 2 | **Reader Agent** | Picks the most relevant URL and scrapes it for deeper content |
| 3 | **Writer** | Combines search results and scraped content into a full report |
| 4 | **Critic** | Reviews the report and gives feedback |

## Features

- Four-agent pipeline with live step-by-step progress in the UI
- Dark, modern Streamlit interface
- Results in tabs: final report, critic feedback, search results, scraped content
- One-click download of the report as Markdown
- Can also be run directly from the terminal

## Project structure

```
Multi-Agent-System/
├── app.py             # Streamlit UI
├── pipline.py         # Pipeline that runs the four steps (CLI)
├── agents.py          # Search agent, reader agent, writer chain, critic chain
├── tools.py           # Tools used by the agents (web search, scraping)
├── requirements.txt   # Python dependencies
├── .env               # API keys (not committed)
└── .streamlit/
    └── config.toml    # Dark theme settings
```

## Getting started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/multi-agent-research-system.git
cd multi-agent-research-system
```

### 2. Create a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your API keys

Create a `.env` file in the project root and add the keys your agents and tools need:

```env
# Example - replace with the keys used in agents.py and tools.py
MISTRAL_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
```


## Usage

### Streamlit app

```bash
streamlit run app.py
```

Open the local URL shown in the terminal, type a research topic, and click **Start Research**.

### Command line

```bash
python pipline.py
```

Enter a topic when prompted. Each step prints its output to the terminal.

## Tech stack

- Python
- Streamlit
- LangChain / LangGraph agents

## Roadmap

- [ ] Let the reader agent scrape multiple URLs
- [ ] Add a revision loop where the writer improves the report using the critic's feedback
- [ ] Export the report to PDF
- [ ] Save a history of past research

## License

Add a license of your choice (for example MIT) before sharing publicly.