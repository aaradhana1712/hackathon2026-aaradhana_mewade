import random
import asyncio
from typing import Optional, Dict, Any
from .data_manager import DataManager

class MockTools:
    def __init__(self, data_manager: DataManager):
        self.dm = data_manager

    async def _simulate_failure(self):
        # 10% chance of timeout, 5% chance of malformed data/error
        r = random.random()
        if r < 0.10:
            await asyncio.sleep(2) # Timeout simulation
            raise TimeoutError("Tool call timed out")
        elif r < 0.15:
            return "INTERNAL_SERVER_ERROR" # Malformed response simulation

    async def get_order(self, order_id: str) -> Dict[str, Any]:
        await asyncio.sleep(0.5)
        fail = await self._simulate_failure()
        if fail: return fail
        
        order = self.dm.get_order(order_id)
        if not order:
            return {"error": "Order not found"}
        return order

    async def check_refund_eligibility(self, order_id: str) -> Dict[str, Any]:
        await asyncio.sleep(0.8)
        fail = await self._simulate_failure()
        if fail: return fail

        order = self.dm.get_order(order_id)
        if not order:
            return {"error": "Order not found for eligibility check"}
        
        # Simple logic based on status and dates
        # Real eligibility check would look at the product category and delivery date
        # For mock purposes, we'll return something useful
        if order["status"] == "delivered":
            # Check 30 day window (mocked as simple true/false for demo)
            return {"eligible": True, "reason": "Within return window"}
        elif order["status"] == "cancelled":
             return {"eligible": False, "reason": "Order already cancelled"}
        else:
            return {"eligible": False, "reason": f"Order status is {order['status']}"}

    async def get_customer(self, email: str) -> Dict[str, Any]:
        await asyncio.sleep(0.3)
        fail = await self._simulate_failure()
        if fail: return fail

        customer = self.dm.get_customer(email)
        if not customer:
            return {"error": "Customer not found"}
        return customer

    async def issue_refund(self, order_id: str, amount: float) -> Dict[str, Any]:
        await asyncio.sleep(1.0)
        fail = await self._simulate_failure()
        if fail: return fail

        order = self.dm.get_order(order_id)
        if not order:
             return {"error": "Order not found for refund"}
        
        return {"status": "success", "refund_id": f"REF-{random.randint(1000, 9999)}", "amount": amount}

    async def get_product(self, product_id: str) -> Dict[str, Any]:
        await asyncio.sleep(0.4)
        fail = await self._simulate_failure()
        if fail: return fail

        product = self.dm.get_product(product_id)
        if not product:
            return {"error": "Product not found"}
        return product

    async def send_reply(self, ticket_id: str, message: str) -> Dict[str, Any]:
        await asyncio.sleep(0.5)
        # This one rarely fails as it's the final step
        return {"status": "sent", "ticket_id": ticket_id}

    async def search_knowledge_base(self, query: str) -> str:
        await asyncio.sleep(0.7)
        # Mocking semantic search by just returning the relevant sections (simplification)
        # In a real app this would use a vector DB
        return self.dm.knowledge_base[:2000] # Return first 2000 chars for now

    async def escalate(self, ticket_id: str, summary: str, priority: str) -> Dict[str, Any]:
        await asyncio.sleep(0.6)
        return {"status": "escalated", "ticket_id": ticket_id, "priority": priority}
