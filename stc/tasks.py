import asyncio
from datetime import datetime
from django.utils.timezone import now, localtime
from asgiref.sync import sync_to_async  # Import sync_to_async
from stc.models import BusPass

async def delete_expired_passes_task():
    last_checked_date = localtime(now()).date()  # Track the last date when passes were checked

    while True:
        current_time = localtime(now())
        current_date = current_time.date()

        print(f"[{current_time}] Running delete_expired_passes_task...")

        # Check if the current date has advanced
        if current_date > last_checked_date:
            print("hello")
            # Use sync_to_async for ORM calls to make them async-compatible
            expired_passes = await sync_to_async(BusPass.objects.filter)(created_at__lt=current_date)
            expired_count = await sync_to_async(expired_passes.count)()
            await sync_to_async(expired_passes.delete)()

            print(f"[{current_time}] Deleted {expired_count} expired bus passes.")

            # Update the last checked date
            last_checked_date = current_date

        # Wait for 1 minute before checking again
        await asyncio.sleep(60)
