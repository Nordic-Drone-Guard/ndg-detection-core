# Nordic Drone Guard – Detection Core

**Passive RF-based drone detection system**  
Developed by [Nordic Drone Guard](https://ndguard.com) – protecting airspace for farms, construction sites, events, and municipalities.

---

## 🛰️ What is NDG Detection Core?

NDG Detection Core is the software component behind **Nordic Drone Guard**, a modular system that uses **passive radio frequency (RF) scanning** to detect unauthorized drones in real-time — without jamming, radar, or cameras.

It’s designed to be:
- **Stealthy**: fully passive, legal in the EU/Norway
- **Affordable**: built for small/medium clients
- **Customizable**: modular hardware + software
- **Portable**: can run on embedded Linux, Raspberry Pi, or other SBCs

---

## 🔧 How It Works

The system listens for known drone RF signatures (typically 2.4GHz and 5.8GHz control signals) and matches them using internal pattern recognition logic.

Key functions:
- Detect drone presence based on RF traffic patterns
- Estimate signal strength and distance
- Identify probable drone types (Pro/Extreme models)
- Send alerts to connected app or dashboard

---

## 🧱 Core Modules

| Module | Description |
|--------|-------------|
| `rf_scanner/` | Low-level scanner that monitors RF spectrum |
| `signal_patterns/` | Database of known drone control signal types |
| `notifier/` | Alert system (email, log, webhook, or UI integration) |
| `simulator/` | Tool to simulate drone signals for testing |

> 💡 All modules are under development. Contributions are welcome once public alpha is released.

---

## 📦 Hardware Compatibility

Supports passive SDR receivers like:
- **RTL-SDR**
- **HackRF One**
- **ADALM-Pluto**
- **LimeSDR Mini**

Runs on:
- Raspberry Pi 4 / 5
- Jetson Nano
- x86_64 Linux (for desktop testing)

---

## 🔐 Legal Compliance

Nordic Drone Guard is designed to comply with:
- **Norwegian Post and Telecommunications Authority (Nkom)**
- **EU RF spectrum regulations**
- **GDPR** (no camera/audio collection)
- **No jamming or offensive components**

Always check local laws before deployment.

---

## 📈 Roadmap

- [x] Project structure and repo setup
- [ ] Signal pattern database (basic models)
- [ ] SDR live monitoring module
- [ ] Desktop + mobile notifier system
- [ ] Alpha field test on prototype device
- [ ] GitHub Actions for build/test

---

## 🧪 Demo & Testing

Demo hardware is in development.  
We are looking for **early testers, demo partners, and feedback**.  
Contact: [info@ndguard.com](mailto:info@ndguard.com)

---

## 📄 License

Licensed under the **Apache 2.0 License** – see [LICENSE](LICENSE) for full details.

---

## 👨‍💼 About the Project

**Nordic Drone Guard** is a Norwegian startup (ENK org nr 935579945) focused on building privacy-friendly, legal, and cost-effective drone detection systems for everyday use.

Visit [ndguard.com](https://ndguard.com) for more details or follow us on LinkedIn.

---

