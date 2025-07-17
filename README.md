# Nordic Drone Guard Detection Core

Passive radio frequency drone detection written in Python.  
Transforms affordable software defined radios into a privacy friendly early warning system for unauthorised drones.

***

## Table of contents

1. Vision  
2. Core features  
3. System architecture diagram  
4. Hardware specifications  
5. Installation guide  
6. Daily operation  
7. Folder map  
8. Development workflow  
9. Legal compliance notes  
10. Business models and pricing  
11. Roadmap  
12. Frequently asked questions  
13. Contributing guidelines  
14. License  
15. Contact information

***

## 1. Vision

Nordic Drone Guard aims to protect critical outdoor spaces without cameras, without jamming, and without heavy compute.  
The Detection Core runs on a single board computer and listens for drone control links.  
Small and mid‑sized customers gain professional airspace awareness at a fraction of legacy system cost.

***

## 2. Core features

* Fully passive scanning in the two point four to two point five giga hertz band  
* One hundred predefined drone patterns stored in JSON  
* Fast Fourier Transform for peak energy detection  
* Confidence scoring that filters noisy environments  
* Adaptive logging of unknown signals for future learning  
* Plugin notifier writes to log file, JSON feed, or web socket  
* Optional DJI Drone ID decoder if hardware supports wider bandwidth  
* Apache two license encourages forks and external audits

***

## 3. System architecture

```text
        IQ samples
Software Defined Radio  →  FFT and peak finder  →  Pattern matcher  →  Notifier
                                                          ↑
                                                          |
                                            Unknown signal logger

