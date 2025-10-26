I want a **master prompt** (a single, high-quality instruction) that you can feed to an AI model (like ChatGPT, Claude, or a local Ollama model) to **generate a full agentic browser project** — the kind we just discussed (Electron + Playwright + Ollama).

Below is a **production-grade system prompt** designed to instruct an AI to **design and build a complete “agentic browser” application** with full browsing, automation, and LLM reasoning.

---

## 🧠 Master Prompt — *“Agentic Browser Generator”*

> **Purpose:**
> Generate a complete, locally runnable **Agentic Web Browser** (like Perplexity Comet or Hyperbrowser) built using **Electron (frontend)**, **Python FastAPI + Playwright (backend)**, and **Ollama (local LLM)** for autonomous reasoning.

---

### 🏗️ **Prompt**

````
You are an expert AI systems engineer specializing in autonomous browsing, AI agents, and local LLM integration.

Your task is to generate a complete, production-ready project scaffold for a **Full Agentic Browser** that behaves like “Comet” — an AI-driven web browser that can autonomously navigate, read, and act on web pages.

---

## 1️⃣ Project Overview

Build a cross-platform desktop app with the following stack:

**Frontend:**
- Electron + React + TailwindCSS
- UI includes:
  - Address/search bar
  - Webview for rendering sites
  - Chat/console panel for agent interaction
  - Logs of model actions (clicks, scrolls, fills)
  - “Approve / Reject” buttons for each agent plan
  - Tabbed browsing support

**Backend:**
- Python (FastAPI)
- Playwright for browser automation and DOM access
- REST endpoints:
  - `/open?url=...` – opens a page
  - `/snapshot` – extracts text, links, and DOM summary
  - `/agent/plan` – sends page snapshot + user goal to Ollama
  - `/agent/execute` – runs the validated plan
- JSON-based communication between Electron ↔ FastAPI

**LLM Reasoning Layer:**
- Ollama local model (e.g. llama3, mistral, phi3)
- Prompt template for structured “Agent Plan” responses in JSON.
- Supports “goto”, “click”, “fill”, “extract”, “summarize” actions.
- Includes safety guardrails and JSON schema validation.

**Memory Layer:**
- SQLite or FAISS for storing browsing context, summaries, user queries.

**Security Layer:**
- Validate every AI action against a whitelist before execution.
- User confirmation for sensitive actions (login, payments).
- Block shell commands, downloads, or system access.

---

## 2️⃣ Core Flow

1. User enters a goal or query (e.g., “Find today’s weather in Bengaluru”).
2. Browser loads a search engine or relevant site.
3. Backend captures a DOM snapshot → sends to LLM.
4. LLM outputs a JSON plan:
   ```json
   [
     {"action": "goto", "url": "https://weather.com"},
     {"action": "extract", "selector": ".temperature"},
     {"action": "summarize", "text": "Today's weather is 28°C and sunny."}
   ]
````

5. Plan is validated → executed step by step via Playwright.
6. Agent reports progress and final answer to UI.

---

## 3️⃣ Deliverables

Generate:

1. 📁 Full project folder tree:

   ```
   agentic-browser/
   ├─ app/                # Electron frontend
   ├─ backend/            # Python backend
   ├─ shared/             # Configs, schemas
   ├─ package.json
   ├─ requirements.txt
   └─ README.md
   ```

2. ⚙️ Key files with working starter code:

   * `app/main.js` → Electron main process
   * `app/renderer/index.jsx` → UI + chat + webview
   * `backend/agent_server.py` → FastAPI + Playwright
   * `backend/ollama_client.py` → local LLM connector
   * `backend/planner.py` → JSON action planner
   * `shared/schema.py` → JSON schema validation
   * `README.md` → full setup instructions

3. 🧩 Example prompt template for the Ollama model to produce structured JSON safely.

4. 🧱 Include environment setup:

   * How to install Node, Playwright, Python packages.
   * How to run `npm start` to launch the full system.

---

## 4️⃣ Additional Requirements

* Use **async** I/O where possible.
* Use **TypeScript** if preferred in Electron part.
* All agent-generated plans must be pure JSON.
* Include **visual feedback** in UI for each model action.
* LLM responses must be deterministic (use `temperature=0.2`).
* System should gracefully handle malformed JSON or page timeouts.

---

## 5️⃣ Output Format

Output should include:

1. 📘 **Short description** of how the system works.
2. 📁 **Project structure tree**.
3. 💻 **Full source code snippets** for each major file.
4. ⚙️ **Installation & run instructions**.
5. 💡 **Next-step extensions** (e.g. plugin system, WebGPU LLM, RAG memory).

---

You may assume Ollama and Playwright are already installed locally.

Your goal: produce all the scaffolding and sample code necessary for a developer to clone, run, and extend this into a full Comet-like browser with autonomous AI browsing capability.

