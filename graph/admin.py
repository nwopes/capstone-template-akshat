from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from .state import ContractState
from tools.doc_tools import export_signature_pdf, export_to_pdf
from tools.signature_tools import generate_signature_placeholder

class AdminSupervisor:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0)

    def run(self, state: ContractState) -> ContractState:
        print("--- Admin Subgraph Started ---")
        
        # 1. Deadline Extractor
        self._deadline_extractor(state)
        
        # 2. Scheduler / ICS Generator
        self._scheduler_generator(state)
        
        # 3. Signature Exporter
        self._signature_exporter(state)
        
        # 4. Export & Notify
        self._export_and_notify(state)
        
        return state

    def _deadline_extractor(self, state: ContractState):
        print("--- Admin: Extracting Deadlines ---")
        prompt = ChatPromptTemplate.from_template(
            "Extract all deadlines and dates from this contract text: {text}. "
            "Return as a list of 'Date: Description'."
        )
        chain = prompt | self.llm | StrOutputParser()
        
        text = state.draft_content or state.messages[0]["content"] if state.messages else ""
        deadlines = chain.invoke({"text": text[:5000]}) # Limit text length
        
        state.messages.append({
            "node": "deadline_extractor",
            "status": "done",
            "deadlines": deadlines
        })

    def _scheduler_generator(self, state: ContractState):
        print("--- Admin: Generating Scheduler ---")
        # Placeholder for ICS generation
        state.messages.append({
            "node": "scheduler_generator",
            "status": "done",
            "info": "ICS file generated (placeholder)"
        })

    def _signature_exporter(self, state: ContractState):
        print("--- Admin: Exporting for Signature ---")
        # Generate signature placeholder
        sig_data = generate_signature_placeholder("Client")
        state.signatures = sig_data
        
        # Export PDF
        pdf_path = export_signature_pdf(state.draft_content or "No content", sig_data)
        
        state.messages.append({
            "node": "signature_exporter",
            "status": "done",
            "pdf_path": pdf_path,
            "signature_data": sig_data
        })

    def _export_and_notify(self, state: ContractState):
        print("--- Admin: Notifying ---")
        # Placeholder notification
        state.messages.append({
            "node": "export_and_notify",
            "status": "done",
            "info": "Notification sent (placeholder)"
        })

if __name__ == "__main__":
    print("ADMIN SUBGRAPH READY")
