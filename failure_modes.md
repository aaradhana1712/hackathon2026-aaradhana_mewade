# Failure Mode Analysis - ShopWave Support Agent

This document outlines potential failure scenarios in the ShopWave Autonomous Support Agent and how the system is designed to handle them gracefully.

## 1. Tool Timeout (Network/Internal Failure)
**Scenario**: The `get_order` or `check_refund_eligibility` tool takes longer than the allowed threshold or returns a timeout error.
**System Response**:
- **Retry Logic**: The agent environment captures the `TimeoutError`.
- **Reasoning Loop**: The error is passed back to the LLM as a tool result. The LLM is instructed to retry the operation at least once or explain the delay to the customer.
- **Audit**: The timeout is logged in `audit_log.json` with a specific `error` level.

## 2. Malformed Tool Output (Hallucination/Schema Mismatch)
**Scenario**: A mock tool returns "INTERNAL_SERVER_ERROR" or a JSON string that isn't a valid dictionary.
**System Response**:
- **Validation**: Tool outputs are validated before being returned to the agent loop.
- **Recovery**: If the LLM receives an error message instead of the expected data, it uses its "reasoning" capability to decide if it should:
    - Try a different tool (e.g., look up by email instead of order ID).
    - Inform the customer about a temporary system glitch and escalate if critical.
- **Audit**: The malformed response is captured and flagged for developer review.

## 3. Ambiguous/Conflicting Customer Data (Social Engineering)
**Scenario**: A customer claims they are "VIP" and deserve an "instant refund," but `get_customer` returns tier `Standard`.
**System Response**:
- **Source of Truth**: The agent is strictly instructed to trust tool outputs over customer claims.
- **Policy Enforcement**: The knowledge base specifies that customer tiers are verified only via system lookup.
- **Conflict Handling**: The agent politely declines the request by citing the system-verified policy and flags the ticket for "Social Engineering" in the audit trail.
- **Escalation**: If the customer becomes aggressive or the threat level is high (angry sentiment), the agent escalates to a human with a summary of the discrepancy.

## 4. Reasoning Chain Depth Limit
**Scenario**: The agent gets stuck in a loop calling the same tool repeatedly without progress.
**System Response**:
- **Step Counter**: The `AgentState` includes a `steps` counter. 
- **Termination**: If the `steps` count exceeds a maximum threshold (e.g., 10), the agent automatically transitions to the `escalate` node to prevent infinite loops and resource consumption.
- **Audit**: The excessive step count is logged as a "Potential Loop" failure mode.
