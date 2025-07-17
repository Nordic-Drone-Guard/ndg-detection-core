# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2025 Nordic Drone Guard

from rtlsdr import RtlSdr
import numpy as np

class SDRInterface:
    def __init__(self):
        self.sdr = RtlSdr()
        self.sdr.sample_rate = 2.4e6
        self.sdr.center_freq = 2.45e9
        self.sdr.gain = 'auto'

    def capture_signals(self):
        samples = self.sdr.read_samples(256 * 1024)
        power = np.abs(np.fft.fft(samples))**2
        peak = np.argmax(power)
        freq_bin = self.sdr.center_freq - (self.sdr.sample_rate / 2) + (peak * self.sdr.sample_rate / len(samples))
        return [{
            "freq": round(freq_bin / 1e6, 2),
            "rssi": int(np.max(power)),
            "burst_pattern": "unknown",  # to be improved
            "duration_ms": 500
        }]
