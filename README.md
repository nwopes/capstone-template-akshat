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
[TODO: Write the title of your project here]

## 2. Overview  
[TODO: Write a simple explanation: what your app does, why it exists, who uses it]

## 3. Reason for choosing this project  
[TODO: Explain how it uses prompting, tools, LangGraph, retrieval, etc.]

## 4. Plan (each step must be committed separately)

Below is the step-by-step plan for executing the full project.  
**For each step:**
- I will change `[TODO]` → `[DONE]` in this README
- I will create **one commit per step**
- Steps must be completed over at least **two different dates**

### ✔️ High-Level Project Steps

- [DONE] Step 1 — Set up folder structure (`capstone-template-akshat`) and initialize repo  
- [DONE] Step 2 — Add `ARCHITECTURE.md` as the canonical system design  
- [TODO] Step 3 — Implement `state.py` (global ContractState model)  
- [TODO] Step 4 — Implement `main.py` (Router → Orchestrator → Validator)  
- [TODO] Step 5 — Implement Research subgraph (all 6 required nodes)  
- [TODO] Step 6 — Implement Drafting subgraph (7 nodes)  
- [TODO] Step 7 — Implement Negotiation subgraph (6 nodes)  
- [TODO] Step 8 — Implement Admin subgraph (4 nodes)  
- [TODO] Step 9 — Implement Validator with all 6 checks  
- [TODO] Step 10 — Implement Tools Layer (template store, doc tools, signatures, payments)  
- [TODO] Step 11 — Load clauses into ChromaDB  
- [TODO] Step 12 — Testing + LangSmith debugging screenshots  
- [TODO] Step 13 — Final cleanup and report completion  

---

## 5. Conclusion

I had planned to achieve:  
[TODO: write intended outcomes]

I believe I have/have not achieved these because:  
[TODO: write reflection]

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

---

# Final Note  
This README.md acts as both the **official project documentation** and the **Capstone Project Report**, with all TODO → DONE traceable through commits.
