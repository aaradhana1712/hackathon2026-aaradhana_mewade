import asyncio
import json
import os
from dotenv import load_dotenv
from mocks.data_manager import DataManager
from mocks.tools import MockTools
from agent.core import ShopWaveAgent
from utils.audit import Auditor

async def process_ticket(agent, ticket, semaphore):
    # Use semaphore to limit concurrency if needed, but 20 tickets is fine
    async with semaphore:
        try:
            print(f"Starting processing for {ticket['ticket_id']}...")
            result = await agent.run(ticket)
            print(f"Finished processing for {ticket['ticket_id']}.")
            # Slow down to avoid "Resource Exhausted" error
            await asyncio.sleep(5)
            return result
        except Exception as e:
            print(f"Error processing {ticket['ticket_id']}: {e}")
            return None

async def main():
    load_dotenv()
    
    if not os.getenv("GOOGLE_API_KEY"):
        print("CRITICAL: GOOGLE_API_KEY not found in .env file.")
        return

    # Initialize components
    data_manager = DataManager("sample_data")
    tools = MockTools(data_manager)
    auditor = Auditor("audit_log.json")
    agent = ShopWaveAgent(tools, auditor)

    tickets = data_manager.tickets # Process all 20 tickets
    
    # Concurrency limit (Simulation mode is fast)
    semaphore = asyncio.Semaphore(10)
    
    tasks = [process_ticket(agent, ticket, semaphore) for ticket in tickets]
    
    print(f"Processing {len(tickets)} tickets using Simulated AI...")
    results = await asyncio.gather(*tasks)
    
    # Save the audit log
    auditor.save()
    print("\nProcessing complete. Audit log saved to audit_log.json.")

if __name__ == "__main__":
    asyncio.run(main())
