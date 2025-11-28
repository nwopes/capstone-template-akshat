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
        
        # 2. Clause Writer Agent
        self._clause_writer_agent(state)
        
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

    def _clause_writer_agent(self, state: ContractState):
        print("--- Drafting: Writing Clauses ---")
        prompt = ChatPromptTemplate.from_template(
            "You are a legal drafter. Write a contract clause based on this request: {request} "
            "and these similar templates: {templates}. "
            "Return ONLY the clause text."
        )
        chain = prompt | self.llm | StrOutputParser()
        
        request = state.messages[0]["content"] if state.messages else ""
        templates = "\n\n".join(state.extracted_facts.get("drafting_templates", []))
        
        clause = chain.invoke({"request": request, "templates": templates})
        state.draft_content = clause
        
        state.messages.append({
            "node": "clause_writer",
            "status": "done",
            "content_preview": clause[:50] + "..."
        })

    def _consistency_checker(self, state: ContractState):
        print("--- Drafting: Checking Consistency ---")
        prompt = ChatPromptTemplate.from_template(
            "Check this contract clause for internal consistency and clarity: {clause}. "
            "Return 'Pass' or a list of issues."
        )
        chain = prompt | self.llm | StrOutputParser()
        report = chain.invoke({"clause": state.draft_content})
        
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
