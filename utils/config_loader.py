# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2025 Nordic Drone Guard

import json

def load_config(path="config/settings.json"):
    with open(path, "r") as f:
        return json.load(f)
