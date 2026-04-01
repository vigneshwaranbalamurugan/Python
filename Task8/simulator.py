import asyncio
import random
from datetime import datetime

async def simulator():
    while True:
        data = {
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "temperature": round(random.uniform(20, 40), 2),
            "vibration": round(random.uniform(1, 10), 2)
        }
        yield data
        await asyncio.sleep(1)