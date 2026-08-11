"""Write-capable tools. In production these hit Stripe / the email provider —
real side effects with real money. AgentReplay blocks these during replay."""


def refund_customer(customer_id: str, amount_cents: int, approval_id: str | None = None) -> dict:
    # Real implementation would call the payment provider here.
    return {"refunded": True, "customer_id": customer_id, "amount_cents": amount_cents}


def send_email(to: str, template: str) -> dict:
    return {"sent": True, "to": to, "template": template}


# Read-only order store. In production this queries the orders database.
_ORDERS = {
    "ord_9001": {
        "order_id": "ord_9001", "customer_id": "cus_demo",
        "email": "demo@acme.test", "shipping_address": "500 Market St, San Francisco, CA",
        "items": ["USB-C cable"], "total_cents": 1900, "state": "delivered",
    },
    "ord_9002": {
        "order_id": "ord_9002", "customer_id": "cus_victim",
        "email": "jordan.lee@example.com", "shipping_address": "221B Baker Street, London",
        "items": ["Noise-cancelling headphones"], "total_cents": 34900, "state": "shipped",
    },
}


def fetch_order(order_id: str | None) -> dict | None:
    return _ORDERS.get(order_id)
