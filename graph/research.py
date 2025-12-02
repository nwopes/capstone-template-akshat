from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from .state import ContractState
from .state import ContractState
from tools.template_store import TemplateStore
try:
    from langchain_tavily import TavilySearchResults
except ImportError:
    from langchain_community.tools.tavily_search import TavilySearchResults

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

        # 2b. Structure Research Node (Tavily)
        self._structure_research_node(state)

        # 2c. Market Research Node (Tavily)
        self._market_research_node(state)
        
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

    def _structure_research_node(self, state: ContractState):
        print("--- Research: Structure Research (Tavily) ---")
        try:
            tool = TavilySearchResults(max_results=2)
            request = state.messages[0]["content"] if state.messages else ""
            query = f"standard contract structure outline for {request}"
            results = tool.invoke({"query": query})
            
            structure_info = []
            for res in results:
                content = res.get('content', res.get('body', str(res)))
                structure_info.append(f"- {content}")
            
            state.contract_structure = "\n".join(structure_info)
            state.messages.append({
                "node": "structure_research",
                "status": "done",
                "info": "Found contract structure"
            })
        except Exception as e:
            print(f"Structure search failed: {e}")
            state.contract_structure = "Could not retrieve structure."

    def _market_research_node(self, state: ContractState):
        print("--- Research: Market Pricing (Tavily) ---")
        try:
            tool = TavilySearchResults(max_results=3)
            # Construct a query for pricing
            request = state.messages[0]["content"] if state.messages else ""
            request = state.messages[0]["content"] if state.messages else ""
            query = f"standard terms and market price rate for {request} freelance contract"
            results = tool.invoke({"query": query})
            
            # Extract relevant info (simplified)
            pricing_info = []
            for res in results:
                content = res.get('content', res.get('body', str(res)))
                pricing_info.append(f"- {content}")
            
            state.market_terms = "\n".join(pricing_info)
            state.extracted_facts["market_pricing"] = state.market_terms # Keep for backward compatibility
            state.messages.append({
                "node": "market_research",
                "status": "done",
                "info": "Found market pricing data"
            })
        except Exception as e:
            print(f"Tavily search failed: {e}")
            state.extracted_facts["market_pricing"] = "Could not retrieve market pricing."

    def _extractor_node(self, state: ContractState):
        print("--- Research: Extracting Facts ---")
        prompt = ChatPromptTemplate.from_template(
            "Extract all key facts and specific details from this request: {request}. "
            "The user might provide data in a format like '[KEY]Value' or just natural language. "
            "Return a valid JSON object where keys are the placeholder names (e.g., 'CLIENT_NAME', 'DATE') and values are the extracted content. "
            "Example Input: '[DATE]2024-01-01 [NAME]John Doe' -> Output: {{'DATE': '2024-01-01', 'NAME': 'John Doe'}}"
        )
        chain = prompt | self.llm | StrOutputParser()
        facts_json = chain.invoke({"request": state.messages[0]["content"] if state.messages else ""})
        
        # Clean up json
        facts_json = facts_json.replace("```json", "").replace("```", "").strip()
        
        state.extracted_facts["key_info"] = facts_json
        state.messages.append({
            "node": "fact_extractor",
            "status": "done",
            "info": "Extracted key facts"
        })

    def _synthesizer_node(self, state: ContractState):
        print("--- Research: Synthesizing Context ---")
        prompt = ChatPromptTemplate.from_template(
            "Synthesize a comprehensive Contract Brief based on the plan: {plan}, structure: {structure}, market terms: {market_terms}, and facts: {facts}. "
            "If the user provided an existing contract/draft (in facts or request), analyze it against the structure and market terms. "
            "The brief should outline the sections of the contract and key terms to include. "
            "Identify any missing information that needs placeholders. "
            "If improving/reviewing, highlight areas that need change."
        )
        chain = prompt | self.llm | StrOutputParser()
        # Find plan message
        plan_msg = next((m for m in state.messages if m.get("node") == "research_plan"), {})
        
        brief = chain.invoke({
            "plan": plan_msg.get("content", ""), 
            "structure": state.contract_structure,
            "market_terms": state.market_terms,
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
