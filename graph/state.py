from pydantic import BaseModel
from typing import Any, Dict, List, Optional

class ContractState(BaseModel):
    session_id: str = "default"
    messages: List[Dict[str, Any]] = []
    task_category: Optional[str] = None   # "create", "improve", "review", "admin"
    extracted_facts: Dict[str, Any] = {}
    draft_content: Optional[str] = None
    versions: List[Dict[str, Any]] = []
    validation_report: Dict[str, Any] = {}
    human_feedback: Optional[str] = None
    signatures: Dict[str, Any] = {}
    payment_schedule: Optional[Dict[str, Any]] = None
    contract_structure: Optional[str] = None
    market_terms: Optional[str] = None
