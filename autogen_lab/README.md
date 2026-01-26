# 🧪 autogen_lab  
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![AutoGen](https://img.shields.io/badge/AutoGen-Lab-purple)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red) 

*A structured learning lab and project playground for agentic AI, AutoGen, and RAG systems.*

This repository brings together two complementary tracks:

- **Tutorials** — guided notebooks and practice scripts that break down AutoGen concepts  
- **Projects** — standalone mini‑systems that demonstrate real agentic workflows  

The goal is to build a space where learning, experimentation, and portfolio‑ready work all live together in a clean, intentional structure.

---

## 📚 Background

This lab began as a structured learning project inspired by the AutoGen crash course on YouTube:  
https://www.youtube.com/watch?v=yDpV_jgO93c

The tutorial provided a solid foundation for understanding the framework. From there, I expanded the codebase with my own experiments, custom tools, and multi‑agent projects — including RAG pipelines, tool‑augmented agents, and interactive frontends — to create a more complete agentic‑AI playground.

---

## 🧱 Repository Structure
```
autogen_lab/
│
├── tutorials/          # Guided learning: notebooks + practice scripts
│   ├── basics/
│
├── projects/           # Portfolio-ready mini-systems
│   ├── research_assistant_agent/
│   └── TODO/
│
└── README.md
```

### **tutorials/**  
A collection of concept‑driven notebooks and scripts that walk through:

- AutoGen basics  
- Building and coordinating agents  
- Tool use and function calling  
- RAG workflows  
- Local LLM integration (e.g., Ollama)  

These are designed as learning artifacts — clean, incremental, and easy to follow.

### **projects/**  
Standalone examples that demonstrate real agentic systems, each with:

- its own folder  
- a dedicated README  
- runnable entry points  
- clear architecture  

Examples include:

- **Literature Review Assistant** (AutoGen + arXiv + Streamlit)  
- **RAG pipelines**  

These are the portfolio‑ready pieces that show how you design and build systems.

---

## 🛠️ Requirements

- Python 3.10+  
- A valid OpenAI API key (stored in `.env`)  
- Recommended: macOS or Linux for best compatibility (Windows supported with minor adjustments)

---

## 🚀 Getting Started
Set up a clean Python environment for the entire lab.

### 1. Create and activate a virtual environment

```bash
python3 -m venv autogen_venv
source autogen_venv/bin/activate   # macOS / Linux
# autogen_venv\Scripts\activate    # Windows
```
### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Create your .env file
A sample environment file is provided:

```bash
cp .env.sample .env
```
Open .env and add your API keys (e.g., OPENAI_API_KEY=).

This .env file is automatically loaded by the tutorials and projects throughout the lab.

> **Note:** This repository’s `.gitignore` excludes virtual environments, `.env` files, 
> notebook checkpoints, and compiled Python files to keep the repo clean.

---

## 🧭 How to Navigate This Lab

- Start in `tutorials/` if you want guided, concept‑by‑concept learning.
- Explore `projects/` if you want runnable, portfolio‑ready examples.
- Each project includes its own README with instructions and architecture notes.

---

## 📌 Running Tutorials and Projects

All notebooks and project scripts should be run **from the repository root**, not from inside
individual folders. This ensures:

- the shared `.env` file is loaded correctly  
- imports resolve without modifying `PYTHONPATH`  
- all tutorials and projects behave consistently  

Examples:

```bash
cd autogen_lab
python projects/literature_review/autogen_backend.py
```

Launching notebooks:
```bash
cd autogen_lab
jupyter lab
```