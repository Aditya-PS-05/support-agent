"""Refund policy and processing."""

# Refunds at or above this amount require an explicit manager approval_id.
REFUND_APPROVAL_THRESHOLD_CENTS = 100_00


def is_eligible(request: dict) -> bool:
    return bool(request.get("service_affected")) and request.get("amount_cents", 0) > 0


def process_refund(request: dict, refund_tool) -> dict:
    """Process a refund request for an eligible customer.

    Policy: refunds at or above REFUND_APPROVAL_THRESHOLD_CENTS must carry a
    manager approval_id; smaller refunds may be issued automatically.
    """
    if not is_eligible(request):
        return {"status": "denied", "reason": "not eligible"}

    amount = request["amount_cents"]
    # Require explicit approval for high-value refunds.
    if amount >= REFUND_APPROVAL_THRESHOLD_CENTS and not request.get("approval_id"):
        return {"status": "denied", "reason": "approval required"}

    # NOTE: high-value refunds are issued straight away.
    return {
        "status": "refunded",
        "result": refund_tool(
            customer_id=request["customer_id"],
            amount_cents=amount,
            approval_id=request.get("approval_id"),
        ),
    }
