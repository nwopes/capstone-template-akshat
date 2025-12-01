import os
import json
import sys
from typing import Optional
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from .state import ContractState
from .negotiation import NegotiationSupervisor
from .admin import AdminSupervisor
from .validator import Validator
from .research import ResearchSupervisor
from .drafting import DraftingSupervisor
from tools.memory_store import MemoryStore

# Load environment variables
load_dotenv()

class Router:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0)

    def route(self, text: str) -> str:
        prompt = ChatPromptTemplate.from_template(
            "Classify the user intent into one of these categories: "
            "['create', 'improve', 'review', 'admin', 'chat'].\n"
            "create: User wants to draft/create a new contract, agreement, or legal document.\n"
            "improve: User wants to edit, modify, or improve an existing contract (e.g. 'rewrite this', 'make this better').\n"
            "review: User wants a contract reviewed, analyzed, summarized, or completed (e.g. 'review this', 'fix loopholes', 'complete this').\n"
            "admin: User wants to manage deadlines, signatures, or export files.\n"
            "chat: User is greeting, asking general questions, or not requesting a specific legal task.\n\n"
            "User Input: {text}\n"
            "Category:"
        )
        chain = prompt | self.llm | StrOutputParser()
        category = chain.invoke({"text": text}).strip().lower()
        
        valid_categories = ['create', 'improve', 'review', 'admin', 'chat']
        if category not in valid_categories:
            return "chat"
        return category

class GeneralAssistant:
    def __init__(self, memory_store: MemoryStore):
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
        self.memory_store = memory_store

    def run(self, state: ContractState) -> ContractState:
        print("--- General Assistant ---")
        
        # Retrieve context from memory
        user_input = state.messages[-1]["content"]
        context = self.memory_store.get_context(user_input, session_id=state.session_id)
        context_str = "\n".join(context)
        
        prompt = ChatPromptTemplate.from_template(
            "You are Lexis, a helpful AI legal assistant for freelancers. "
            "Here is some context from previous conversations:\n{context}\n\n"
            "The user said: {input}\n"
            "Respond helpfully and briefly. If they need to draft, review, or negotiate a contract, guide them to ask for that."
        )
        chain = prompt | self.llm | StrOutputParser()
        response = chain.invoke({"input": user_input, "context": context_str})
        
        print(f"Lexis: {response}")
        state.messages.append({"role": "assistant", "content": response})
        
        # Save assistant response to memory
        self.memory_store.add_message("assistant", response, session_id=state.session_id)
        
        return state

