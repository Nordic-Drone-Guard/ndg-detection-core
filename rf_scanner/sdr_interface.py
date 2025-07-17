import asyncio
import random

class SDRInterface:
    def __init__(self):
        self.freq_range = (2400, 2500)

    async def capture_signals(self):
        await asyncio.sleep(0.1)
        return [{
            "freq": round(random.uniform(*self.freq_range), 2),
            "rssi": random.randint(10, 90),
            "burst_pattern": random.choice(["100Hz", "200Hz", "static"]),
            "duration_ms": random.randint(300, 2500)
        } for _ in range(random.randint(1, 4))]
