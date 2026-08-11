"""Thin LLM wrapper. Falls back to a deterministic stub when offline so the
agent (and its tests) run without network access or credentials."""
import json
import os


def classify(message: str) -> dict:
    """Return {"intent": "refund"|"question", "amount_cents": int, "approval_id": str|None}."""
    key = os.environ.get("OPENAI_API_KEY")
    if key:
        try:
            import urllib.request
            body = json.dumps({
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "Extract JSON {intent, amount_cents, approval_id}."},
                    {"role": "user", "content": message},
                ],
                "response_format": {"type": "json_object"},
            }).encode()
            req = urllib.request.Request(
                "https://api.openai.com/v1/chat/completions",
                data=body,
                headers={"authorization": f"Bearer {key}", "content-type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=20) as r:
                return json.loads(json.load(r)["choices"][0]["message"]["content"])
        except Exception:
            pass
    # offline stub: naive extraction
    intent = "refund" if "refund" in message.lower() else "question"
    amount = 0
    for token in message.replace("$", " ").split():
        digits = token.replace(",", "").replace(".", "")
        if digits.isdigit():
            amount = int(digits) * 100
            break
    return {"intent": intent, "amount_cents": amount, "approval_id": None}
