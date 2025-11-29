# MAT496 Capstone Project  
# Project Title: [TODO: Add your project title]

This repository contains my MAT496 Capstone Project submission.

The main purpose of this project is to demonstrate mastery of the topics taught in the course:

- Prompting  
- Structured Output  
- Semantic Search  
- Retrieval Augmented Generation (RAG)  
- Tool Calling + MCP  
- LangGraph: State, Nodes, Graph  
- LangSmith debugging

My project follows the architecture defined in `docs/ARCHITECTURE.md` and implements a full LangGraph-based multi-agent system.

---

# 📌 PROJECT REPORT (As required by the assignment)

## 1. Title  
Lexis-Freelance-Local: AI Legal Assistant for Freelancers

## 2. Overview  
Lexis-Freelance-Local is a local-only, CLI-driven tool designed to help freelancers generate, review, and negotiate service contracts. It uses a multi-agent architecture to research legal precedents, draft clauses, analyze changes, and manage administrative tasks like scheduling and invoicing, all without sending sensitive data to a cloud server (except for LLM inference).

## 3. Reason for choosing this project  
This project demonstrates advanced usage of:
- **LangGraph** for orchestrating complex, multi-step workflows (Research, Drafting, Negotiation, Admin).
- **Tool Calling** for generating documents (PDF/DOCX) and managing signatures.
- **Retrieval Augmented Generation (RAG)** using ChromaDB to fetch relevant legal clauses.
- **Structured Output** for strict adherence to data models (ContractState).
- **Prompt Engineering** to guide agents in specific legal tasks without hallucination.

## 4. Plan (each step must be committed separately)

Below is the step-by-step plan for executing the full project.  
**For each step:**
- I will change `[TODO]` → `[DONE]` in this README
- I will create **one commit per step**
- Steps must be completed over at least **two different dates**

### ✔️ High-Level Project Steps

- [DONE] Step 1 — Set up folder structure (`capstone-template-akshat`) and initialize repo  
- [DONE] Step 2 — Add `ARCHITECTURE.md` as the canonical system design  
- [DONE] Step 3 — Implement `state.py` (global ContractState model)  
- [x] Step 4 — Implement `main.py` (Router → Orchestrator → Validator)  
- [x] Step 5 — Implement Research subgraph (all 6 required nodes)  
- [x] Step 6 — Implement Drafting subgraph (7 nodes)  
- [DONE] Step 7 — Implement Negotiation subgraph (6 nodes)  
- [x] Step 8 — Implement Admin subgraph (4 nodes)  
- [x] Step 9 — Implement Validator with all 6 checks  
- [x] Step 10 — Implement Tools Layer (template store, doc tools, signatures, payments)  
- [x] Step 11 — Load clauses into ChromaDB  
- [x] Step 12 — Testing + LangSmith debugging screenshots  
- [x] Step 13 — Final cleanup and report completion  

### Phase 2: Real AI Integration
- [x] Install dependencies (`langchain`, `openai`, `chromadb`, `presidio`)
- [x] Implement `template_store.py` with ChromaDB + OpenAI Embeddings
- [x] Implement `research.py` with ChatOpenAI chains
- [x] Implement `drafting.py` with ChatOpenAI chains
- [x] Implement `negotiation.py` with ChatOpenAI chains
- [x] Implement `admin.py` with ChatOpenAI chains
- [x] Implement `validator.py` with Presidio PII scan + ChatOpenAI checks
- [x] Verify full workflow with real AI calls  
- [x] Improve CLI UX (LLM Router + General Assistant)
- [x] Improve CLI UX (LLM Router + General Assistant)
- [x] Step 13 — Final cleanup and report completion

### Phase 3: Persistence & Memory
- [x] Implement `tools/memory_store.py` (ChromaDB)
- [x] Integrate Memory Store into `graph/main.py`
- [x] Verify message persistence and context retrieval

### Phase 4: Robustness & Feedback
- [x] Improve Error Handling (Fix crashes)
- [x] Implement Smart Feedback (LLM-based guidance)

### Features
- **Natural Language Interface**: Chat with Lexis to get help or guidance.
- **Smart Routing**: Automatically detects if you want to create, improve, review, or manage contracts.
- **Real AI Integration**: Uses GPT-4o for all logic and reasoning.
- **Conversation Memory**: Remembers your name and context across sessions using ChromaDB.
- **Smart Feedback**: Analyzes failures and tells you exactly what information is missing.
- **Local Privacy**: Documents are processed locally; only text is sent to LLM.

---

## 5. Conclusion

I had planned to achieve:  
A fully functional, local-first legal assistant that can autonomously draft and negotiate contracts using a multi-agent system.

I believe I have achieved these because:  
I have implemented all the core subgraphs (Research, Drafting, Negotiation, Admin) and the Validator. The system successfully routes user requests, executes the appropriate workflow, and produces valid outputs. The modular architecture allows for easy extension, and the local tool integration ensures data privacy where possible. All planned steps have been executed and verified.

---

# 🚨 CAPSTONE RULES COMPLIANCE CHECKLIST

- Solo work — I am responsible for the code  
- Commit history must show progress for each planned step  
- Commits must span at least **two dates**  
- Each step in plan must have:  
  - `[TODO]` → `[DONE]`  
  - A corresponding commit  
- Submission deadline: **Nov 30, Sunday 11:59 pm**

---

# 🧩 Project Structure

This repository must contain the *exact* structure:

capstone-template-akshat/
├── graph
│ ├── state.py
│ ├── main.py
│ ├── research.py
│ ├── drafting.py
│ ├── negotiation.py
│ ├── admin.py
│ └── validator.py
├── tools
│ ├── template_store.py
│ ├── doc_tools.py
│ ├── signature_tools.py
│ └── payment_tools.py
├── clauses
│ ├── payment.txt
│ ├── scope.txt
│ └── termination.txt
├── data
│ └── vector_db/
├── docs
│ └── ARCHITECTURE.md
├── requirements.txt
├── .env
└── README.md

yaml
Copy code

---

# ✔️ Technologies Used  
- **LangChain**  
- **LangGraph**  
- **LangChain OpenAI wrappers**  
- **ChromaDB**  
- **Presidio Analyzer**  
- **python-docx & reportlab**  
- **python-dotenv**
- **Tavily API** (for internet research)

---

# 🚀 How to Run

### 1. Prerequisites
- Python 3.11+
- OpenAI API Key

### 2. Setup
1.  **Clone the repository**:
    ```bash
    git clone <your-repo-url>
    cd capstone-template-akshat
    ```
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    python -m presidio_analyzer download en
    ```
3.  **Configure Environment**:
    Create a `.env` file in the root directory:
    ```env
    OPENAI_API_KEY=sk-your-key-here
    LANGCHAIN_TRACING_V2=true
    LANGCHAIN_API_KEY=lsv2-your-key-here (optional)
    ```

### 3. Usage
Run the CLI application:
```bash
python -m graph.main
```

**Interactive Commands:**
- Say **"Hi"** to chat with Lexis.
- Say **"Draft a contract for web design"** to start the drafting workflow.
- Say **"Review this contract"** to start the review workflow.
- Say **"My name is [Name]"** to test the memory.

---

---

# Final Note  
This README.md acts as both the **official project documentation** and the **Capstone Project Report**, with all TODO → DONE traceable through commits.
