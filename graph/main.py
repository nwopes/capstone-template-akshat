import os
import json
import sys
from typing import Optional
from dotenv import load_dotenv
from .state import ContractState
from .negotiation import NegotiationSupervisor
from .admin import AdminSupervisor
from .validator import Validator
# Placeholder imports for other subgraphs
# from .research import ResearchSupervisor
# from .drafting import DraftingSupervisor

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
        # self.research_supervisor = ResearchSupervisor()
        # self.drafting_supervisor = DraftingSupervisor()

    def run(self, state: ContractState):
        print(f"--- Orchestrator: Routing to {state.task_category} ---")
        
        # Route to subgraph
        if state.task_category == "admin":
            state = self.admin_supervisor.run(state)
        elif state.task_category in ["create", "improve", "review"]:
            # For now, we route create/improve/review to negotiation as a placeholder 
            # or if specifically requested. 
            # Ideally, this should route to research/drafting/negotiation based on more fine-grained logic
            # or simply route to the requested subgraph.
            # Given the prompt instructions: "create"/"improve"/"review" -> research/drafting/negotiation as appropriate
            # Since we only implemented Negotiation fully in this session (and others are stubs or not requested in this prompt block),
            # we will route to Negotiation for demonstration if it fits, or just print a placeholder.
            
            # However, the user prompt asked to implement Negotiation, Admin, Validator.
            # Research and Drafting are not explicitly asked to be implemented in this prompt, 
            # but they are part of the architecture.
            # We will use Negotiation for now as the active subgraph for these categories 
            # if they don't map to Research/Drafting which might be missing.
            
            # Actually, let's check if we can import Research/Drafting. 
            # They exist in the file system but might be empty or stubs.
            # Let's try to use them if possible, otherwise fallback to Negotiation or just pass.
            
            # For this implementation, I will route to Negotiation if "negotiate" is implied, 
            # otherwise I will just print that Research/Drafting would run here.
            
            # Wait, the prompt says: "create"/"improve"/"review" -> research/drafting/negotiation as appropriate (you may call Supervisor.run placeholders)
            
            if state.task_category == "create":
                 # Placeholder for Research/Drafting
                 print("--- [Placeholder] Running Research & Drafting Subgraphs ---")
                 state.messages.append({"node": "orchestrator", "info": "Routed to Research/Drafting (Placeholder)"})
            elif state.task_category == "improve":
                 # Placeholder for Drafting/Negotiation
                 print("--- [Placeholder] Running Drafting & Negotiation Subgraphs ---")
                 state = self.negotiation_supervisor.run(state)
            elif state.task_category == "review":
                 # Placeholder for Research/Negotiation
                 print("--- [Placeholder] Running Research & Negotiation Subgraphs ---")
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
        json.dump(state.dict(), f, indent=2)
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
    
    # Orchestrator
    orchestrator = Orchestrator()
    orchestrator.run(state)
    
    print("MAIN ORCHESTRATOR READY")
