"""Write-capable tools. In production these hit Stripe / the email provider —
real side effects with real money. AgentReplay blocks these during replay."""


def refund_customer(customer_id: str, amount_cents: int, approval_id: str | None = None) -> dict:
    # Real implementation would call the payment provider here.
    return {"refunded": True, "customer_id": customer_id, "amount_cents": amount_cents}


def send_email(to: str, template: str) -> dict:
    return {"sent": True, "to": to, "template": template}