class Orchestrator:
    def __init__(self):
        self.negotiation_supervisor = NegotiationSupervisor()
        self.admin_supervisor = AdminSupervisor()
        self.validator = Validator()
        self.research_supervisor = ResearchSupervisor()
        self.drafting_supervisor = DraftingSupervisor()
        self.memory_store = MemoryStore()
        self.general_assistant = GeneralAssistant(self.memory_store)

    def run(self, state: ContractState):
        print(f"--- Orchestrator: Routing to {state.task_category} ---")
        
        # Save user input to memory (if it's a new message)
        if state.messages and state.messages[-1]["role"] == "user":
             self.memory_store.add_message("user", state.messages[-1]["content"], session_id=state.session_id)

        # Route to subgraph
        if state.task_category == "chat":
            state = self.general_assistant.run(state)
            return state # Skip validation for chat
            
        elif state.task_category == "admin":
            state = self.admin_supervisor.run(state)
        elif state.task_category in ["create", "improve", "review"]:
            if state.task_category == "create":
                 state = self.research_supervisor.run(state)
                 state = self.drafting_supervisor.run(state)
            elif state.task_category == "improve":
                 state = self.research_supervisor.run(state)
                 state = self.drafting_supervisor.run(state)
                 # state = self.negotiation_supervisor.run(state) # Removed negotiation for improve, drafting handles rewrite
            elif state.task_category == "review":
                 state = self.research_supervisor.run(state)
                 state = self.drafting_supervisor.run(state)
                 # state = self.negotiation_supervisor.run(state) # Changed to drafting to support "complete this" request
            
        
        # Run Validator
        state = self.validator.run(state)
        
        # Checkpoint
        checkpoint_state(state)
        
        # Summary
        self.print_summary(state)
        
        return state

    def print_summary(self, state: ContractState):
        print("\n" + "="*30)
        print("       📝 MISSION REPORT       ")
        print("="*30)
        print(f"📌 Task Type: {state.task_category.upper()}")
        print(f"💬 Messages Processed: {len(state.messages)}")
        
        print("\n🔍 Validation Results:")
        for check, result in state.validation_report.items():
            if "details" not in check:
                # Fix: Handle non-string results (like readability score)
                display_result = str(result).upper()
                status_icon = "✅" if display_result == "PASS" else "⚠️" if display_result == "WARNING" else "❌"
                if isinstance(result, (int, float)):
                     status_icon = "ℹ️"
                
                print(f"   {status_icon} {check.replace('_', ' ').title()}: {display_result}")
        
        print("\n🤖 Lexis Analysis:")
        self.generate_helpful_feedback(state)
        
        print("="*30 + "\n")

    def generate_helpful_feedback(self, state: ContractState):
        # Use LLM to analyze the report and guide the user
        llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
        prompt = ChatPromptTemplate.from_template(
            "You are Lexis, the AI legal assistant. Analyze this contract task execution.\n"
            "Task: {task}\n"
            "Validation Report: {report}\n"
            "Draft Preview: {preview}\n\n"
            "1. Summarize what was done.\n"
            "2. Identify any critical failures or missing information (e.g. missing payment terms, PII issues).\n"
            "3. Tell the user EXACTLY what information they need to provide next to fix it.\n"
            "4. Be encouraging and helpful.\n"
            "Keep it brief (3-4 sentences)."
        )
        chain = prompt | llm | StrOutputParser()
        
        preview = (state.draft_content or "")[:500]
        report_str = json.dumps(state.validation_report, indent=2)
        
        try:
            feedback = chain.invoke({
                "task": state.task_category,
                "report": report_str,
                "preview": preview
            })
            print(feedback)
        except Exception as e:
            print(f"Could not generate feedback: {e}")

def checkpoint_state(state: ContractState):
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    os.makedirs(data_dir, exist_ok=True)
    filepath = os.path.join(data_dir, "state.json")
    with open(filepath, "w") as f:
        json.dump(state.model_dump(), f, indent=2)
    # print(f"State saved to {filepath}") # Reduce noise

def load_checkpoint() -> ContractState:
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    filepath = os.path.join(data_dir, "state.json")
    if os.path.exists(filepath):
        try:
            with open(filepath, "r") as f:
                data = json.load(f)
            return ContractState(**data)
        except Exception as e:
            # print(f"Error loading checkpoint: {e}")
            return ContractState()
    else:
        return ContractState()

if __name__ == "__main__":
    # CLI Interface
    print("\n🤖 Lexis-Freelance-Local: AI Legal Assistant")
    print("Type 'exit' to quit.\n")
    
    current_session_id = "default"
    
    while True:
        try:
            user_input = input(f"\nUser ({current_session_id}): ")
            if user_input.lower() in ["exit", "quit"]:
                print("Lexis: Goodbye!")
                break
            
            # Session Management Commands
            if user_input.startswith("/session"):
                parts = user_input.split()
                if len(parts) > 1:
                    current_session_id = parts[1]
                    print(f"Switched to session: {current_session_id}")
                else:
                    print(f"Current session: {current_session_id}")
                continue
            elif user_input.startswith("/new"):
                import uuid
                current_session_id = str(uuid.uuid4())[:8]
                print(f"Started new session: {current_session_id}")
                continue
            elif user_input.startswith("/info"):
                print(f"Current Session ID: {current_session_id}")
                continue
            
            # Load or create state (fresh state for chat, load for tasks if needed - simplified to load always)
            state = load_checkpoint()
            state.session_id = current_session_id # Ensure state has current session ID
            
            # Router
            router = Router()
            category = router.route(user_input)
            state.task_category = category
            state.messages.append({"role": "user", "content": user_input})
            
            # Orchestrator
            orchestrator = Orchestrator()
            orchestrator.run(state)
            
        except (KeyboardInterrupt, EOFError):
            print("\nLexis: Goodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
