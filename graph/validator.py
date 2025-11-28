from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from .state import ContractState
from presidio_analyzer import AnalyzerEngine

class Validator:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0)
        self.analyzer = AnalyzerEngine()

    def run(self, state: ContractState) -> ContractState:
        print("--- Validator Started ---")
        
        # 1. PII Scan
        self._pii_scan(state)
        
        # 2. Enforceability/Risk Scan
        self._enforceability_scan(state)
        
        # 3. Payment Check
        self._payment_check(state)
        
        # 4. IP Ownership Check
        self._ip_ownership_check(state)
        
        # 5. Readability Score
        self._readability_score(state)
        
        # 6. Consistency Check
        self._consistency_check(state)
        
        # Append completion message
        state.messages.append({"node": "validator", "status": "done", "info": "Validator run completed"})
        
        return state

    def _pii_scan(self, state: ContractState):
        print("--- Validator: Scanning for PII ---")
        text = state.draft_content or ""
        results = self.analyzer.analyze(text=text, entities=["PERSON", "PHONE_NUMBER", "EMAIL_ADDRESS"], language='en')
        
        pii_found = [res.entity_type for res in results]
        state.validation_report["pii_scan"] = "fail" if pii_found else "pass"
        state.validation_report["pii_details"] = f"Found: {pii_found}" if pii_found else "No PII found"

    def _enforceability_scan(self, state: ContractState):
        print("--- Validator: Checking Enforceability ---")
        prompt = ChatPromptTemplate.from_template(
            "Review this contract text for enforceability risks: {text}. "
            "Return 'Pass' or a list of risks."
        )
        chain = prompt | self.llm | StrOutputParser()
        result = chain.invoke({"text": (state.draft_content or "")[:5000]})
        
        state.validation_report["enforceability"] = "pass" if "Pass" in result else "warning"
        state.validation_report["enforceability_details"] = result

    def _payment_check(self, state: ContractState):
        print("--- Validator: Checking Payment Terms ---")
        prompt = ChatPromptTemplate.from_template(
            "Check if this contract contains clear payment terms (amount, schedule, currency): {text}. "
            "Return 'Pass' or 'Fail' with reason."
        )
        chain = prompt | self.llm | StrOutputParser()
        result = chain.invoke({"text": (state.draft_content or "")[:5000]})
        
        state.validation_report["payment_check"] = "pass" if "Pass" in result else "fail"
        state.validation_report["payment_details"] = result

    def _ip_ownership_check(self, state: ContractState):
        print("--- Validator: Checking IP Ownership ---")
        prompt = ChatPromptTemplate.from_template(
            "Check if this contract clearly defines Intellectual Property ownership: {text}. "
            "Return 'Pass' or 'Fail' with reason."
        )
        chain = prompt | self.llm | StrOutputParser()
        result = chain.invoke({"text": (state.draft_content or "")[:5000]})
        
        state.validation_report["ip_ownership"] = "pass" if "Pass" in result else "fail"
        state.validation_report["ip_details"] = result

    def _readability_score(self, state: ContractState):
        print("--- Validator: Scoring Readability ---")
        text = state.draft_content or ""
        words = text.split()
        avg_len = sum(len(w) for w in words) / len(words) if words else 0
        
        state.validation_report["readability_score"] = round(avg_len, 2)
        state.validation_report["readability_details"] = f"Average word length: {round(avg_len, 2)}"

    def _consistency_check(self, state: ContractState):
        print("--- Validator: Checking Consistency ---")
        prompt = ChatPromptTemplate.from_template(
            "Check for contradictions in this contract: {text}. "
            "Return 'Pass' or list of contradictions."
        )
        chain = prompt | self.llm | StrOutputParser()
        result = chain.invoke({"text": (state.draft_content or "")[:5000]})
        
        state.validation_report["consistency"] = "pass" if "Pass" in result else "warning"
        state.validation_report["consistency_details"] = result

if __name__ == "__main__":
    print("VALIDATOR READY")
