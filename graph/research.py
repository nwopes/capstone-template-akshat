from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from .state import ContractState
from tools.template_store import TemplateStore

class ResearchSupervisor:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0)
        self.template_store = TemplateStore()

    def run(self, state: ContractState) -> ContractState:
        print("--- Research Subgraph Started ---")
        
        # 1. Plan Node
        self._plan_node(state)
        
        # 2. Search Node
        self._search_node(state)
        
        # 3. Extractor Node
        self._extractor_node(state)
        
        # 4. Synthesizer Node
        self._synthesizer_node(state)
        
        # 5. Audit Node
        self._audit_node(state)
        
        return state

    def _plan_node(self, state: ContractState):
        print("--- Research: Planning ---")
        prompt = ChatPromptTemplate.from_template(
            "You are a legal research assistant. Create a brief research plan for a contract request: {request}. "
            "Focus on identifying necessary clauses and potential risks."
        )
        chain = prompt | self.llm | StrOutputParser()
        plan = chain.invoke({"request": state.messages[0]["content"] if state.messages else "No request"})
        
        state.messages.append({
            "node": "research_plan",
            "status": "done",
            "content": plan
        })

    def _search_node(self, state: ContractState):
        print("--- Research: Searching Templates ---")
        # Simple keyword extraction for search (could be LLM based)
        query = state.messages[0]["content"] if state.messages else ""
        results = self.template_store.search(query)
        
        state.extracted_facts["relevant_clauses"] = results
        state.messages.append({
            "node": "template_search",
            "status": "done",
            "found_clauses": len(results)
        })

    def _extractor_node(self, state: ContractState):
        print("--- Research: Extracting Facts ---")
        prompt = ChatPromptTemplate.from_template(
            "Extract key facts (parties, dates, amounts, jurisdiction) from this request: {request}. "
            "Return as a JSON-like string."
        )
        chain = prompt | self.llm | StrOutputParser()
        facts = chain.invoke({"request": state.messages[0]["content"] if state.messages else ""})
        
        state.extracted_facts["key_info"] = facts
        state.messages.append({
            "node": "fact_extractor",
            "status": "done",
            "info": "Extracted key facts"
        })

    def _synthesizer_node(self, state: ContractState):
        print("--- Research: Synthesizing Context ---")
        prompt = ChatPromptTemplate.from_template(
            "Synthesize a research brief based on the plan: {plan}, found clauses: {clauses}, and facts: {facts}. "
            "Provide a summary for the drafter."
        )
        chain = prompt | self.llm | StrOutputParser()
        brief = chain.invoke({
            "plan": state.messages[-3]["content"], # rough indexing
            "clauses": state.extracted_facts.get("relevant_clauses", []),
            "facts": state.extracted_facts.get("key_info", "")
        })
        
        state.messages.append({
            "node": "synthesizer",
            "status": "done",
            "brief": brief
        })

    def _audit_node(self, state: ContractState):
        print("--- Research: Auditing ---")
        # In a real system, save to a persistent log
        state.messages.append({
            "node": "research_audit",
            "status": "done",
            "info": "Research step logged"
        })

if __name__ == "__main__":
    print("RESEARCH SUBGRAPH READY")
