# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2025 Nordic Drone Guard

from __future__ import annotations

import logging
from typing import Dict, List

import numpy as np
from rtlsdr import RtlSdr, librtlsdr  # type: ignore

from utils.config_loader import load_config


class SDRInterface:
    """
    Wraps an RTL‑SDR dongle and returns peak detections as dictionaries
    compatible with SignalMatcher.  All parameters are read from the
    same JSON config file used by the scanner loop.
    """

    def __init__(self, cfg_path: str | None = None) -> None:
        cfg: Dict = load_config(cfg_path)
        self.sample_rate: float = cfg.get("sample_rate", 2.4e6)
        self.gain: str | int = cfg.get("gain", "auto")
        self.peak_threshold_db: float = cfg.get("peak_threshold_db", 30.0)
        self.chunk_samples: int = cfg.get("chunk_samples", 256 * 1024)
        self.bands: List[float] = cfg.get(
            "scan_bands_mhz", [2400.0, 2425.0, 2450.0, 2475.0]
        )  # centre frequencies in MHz

        # Initialise hardware
        try:
            self.sdr: RtlSdr = RtlSdr()
        except librtlsdr.LibUSBError as exc:
            raise RuntimeError("RTL‑SDR not found or busy") from exc

        self.sdr.sample_rate = self.sample_rate
        if self.gain == "auto":
            self.sdr.gain = "auto"
        else:
            self.sdr.gain = float(self.gain)

        logging.info(
            "SDR ready. sample_rate %.1f MHz gain %s dB  peaks over %s dB will be returned",
            self.sample_rate / 1e6,
            self.sdr.gain,
            self.peak_threshold_db,
        )

    async def capture_signals(self) -> List[Dict]:
        """
        Sweep every configured band once and return a list
        of peak detections that exceed the power threshold.
        """
        detections: List[Dict] = []

        for centre_mhz in self.bands:
            self.sdr.center_freq = centre_mhz * 1e6

            try:
                samples = self.sdr.read_samples(self.chunk_samples)
            except Exception as exc:  # pragma: no cover
                logging.exception("SDR read error at %.1f MHz: %s", centre_mhz, exc)
                continue

            # FFT and convert to power in dB
            power = 20 * np.log10(np.abs(np.fft.rfft(samples)))
            max_db = power.max()
            if max_db < self.peak_threshold_db:
                continue  # nothing strong enough in this chunk

            peak_idx = np.argmax(power)
            bins = power.shape[0]
            bin_width_hz = self.sample_rate / 2 / bins
            peak_freq_hz = (
                self.sdr.center_freq - self.sample_rate / 4 + peak_idx * bin_width_hz
            )

            detection = {
                "freq": round(peak_freq_hz / 1e6, 2),  # MHz
                "rssi": int(max_db),
                "burst_pattern": "unknown",
                "duration_ms": 500,
            }
            detections.append(detection)

        return detections

    # Optional helper for graceful shutdown
    def close(self) -> None:
        try:
            self.sdr.close()
        except Exception:
            pass
