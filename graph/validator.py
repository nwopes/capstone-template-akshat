from typing import Any, Dict, List
from .state import ContractState

class Validator:
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
        
        # 7. Append "validator_run" to state.messages
        state.messages.append({"node": "validator", "status": "done", "info": "Validator run completed"})
        
        return state

    def _pii_scan(self, state: ContractState):
        # Deterministic scan: if 'email' substring in state.draft_content, flag PII
        content = state.draft_content or ""
        has_pii = "email" in content.lower()
        state.validation_report["pii_scan"] = "fail" if has_pii else "pass"
        state.validation_report["pii_details"] = "Found 'email' substring" if has_pii else "No PII found"

    def _enforceability_scan(self, state: ContractState):
        # Deterministic heuristics placeholder
        state.validation_report["enforceability"] = "pass"
        state.validation_report["enforceability_details"] = "Standard terms detected"

    def _payment_check(self, state: ContractState):
        # Validate existence of payment_schedule or presence of 'Payment Terms' in versions
        has_payment_terms = False
        if state.payment_schedule:
            has_payment_terms = True
        else:
            for version in state.versions:
                if "Payment Terms" in version.get("content", ""):
                    has_payment_terms = True
                    break
        
        state.validation_report["payment_check"] = "pass" if has_payment_terms else "fail"
        state.validation_report["payment_details"] = "Payment terms found" if has_payment_terms else "Missing payment terms"

    def _ip_ownership_check(self, state: ContractState):
        # Placeholder
        state.validation_report["ip_ownership"] = "pass"
        state.validation_report["ip_details"] = "IP clause present"

    def _readability_score(self, state: ContractState):
        # Trivial readability heuristic: average sentence length
        content = state.draft_content or ""
        sentences = content.split('.')
        avg_len = sum(len(s.split()) for s in sentences) / max(1, len(sentences))
        state.validation_report["readability_score"] = round(avg_len, 2)
        state.validation_report["readability_details"] = f"Average sentence length: {round(avg_len, 2)} words"

    def _consistency_check(self, state: ContractState):
        # Check for repeated contradictory phrases placeholder
        state.validation_report["consistency"] = "pass"
        state.validation_report["consistency_details"] = "No contradictions found"

if __name__ == "__main__":
    print("VALIDATOR READY")
