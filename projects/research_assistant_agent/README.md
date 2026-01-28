# Research Assistant AGent (AutoGen + Streamlit)

A two‑agent AutoGen system that performs an automated literature review using the arXiv API.  
The system consists of:

- **search_agent** — crafts arXiv queries and retrieves candidate papers  
- **summarizer** — generates a structured Markdown literature review  
- **Streamlit frontend** — provides a simple UI and streams the agent conversation in real time  

This project demonstrates tool‑augmented agents, multi‑agent orchestration, and a lightweight frontend for interactive AI workflows.

---

## 🚀 Features

- Multi‑agent workflow using AutoGen’s `RoundRobinGroupChat`
- Tool‑enabled agent that calls a custom `arxiv_search` function
- Streaming output for real‑time interaction
- Clean separation of backend logic and frontend UI
- Fully asynchronous pipeline
- Minimal, reproducible example suitable for learning or extension

---

## 📂 Project Structure
research_assistant_agent/
│
├── autogen_backend.py        # Multi-agent orchestration + arXiv tool
├── autogen_frontend_streamlit.py
├── requirements.txt
└── README.md


---

## 🧠 How It Works

1. The **search_agent** receives the user’s topic and:
   - crafts an arXiv query  
   - fetches 5× the requested number of papers  
   - down‑selects the top N  
   - returns a compact JSON list  

2. The **summarizer** receives the JSON and produces:
   - a short introduction  
   - one bullet per paper  
   - a final takeaway sentence  

3. The **Streamlit frontend**:
   - collects user input  
   - streams the agent conversation  
   - displays the final review  

---

## 🛠️ Setup

Create and activate a virtual environment:

```bash
python3 -m venv .autogen_venv
source .venv/bin/activate   # macOS / Linux
# .venv\Scripts\activate    # Windows (if needed)

pip install -r requirements.txt
```

---

## ▶️ Running the App
Run the Streamlit frontend:  
```bash
streamlit run autogen_frontend_streamlit.py
```

App will open at
```
http://localhost:8501
```

