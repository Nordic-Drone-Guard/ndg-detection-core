# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2025 Nordic Drone Guard

import argparse
import asyncio
import json
import logging
import signal
from pathlib import Path
from typing import List, Dict

from rf_scanner.sdr_interface import SDRInterface
from signal_patterns.matcher import SignalMatcher
from notifier.alert import AlertManager
from utils.config_loader import load_config


class AsyncRFScanner:
    """Main loop for passive drone detection."""

    def __init__(self, cfg_path: Path | None = None) -> None:
        self.config: Dict = load_config(cfg_path)  # type: ignore[arg-type]
        self.sdr: SDRInterface = SDRInterface()
        self.matcher: SignalMatcher = SignalMatcher(self.config)
        self.alerter: AlertManager = AlertManager(self.config)

        # metrics
        self.matches: int = 0
        self.unknown: int = 0

        # log level can be set in settings.json
        logging.basicConfig(
            filename=self.config.get("log_file", "ndg_advanced.log"),
            level=getattr(logging, self.config.get("log_level", "INFO").upper()),
            format="%(asctime)s | %(levelname)s | %(message)s",
        )

    async def scan_iteration(self) -> None:
        """One sweep, then update counters and send alerts."""
        try:
            signals: List[Dict] = await self.sdr.capture_signals()
        except Exception as exc:
            logging.exception("SDR capture failed: %s", exc)
            return

        for sig in signals:
            match = self.matcher.match(sig)
            if match:
                self.matches += 1
                self.alerter.send(match, sig)
            else:
                self.unknown += 1

    async def scan_loop(self) -> None:
        """Run until cancelled."""
        interval = self.config["scan_interval_sec"]
        logging.info("Scanner started with %.1f s interval", interval)
        try:
            while True:
                await self.scan_iteration()
                await asyncio.sleep(interval)
        except asyncio.CancelledError:
            logging.info("Scanner stopped. Matches %d, unknown %d", self.matches, self.unknown)
            raise


def _shutdown(loop: asyncio.AbstractEventLoop, task: asyncio.Task) -> None:
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.remove_signal_handler(sig)
    task.cancel()


def main() -> None:
    parser = argparse.ArgumentParser(description="NDGuard passive RF scanner")
    parser.add_argument("--config", "-c", type=Path, help="Path to settings.json")
    args = parser.parse_args()

    scanner = AsyncRFScanner(cfg_path=args.config)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    task = loop.create_task(scanner.scan_loop())

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, _shutdown, loop, task)

    try:
        loop.run_until_complete(task)
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()


if __name__ == "__main__":
    main()
