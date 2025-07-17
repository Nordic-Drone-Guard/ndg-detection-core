# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2025 Nordic Drone Guard

import json
import datetime
import os

class SignalMatcher:
    def __init__(self, config):
        self.config = config
        self.patterns = self.load_patterns("signal_patterns/patterns.json")
        self.unmatched_log = "unrecognized_signals.json"

    def load_patterns(self, path):
        if os.path.exists(path):
            with open(path, "r") as f:
                return json.load(f)
        else:
            return []

    def match(self, signal):
        best_match = None
        highest_score = 0

        for pattern in self.patterns:
            score = 0

            # Frequency match
            if pattern["freq_band"][0] <= signal["freq"] <= pattern["freq_band"][1]:
                score += 0.4

            # Burst pattern match
            if signal["burst_pattern"] == pattern["burst_pattern"]:
                score += 0.3

            # RSSI threshold
            if signal["rssi"] >= pattern["rssi_min"]:
                score += 0.3

            if score > highest_score and score >= 0.6:
                highest_score = score
                best_match = pattern

        if best_match:
            best_match["match_confidence"] = round(highest_score, 2)
            return best_match
        else:
            self.log_unrecognized(signal)
            return None

    def log_unrecognized(self, signal):
        record = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "freq": signal["freq"],
            "rssi": signal["rssi"],
            "burst_pattern": signal["burst_pattern"],
            "duration_ms": signal["duration_ms"]
        }

        with open(self.unmatched_log, "a") as f:
            f.write(json.dumps(record) + "\n")

        print("[NDG] Unrecognized drone-like signal logged.")
