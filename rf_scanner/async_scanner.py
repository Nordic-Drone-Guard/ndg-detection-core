import asyncio
import json
import logging
from rf_scanner.sdr_interface import SDRInterface
from signal_patterns.matcher import SignalMatcher
from notifier.alert import AlertManager
from utils.config_loader import load_config

class AsyncRFScanner:
    def __init__(self):
        self.config = load_config()
        self.sdr = SDRInterface()
        self.matcher = SignalMatcher(self.config)
        self.alerter = AlertManager(self.config)

    async def scan_loop(self):
        while True:
            signals = await self.sdr.capture_signals()
            for sig in signals:
                match = self.matcher.match(sig)
                if match:
                    self.alerter.send(match, sig)
            await asyncio.sleep(self.config["scan_interval_sec"])

if __name__ == "__main__":
    scanner = AsyncRFScanner()
    asyncio.run(scanner.scan_loop())
