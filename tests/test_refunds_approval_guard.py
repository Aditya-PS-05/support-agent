from unittest.mock import Mock

from support_agent import refunds


def test_high_value_refund_without_approval_is_denied_and_tool_not_called():
    request = {
        "service_affected": True,
        "amount_cents": refunds.REFUND_APPROVAL_THRESHOLD_CENTS,  # at threshold
        "customer_id": "cust_123",
        # no approval_id provided
    }
    refund_tool = Mock(return_value={"ok": True})

    result = refunds.process_refund(request, refund_tool)

    assert result["status"] == "denied"
    refund_tool.assert_not_called()
