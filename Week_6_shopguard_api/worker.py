import asyncio
from temporalio.client import Client
from temporalio.worker import Worker, UnsandboxedWorkflowRunner
from workflows import OrderFollowUpWorkflow
from activities import check_order_status_activity, notify_customer_activity

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

    print("🚀 Temporal Worker started. Listening for workflows...")

    await worker.run()

    

if __name__ == "__main__":
    asyncio.run(main())