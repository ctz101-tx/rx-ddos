# RX-DDoS Ultimate v5.0

<div align="center">

![rx-ddos.jpg](rx-ddos.jpg)

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)]()
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey?style=for-the-badge)]()
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)]()
[![Version](https://img.shields.io/badge/Version-5.0--Ultimate-orange?style=for-the-badge)]()
[![Status](https://img.shields.io/badge/Status-Stable-success?style=for-the-badge&logo=github)]()
[![Build](https://img.shields.io/badge/Build-Passing-brightgreen?style=for-the-badge&logo=githubactions)]()
[![Documentation](https://img.shields.io/badge/Docs-Available-blueviolet?style=for-the-badge&logo=readthedocs)]()
[![Simulation](https://img.shields.io/badge/Mode-Simulation--Only-lightblue?style=for-the-badge&logo=flask)]()

**RX-DDoS Ultimate v5.0 — Educational & Research Documentation**

</div>

> ⚠️ **This project should only be used in a secure and licensed environment and not in a real-world environment, on unlicensed systems, or on a public network.**


⛔Disclaimer: We are not responsible for any illegal use of this tool. ⛔

## 🎯 Overview

**RX-DDoS Ultimate v5.0** is a modular, simulation-based DDoS framework created for academic cybersecurity research and analysis.  
It models distributed network behavior, **command & control (C2)** structure, and **traffic orchestration**, entirely within a **safe simulation environment**.  
No real attack payloads are included or supported.

> This README focuses on theoretical architecture, not offensive execution.

---

## ✨ Features

### ⚙️ Core Highlights

| Feature | Status | Description |
|---|---:|---|
| Modular C2 Architecture | ✅ | Multi-port command & control simulation |
| Real-time Bot Tracking | ✅ | Simulated bot registration system |
| AES-256 Encryption Design | ✅ | Conceptual encrypted channel handling |
| Cross-Platform Compatibility | ✅ | Runs on Windows, macOS, and Linux |
| Simulation Dashboard | ✅ | Tracks mock connections and actions |
| API-Based Extensibility | ✅ | Easily extend modules for research |

---

### 🔬 Research-Oriented Vectors (Conceptual Only)

| Type | OSI Layer | Purpose | Realism Level |
|---|---|---|---:|
| HTTP Request Simulation | Layer 7 | Web flood pattern study | ⭐⭐⭐⭐ |
| SYN/ACK Patterning | Layer 4 | TCP handshake load simulation | ⭐⭐⭐ |
| UDP Burst Simulation | Layer 4 | Stateless packet modeling | ⭐⭐⭐⭐ |
| DNS Amplification Model | Layer 7 | Reflection/amplification research | ⭐⭐⭐⭐⭐ |

---

## 🧩 Architecture Overview

Conceptually, RX-DDoS simulates:
- **C2 Core** — Manages simulated bot registration and coordination.  
- **Bot Clients** — Virtual agents modeled as independent nodes.  
- **Attack Engine (Safe Mode)** — Generates traffic patterns in simulation only.  
- **Admin Console** — Displays internal statistics and simulated metrics.

---

## 🏗️ Code Structure (Conceptual)

```python
# BotnetC2Server — simulation of command-and-control logic
class BotnetC2Server:
    def __init__(self, host='127.0.0.1', ports=[501, 502, 503]):
        self.encryption = "[REDACTED]"
        self.bots = {}
        print("[SIMULATION] C2 Server initialized at", host, ports)

    def register_bot(self, bot_id):
        self.bots[bot_id] = "active"
        print(f"[SIMULATION] Bot {bot_id} registered.")

# AdvancedAttackEngine — simulates attack commands (safe)
class AdvancedAttackEngine:
    def simulate_attack(self, target, duration=60):
        print(f"[SIMULATION] Launching safe-mode test on {target} for {duration}s.")
        return {"status": "simulated", "target": target, "duration": duration}

# Example usage
if __name__ == "__main__":
    c2 = BotnetC2Server()
    c2.register_bot("BOT-001")

    engine = AdvancedAttackEngine()
    result = engine.simulate_attack("example.com")
    print(result)
```

---

## ⚡ Installation

### Prerequisites

- Python 3.8 or newer  
- pip package manager  
- Virtual Environment (recommended)  
- Works on: Windows, macOS, Linux  

### Installation Steps

```bash
git clone https://github.com/your-username/rx-ddos-ultimate.git
cd rx-ddos-ultimate
python -m venv venv
source venv/bin/activate   # macOS/Linux
# venv\Scripts\activate    # Windows
pip install -r requirements-docs.txt
```

---

## 🧪 Lab Usage (Simulation Mode)

All functions are non-destructive and run entirely in **simulation mode**.  
They allow researchers to visualize the coordination and communication flow without affecting real networks.

### Example Run (Safe Mode):

```bash
python rx_c2_simulation.py
python register_bot_sim.py --bot-id BOT-001
python attack_engine.py --target example.com --simulate
---

## 🧰 Example Configuration (JSON)

```json
{
    "c2_server": {
        "host": "127.0.0.1",
        "ports": [501, 502, 503],
        "mode": "simulation"
    },
    "attack_settings": {
        "target": "example.com",
        "threads": 50,
        "duration": 120
    }
}
```

---

## 📡 C2 Linking (Conceptual)

To safely simulate a C2 link:

1. Define your configuration file (`c2_config.json`)  
2. Launch the simulated C2 server locally  
3. Run simulated bot clients within the same test environment  
4. Observe coordination messages in the console/log files  

**Example Code:**

```python
c2 = BotnetC2Server(host="127.0.0.1", ports=[501, 502, 503])
c2.register_bot("BOT-002")
print("[INFO] Simulated bot linked to local C2 successfully.")
```

---

## 🔧 API Reference (Simulation Only)

| Function | Description |
|---|---|
| `register_bot(id)` | Registers a mock bot node |
| `simulate_attack(target, duration)` | Starts a harmless simulation |
| `get_active_bots()` | Lists all simulated bots |
| `shutdown()` | Ends the simulation safely |

---

## 🛡️ Security & Ethics

| Scenario | Allowed | Purpose |
|---|:---:|---|
| Research & Documentation | ✅ | Study distributed coordination safely |
| Defense Training | ✅ | Learn mitigation and detection |
| Real Attacks | ❌ | Illegal & unethical |
| Use on Live Systems | ❌ | Prohibited without written consent |

---

## 🧩 Troubleshooting

| Issue | Solution |
|---|---|
| ModuleNotFoundError | Run `pip install -r requirements-docs.txt` |
| PermissionError | Ensure proper access or use `sudo` on Linux |
| No C2 Connection | Check simulation ports and host IP |
| Simulation Delay | Adjust thread count or reduce logs |

---

## 🤝 Contributing

```bash
git clone https://github.com/your-username/rx-ddos-ultimate.git
git checkout -b feature/new-simulation-module
```

### Areas to Contribute
- Documentation  
- Educational Lab Modules  
- Data Visualization  
- Network Simulation Enhancements  

---

## 📄 License

**MIT License**  
Copyright (c) 2025  
**RX-TEAM — All Rights Reserved**

---

## 🏆 Acknowledgments

- **CRZ101** — Lead Research Developer  
- **RX-TEAM** — Core Simulation & Documentation  
- **Open Source Security Community** — Shared Knowledge  
- **Cybersecurity Labs Worldwide** — Ethical Research Support  

---

> 🧠 *“The purpose of security research is not to destroy systems — but to understand them, so we can make them stronger.”*
