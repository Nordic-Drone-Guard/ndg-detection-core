# Nordic Drone Guard Detection Core

Passive Radio Frequency drone detection written in Python.  
Runs on Raspberry Pi, Jetson Nano, or any Linux host with an attached software defined radio.

***

## 1. What this project delivers

* Real time RF capture through RTL SDR or similar hardware  
* Fast Fourier Transform analysis for energy peaks in two point four to two point five giga hertz  
* Signature matcher with confidence score based on one hundred drone patterns  
* Logging of unrecognised signals for later analysis  
* Pluggable notifier that writes alerts to file, JSON feed, or web socket  
* Apache two license so anyone can audit or extend the code

***

## 2. Quick start

```bash
git clone https://github.com/Nordic-Drone-Guard/ndg-detection-core.git
cd ndg-detection-core
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m ndg.rfscanner.async_scanner
