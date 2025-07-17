# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2025 Nordic Drone Guard

from __future__ import annotations

import json
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Callable, Dict, List, Optional

try:
    from colorama import Fore, Style, init as colorama_init
    colorama_init()  # enables ANSI colours on Windows
    COLOUR_OK = True
except ImportError:  # colour is optional
    COLOUR_OK = False


class AlertManager:
    """
    Writes alerts to JSON‑Lines log and optionally publishes
    to external callbacks, for example an MQTT broker.
    """

    def __init__(
        self,
        config: Dict,
        callbacks: Optional[List[Callable[[Dict], None]]] = None,
    ) -> None:
        # File path and rotation parameters from config
        self.alert_file: Path = Path(config.get("alert_output", "alerts.jsonl"))
        max_bytes: int = config.get("alert_max_bytes", 2_000_000)  # two MB
        backups: int = config.get("alert_backups", 3)

        self._handler = RotatingFileHandler(
            self.alert_file,
            maxBytes=max_bytes,
            backupCount=backups,
            encoding="utf‑8",
        )
        self._handler.setFormatter(
            logging.Formatter("%(message)s")  # raw JSON per line
        )
        self.logger = logging.getLogger("ndg.alerts")
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(self._handler)

        self.callbacks = callbacks or []

    # Public -------------------------------------------------------------

    def send(self, drone_info: Dict, signal: Dict) -> None:
        """Compose an alert payload and dispatch it."""
        payload = {
            "timestamp": datetime.utcnow().isoformat(timespec="seconds"),
            "drone": drone_info["drone"],
            "frequency_mhz": signal["freq"],
            "rssi_db": signal["rssi"],
            "pattern": signal.get("burst_pattern", "n/a"),
            "duration_ms": signal.get("duration_ms", 0),
            "confidence": drone_info.get("match_confidence", 1.0),
        }

        # Write to JSON‑lines log
        self.logger.info(json.dumps(payload, separators=(",", ":")))

        # Pretty console line
        self._print_console(payload)

        # Forward to any external callbacks
        for cb in self.callbacks:
            try:
                cb(payload)
            except Exception as exc:  # pragma: no cover
                logging.exception("Alert callback failed: %s", exc)

    # Private ------------------------------------------------------------

    def _print_console(self, p: Dict) -> None:
        text = (
            f"[{p['timestamp']}] ALERT   "
            f"{p['drone']}  {p['frequency_mhz']:.2f} MHz  "
            f"{p['rssi_db']} dB  "
            f"conf {p['confidence']:.2f}"
        )
        if COLOUR_OK:
            print(f"{Fore.CYAN}{text}{Style.RESET_ALL}")
        else:
            print(text)
