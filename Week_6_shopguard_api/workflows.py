from schemas import CustomerInput
from temporalio import workflow
from datetime import timedelta
from activities import check_order_status_activity, notify_customer_activity

@workflow.defn
class OrderFollowUpWorkflow:

    @workflow.run
    async def run(self, order_id: str, customer_id: str):
        print(f"Starting long-running workflow for order {order_id}")

        # Step 1: Check order status
        status = await workflow.execute_activity(
            check_order_status_activity,
            order_id,
            start_to_close_timeout=timedelta(seconds=30)
        )

        # Step 2: Wait for some time
        # CRITICAL: In Temporal workflows, you must use workflow.sleep() 
        # instead of asyncio.sleep() to maintain determinism.
        await workflow.sleep(5)

        # Step 3: Send follow-up notification
        notification = await workflow.execute_activity(
            notify_customer_activity,
            CustomerInput(customer_id=customer_id, message=f"Your order {order_id} is still in transit. Do you need assistance?"),
            start_to_close_timeout=timedelta(seconds=30)
        )

        return {
            "order_id": order_id,
            "final_status": status,
            "notification": notification
        }