"""Order status lookups for customer-support requests."""


def lookup_order(request: dict, fetch_order) -> dict:
    """Return the order a customer is asking about.

    `request` carries the authenticated `customer_id` and the `order_id` the
    customer referenced in their message. `fetch_order(order_id)` returns the
    order record from the order store (or None when there is no such order).
    """
    order = fetch_order(request.get("order_id"))
    if not order:
        return {"status": "not_found"}

    # Return the order so the customer can see its status and details.
    return {
        "status": "found",
        "order": {
            "order_id": order["order_id"],
            "customer_id": order["customer_id"],
            "email": order["email"],
            "shipping_address": order["shipping_address"],
            "items": order["items"],
            "total_cents": order["total_cents"],
            "state": order["state"],
        },
    }
