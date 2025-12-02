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

        # 5. Text Exporter
        self._text_exporter(state)
        
        return state

    def _text_exporter(self, state: ContractState):
        print("--- Admin: Checking for Text Export ---")
        # Find the last user message
        last_user_msg = next((m.get("content", "") for m in reversed(state.messages) if m.get("role") == "user"), "").lower()
        
        # Check if user asked for text file
        if any(keyword in last_user_msg for keyword in ["txt", "text file", ".txt", "plain text"]):
            print("--- Admin: Exporting to .txt ---")
            import os
            data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
            os.makedirs(data_dir, exist_ok=True)
            
            # Generate unique filename
            base_name = "contract"
            extension = ".txt"
            counter = 1
            while True:
                filename = f"{base_name}_v{counter}{extension}" if counter > 1 else f"{base_name}{extension}"
                filepath = os.path.join(data_dir, filename)
                if not os.path.exists(filepath):
                    break
                counter += 1
            
            content = state.draft_content or "No contract content available."
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
                
            state.messages.append({
                "node": "text_exporter",
                "status": "done",
                "info": f"Text file generated at {filepath}"
            })

    def _deadline_extractor(self, state: ContractState):
        print("--- Admin: Extracting Deadlines ---")
        prompt = ChatPromptTemplate.from_template(
            "Extract all deadlines and dates from this contract text: {text}. "
            "Return a JSON list of objects with 'date' (YYYY-MM-DD) and 'description'. "
            "Example: [{{\"date\": \"2023-12-31\", \"description\": \"Project Completion\"}}]"
        )
        chain = prompt | self.llm | StrOutputParser()
        
        text = state.draft_content or (state.messages[0].get("content", "") if state.messages else "")
        try:
            deadlines_json = chain.invoke({"text": text[:5000]})
            # Clean up potential markdown code blocks
            deadlines_json = deadlines_json.replace("```json", "").replace("```", "").strip()
            import json
            deadlines = json.loads(deadlines_json)
        except Exception as e:
            print(f"Error parsing deadlines: {e}")
            deadlines = []
        
        state.extracted_facts["deadlines"] = deadlines
        state.messages.append({
            "node": "deadline_extractor",
            "status": "done",
            "deadlines": deadlines
        })

    def _scheduler_generator(self, state: ContractState):
        print("--- Admin: Generating Scheduler ---")
        deadlines = state.extracted_facts.get("deadlines", [])
        
        if not deadlines:
            info = "No deadlines found to schedule."
        else:
            # Generate ICS content manually
            ics_content = "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Lexis//ContractDeadlines//EN\n"
            for item in deadlines:
                date_str = item.get("date", "").replace("-", "")
                desc = item.get("description", "Contract Deadline")
                if len(date_str) == 8: # YYYYMMDD
                    ics_content += "BEGIN:VEVENT\n"
                    ics_content += f"DTSTART;VALUE=DATE:{date_str}\n"
                    ics_content += f"SUMMARY:{desc}\n"
                    ics_content += "END:VEVENT\n"
            ics_content += "END:VCALENDAR"
            
            # Save to file
            import os
            data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
            os.makedirs(data_dir, exist_ok=True)
            filepath = os.path.join(data_dir, "contract_deadlines.ics")
            with open(filepath, "w") as f:
                f.write(ics_content)
            
            info = f"ICS file generated at {filepath}"

        state.messages.append({
            "node": "scheduler_generator",
            "status": "done",
            "info": info
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
