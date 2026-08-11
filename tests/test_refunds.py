from support_agent.refunds import is_eligible, process_refund


def test_ineligible_request_is_denied():
    calls = []
    result = process_refund(
        {"customer_id": "c1", "amount_cents": 500, "service_affected": False},
        lambda **kw: calls.append(kw) or {"refunded": True},
    )
    assert result["status"] == "denied"
    assert calls == []


def test_small_eligible_refund_is_issued():
    result = process_refund(
        {"customer_id": "c1", "amount_cents": 500, "service_affected": True},
        lambda **kw: {"refunded": True, **kw},
    )
    assert result["status"] == "refunded"


def test_eligibility_rules():
    assert is_eligible({"service_affected": True, "amount_cents": 100})
    assert not is_eligible({"service_affected": False, "amount_cents": 100})
