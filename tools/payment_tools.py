from typing import Dict, List

def generate_invoice(amount: float, currency: str = "USD") -> Dict[str, str]:
    print(f"Generated invoice for {amount} {currency} (Placeholder)")
    return {
        "invoice_id": "inv_123",
        "amount": str(amount),
        "currency": currency,
        "status": "draft"
    }

def generate_payment_schedule(total_amount: float, milestones: List[str]) -> Dict[str, str]:
    print(f"Generated payment schedule for {total_amount} with milestones {milestones} (Placeholder)")
    return {
        "schedule_id": "sched_123",
        "total_amount": str(total_amount),
        "milestones": milestones
    }

if __name__ == "__main__":
    generate_invoice(1000)
    generate_payment_schedule(5000, ["Start", "Mid", "End"])
