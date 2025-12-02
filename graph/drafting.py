from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from .state import ContractState
import datetime
from tools.template_store import TemplateStore

class DraftingSupervisor:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0)
        self.template_store = TemplateStore()

    def run(self, state: ContractState) -> ContractState:
        print("--- Drafting Subgraph Started ---")
        
        # 1. Template Retriever
        self._template_retriever(state)
        
        # 2. Contract Writer Agent
        self._contract_writer_agent(state)
        
        # 3. Consistency & Readability Checker
        self._consistency_checker(state)
        
        # 4. Draft Assembler
        self._draft_assembler(state)
        
        # 5. Redline Generator
        self._redline_generator(state)
        
        # 6. Draft Audit Node
        self._draft_audit(state)
        
        return state

    def _template_retriever(self, state: ContractState):
        print("--- Drafting: Retrieving Templates ---")
        # Use the research plan or context to find templates
        query = state.messages[0]["content"] if state.messages else "contract"
        results = self.template_store.search(query)
        state.extracted_facts["drafting_templates"] = results
        state.messages.append({
            "node": "template_retriever",
            "status": "done",
            "found": len(results)
        })

    def _contract_writer_agent(self, state: ContractState):
        print("--- Drafting: Writing Contract ---")
        prompt = ChatPromptTemplate.from_template(
            "You are an expert legal drafter. Your task is to {task_type} a contract based on this brief: {brief}. "
            "Use the provided structure: {structure}. "
            "Incorporate these market terms/pricing: {market_terms}. "
            "Use similar templates for reference: {templates}. "
            "CURRENT DRAFT (for improvements): {current_draft}\n"
            "CRITICAL: The brief contains specific extracted values (JSON). YOU MUST USE THESE VALUES to fill in the contract. "
            "For example, if the brief says {{'CLIENT_NAME': 'Acme Corp'}}, you must write 'Acme Corp' in the contract, NOT '[CLIENT_NAME]'. "
            "Only use placeholders like [PARTY_NAME] if the value is TRULY missing from the brief. "
            "If improving, review the CURRENT DRAFT and fix any issues, consistency warnings, or missing sections. "
            "Do not make up values. "
            "IF TASK IS 'REVIEW': Start the output with a section called '## Contract Review Report'. "
            "In this report, bullet point: 1) What is Good/Strong, 2) What is Weak/Risky, 3) What is Missing. "
            "Then, provide the full rewritten/improved contract below it. "
            "At the very end of the contract, add a section called '## Suggestions & Improvements'. "
            "In this section, list 2-3 specific clauses or protections that are missing from the user's request but would be beneficial (e.g., Indemnification, Non-Solicitation, Force Majeure). "
            "Explain WHY they are important. "
            "Return the full contract text in Markdown format."
        )
        chain = prompt | self.llm | StrOutputParser()
        
        task_type = state.task_category if state.task_category else "create"
        
        # Find brief message
        brief_msg = next((m for m in state.messages if m.get("node") == "synthesizer"), {})
        
        templates = "\n\n".join(state.extracted_facts.get("drafting_templates", []))
        
        contract = chain.invoke({
            "task_type": task_type,
            "brief": brief_msg.get("brief", "") + "\n\nEXTRACTED FACTS:\n" + state.extracted_facts.get("key_info", ""), 
            "structure": state.contract_structure,
            "market_terms": state.market_terms,
            "templates": templates,
            "current_draft": state.draft_content or "No existing draft."
        })
        state.draft_content = contract
        
        state.messages.append({
            "node": "contract_writer",
            "status": "done",
            "content_preview": contract[:100] + "..."
        })

    def _consistency_checker(self, state: ContractState):
        print("--- Drafting: Checking Consistency ---")
        prompt = ChatPromptTemplate.from_template(
            "Check this contract for internal consistency, clarity, and placeholder usage: {contract}. "
            "Ensure all necessary sections are present. "
            "Return 'Pass' or a list of issues/missing information."
        )
        chain = prompt | self.llm | StrOutputParser()
        report = chain.invoke({"contract": state.draft_content})
        
        state.validation_report["drafting_consistency"] = report
        state.messages.append({
            "node": "consistency_checker",
            "status": "done",
            "report": report
        })

    def _draft_assembler(self, state: ContractState):
        print("--- Drafting: Assembling Draft ---")
        # In a real app, this would combine multiple clauses. Here we just use the single clause.
        full_draft = f"DRAFT CONTRACT\n\n{state.draft_content}\n\n[End of Draft]"
        state.draft_content = full_draft
        state.messages.append({
            "node": "draft_assembler",
            "status": "done",
            "info": "Draft assembled"
        })

    def _redline_generator(self, state: ContractState):
        print("--- Drafting: Generating Redlines ---")
        # Simple placeholder for diff
        state.messages.append({
            "node": "redline_generator",
            "status": "done",
            "info": "No previous version to diff against"
        })

    def _draft_audit(self, state: ContractState):
        print("--- Drafting: Auditing ---")
        state.versions.append({
            "version_number": len(state.versions) + 1,
            "content": state.draft_content,
            "type": "draft"
        })
        state.messages.append({
            "node": "draft_audit",
            "status": "done",
            "info": "Draft version saved"
        })

if __name__ == "__main__":
    print("DRAFTING SUBGRAPH READY")
