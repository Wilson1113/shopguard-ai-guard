import asyncio
from temporalio.client import Client
from temporalio.worker import Worker, UnsandboxedWorkflowRunner
from workflows import OrderFollowUpWorkflow
from activities import check_order_status_activity, notify_customer_activity
import uuid

async def main():
    client = await Client.connect("localhost:7233")

    # Start Worker with UnsandboxedWorkflowRunner to fix beartype/fastmcp conflicts
    worker = Worker(
        client,
        task_queue="shopguard-task-queue",
        workflows=[OrderFollowUpWorkflow],
        activities=[check_order_status_activity, notify_customer_activity],
        workflow_runner=UnsandboxedWorkflowRunner(),
    )
    await worker.run()

    print("🚀 Temporal Worker started. Listening for workflows...")

    # workflow_id = f"order-followup-{uuid.uuid4().hex[:8]}"

    # handle = await client.start_workflow(
    #     OrderFollowUpWorkflow.run,
    #     args=["ORD-78492", "customer_001"],
    #     id=workflow_id,                    # ← 使用随机 ID
    #     task_queue="shopguard-task-queue",
    # )

    # print(f"Workflow started with ID: {handle.id}")

    # # Wait for Workflow completion
    # result = await handle.result()
    # print("Workflow completed with result:", result)

if __name__ == "__main__":
    asyncio.run(main())