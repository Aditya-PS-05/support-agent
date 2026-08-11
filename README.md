# support-agent

A small AI customer-support agent. It reads an incoming customer message,
retrieves the relevant policy, uses an LLM to classify intent and extract
details, and then acts — answering questions or issuing refunds through
write-capable tools (`refund_customer`, `send_email`).

## Run

```python
from support_agent.agent import SupportAgent
agent = SupportAgent()
print(agent.handle("My annual plan was charged $900 but the service was down all week. Refund it."))
```

## Layout
- `support_agent/agent.py`    — orchestration (retrieve → classify → act)
- `support_agent/refunds.py`  — refund policy + processing
- `support_agent/tools.py`    — write-capable tools (payments, email)
- `support_agent/llm.py`      — thin LLM wrapper (offline-safe stub)
