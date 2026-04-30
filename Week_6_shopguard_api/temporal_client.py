# temporal_client.py
import asyncio
from temporalio.client import Client
from workflows import OrderFollowUpWorkflow

class TemporalClient:
    def __init__(self, server_address: str = "localhost:7233"):
        self.server_address = server_address
        self.client = None

    async def trigger_order_followup(self, order_id: str, customer_id: str):
        """Trigger long-running order follow-up workflow"""
        if not self.client:
            self.client = await Client.connect(self.server_address)

        workflow_id = f"order-followup-{order_id}-{int(asyncio.get_event_loop().time())}"

        handle = await self.client.start_workflow(
            OrderFollowUpWorkflow.run,
            args=[order_id, customer_id],
            id=workflow_id,
            task_queue="shopguard-task-queue",
        )

        print(f"🚀 Temporal Workflow triggered: {workflow_id}")
        
        return {
            "workflow_id": workflow_id,
            "status": "started",
            "message": f"I have started the long-term follow-up process for order {order_id}. I will continue to track and notify you in the coming days."
        }