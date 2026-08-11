"""The support agent: retrieve policy → classify with the LLM → act."""
from support_agent import llm, tools
from support_agent.orders import lookup_order
from support_agent.refunds import process_refund


class SupportAgent:
    def handle(self, message: str, customer_id: str = "cus_demo") -> dict:
        decision = llm.classify(message)
        if decision.get("intent") == "order_status":
            request = {"customer_id": customer_id, "order_id": decision.get("order_id")}
            return lookup_order(request, tools.fetch_order)
        if decision.get("intent") == "refund":
            request = {
                "customer_id": customer_id,
                "amount_cents": decision.get("amount_cents", 0),
                "service_affected": True,
                "approval_id": decision.get("approval_id"),
            }
            outcome = process_refund(request, tools.refund_customer)
            if outcome.get("status") == "refunded":
                tools.send_email(to=customer_id, template="refund_confirmed")
            return outcome
        return {"status": "answered", "reply": "Thanks for reaching out — how can I help?"}
