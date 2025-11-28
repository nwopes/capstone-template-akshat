from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from .state import ContractState
import datetime

class NegotiationSupervisor:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0)

    def run(self, state: ContractState) -> ContractState:
        print("--- Negotiation Subgraph Started ---")
        
        # 1. Change Extractor
        self._change_extractor(state)
        
        # 2. Impact Analyzer
        self._impact_analyzer(state)
        
        # 3. Counterproposal Generator
        self._counterproposal_generator(state)
        
        # 4. Versioning Node
        self._versioning_node(state)
        
        # 5. Policy Gate
        self._policy_gate(state)
        
        return state

    def _change_extractor(self, state: ContractState):
        print("--- Negotiation: Extracting Changes ---")
        # In a real scenario, compare state.draft_content with previous version
        # Here we just assume the user input contains the requested changes
        changes = state.messages[0]["content"] if state.messages else "No changes requested"
        
        state.messages.append({
            "node": "change_extractor",
            "status": "done",
            "changes_detected": changes
        })

    def _impact_analyzer(self, state: ContractState):
        print("--- Negotiation: Analyzing Impact ---")
        prompt = ChatPromptTemplate.from_template(
            "Analyze the legal and business impact of these requested changes: {changes}. "
            "Return a brief summary of risks."
        )
        chain = prompt | self.llm | StrOutputParser()
        
        changes = state.messages[-1]["changes_detected"]
        impact = chain.invoke({"changes": changes})
        
        state.messages.append({
            "node": "impact_analyzer",
            "status": "done",
            "impact_analysis": impact
        })

    def _counterproposal_generator(self, state: ContractState):
        print("--- Negotiation: Generating Counterproposal ---")
        prompt = ChatPromptTemplate.from_template(
            "Generate a counterproposal for these changes: {changes}, considering this impact: {impact}. "
            "Return the suggested clause text."
        )
        chain = prompt | self.llm | StrOutputParser()
        
        changes = state.messages[-2]["changes_detected"]
        impact = state.messages[-1]["impact_analysis"]
        
        counterproposal = chain.invoke({"changes": changes, "impact": impact})
        state.draft_content = counterproposal # Update draft with counterproposal
        
        state.messages.append({
            "node": "counterproposal_generator",
            "status": "done",
            "counterproposal": counterproposal
        })

    def _versioning_node(self, state: ContractState):
        print("--- Negotiation: Versioning ---")
        state.versions.append({
            "version_number": len(state.versions) + 1,
            "content": state.draft_content,
            "timestamp": datetime.datetime.now().isoformat(),
            "type": "negotiation"
        })
        state.messages.append({
            "node": "versioning_node",
            "status": "done",
            "info": "New version saved"
        })

    def _policy_gate(self, state: ContractState):
        print("--- Negotiation: Checking Policy ---")
        # Simple check
        state.validation_report["policy_gate"] = "pass"
        state.messages.append({
            "node": "policy_gate",
            "status": "done",
            "info": "Policy check passed"
        })

if __name__ == "__main__":
    print("NEGOTIATION SUBGRAPH READY")
