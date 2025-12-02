import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.template_store import TemplateStore

def load_templates():
    print("Loading templates...")
    store = TemplateStore()
    clauses_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "clauses")
    if not os.path.exists(clauses_dir):
        print(f"Error: {clauses_dir} does not exist.")
        return
        
    store.load_clauses(clauses_dir)
    print("Templates loaded.")

if __name__ == "__main__":
    load_templates()
