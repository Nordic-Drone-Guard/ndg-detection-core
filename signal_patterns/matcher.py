class SignalMatcher:
    def __init__(self, config):
        self.config = config
        self.patterns = [
            {
                "drone": "DJI Phantom 4",
                "freq_band": (2405, 2475),
                "burst_pattern": "100Hz",
                "rssi_min": 35
            },
            {
                "drone": "Autel Evo II",
                "freq_band": (2410, 2460),
                "burst_pattern": "200Hz",
                "rssi_min": 30
            }
        ]

    def match(self, signal):
        for pattern in self.patterns:
            if pattern["freq_band"][0] <= signal["freq"] <= pattern["freq_band"][1] and \
               signal["burst_pattern"] == pattern["burst_pattern"] and \
               signal["rssi"] >= max(pattern["rssi_min"], self.config["min_rssi_threshold"]):
                return pattern
        return None
