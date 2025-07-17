import json
import datetime

class AlertManager:
    def __init__(self, config):
        self.alert_file = config["alert_output"]

    def send(self, drone_info, signal):
        alert_data = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "drone": drone_info["drone"],
            "frequency": signal["freq"],
            "rssi": signal["rssi"],
            "pattern": signal["burst_pattern"],
            "duration": signal["duration_ms"]
        }
        with open(self.alert_file, "a") as f:
            f.write(json.dumps(alert_data) + "\n")
        print(f"[ALERT] {alert_data['drone']} detected at {alert_data['frequency']} MHz")
