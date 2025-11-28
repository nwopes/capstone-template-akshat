import os
import json
import sys
from typing import Optional
from dotenv import load_dotenv
from .state import ContractState
from .negotiation import NegotiationSupervisor
from .admin import AdminSupervisor
from .validator import Validator
from .research import ResearchSupervisor
from .drafting import DraftingSupervisor

# Load environment variables
load_dotenv()

class Router:
    @staticmethod
    def route(text: str) -> str:
        text = text.lower()
        if "create" in text:
            return "create"
        elif "improve" in text:
            return "improve"
        elif "review" in text:
            return "review"
        elif "admin" in text:
            return "admin"
        else:
            return "create" # Fallback

class Orchestrator:
    def __init__(self):
        self.negotiation_supervisor = NegotiationSupervisor()
        self.admin_supervisor = AdminSupervisor()
        self.validator = Validator()
        self.research_supervisor = ResearchSupervisor()
        self.drafting_supervisor = DraftingSupervisor()

    def run(self, state: ContractState):
        print(f"--- Orchestrator: Routing to {state.task_category} ---")
        
        # Route to subgraph
        if state.task_category == "admin":
            state = self.admin_supervisor.run(state)
        elif state.task_category in ["create", "improve", "review"]:
            if state.task_category == "create":
                 state = self.research_supervisor.run(state)
                 state = self.drafting_supervisor.run(state)
            elif state.task_category == "improve":
                 state = self.drafting_supervisor.run(state)
                 state = self.negotiation_supervisor.run(state)
            elif state.task_category == "review":
                 state = self.research_supervisor.run(state)
                 state = self.negotiation_supervisor.run(state)
            
        
        # Run Validator
        state = self.validator.run(state)
        
        # Checkpoint
        checkpoint_state(state)
        
        # Summary
        print("\n--- Final Summary ---")
        print(f"Task: {state.task_category}")
        print(f"Messages: {len(state.messages)}")
        print(f"Validation: {state.validation_report}")
        
        return state

def checkpoint_state(state: ContractState):
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    os.makedirs(data_dir, exist_ok=True)
    filepath = os.path.join(data_dir, "state.json")
    with open(filepath, "w") as f:
        json.dump(state.model_dump(), f, indent=2)
    print(f"State saved to {filepath}")

def load_checkpoint() -> ContractState:
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    filepath = os.path.join(data_dir, "state.json")
    if os.path.exists(filepath):
        try:
            with open(filepath, "r") as f:
                data = json.load(f)
            return ContractState(**data)
        except Exception as e:
            print(f"Error loading checkpoint: {e}")
            return ContractState()
    else:
        return ContractState()

if __name__ == "__main__":
    # CLI Interface
    print("--- Lexis-Freelance-Local CLI ---")
    user_input = input("Input: ")
    
    # Load or create state
    state = load_checkpoint()
    
    # Router
    router = Router()
    category = router.route(user_input)
    state.task_category = category
    state.messages.append({"role": "user", "content": user_input})
    
    # Orchestrator
    orchestrator = Orchestrator()
    orchestrator.run(state)
    
    print("MAIN ORCHESTRATOR READY")
