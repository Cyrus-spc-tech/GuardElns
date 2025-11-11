"""
Network Traffic Capture Module
Captures and analyzes network packets in real-time
"""

import time
import threading
from datetime import datetime
from collections import deque
import psutil
import pandas as pd

try:
    from scapy.all import sniff, IP, TCP, UDP, ICMP
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False
    print("Warning: Scapy not available. Using simulation mode.")


class TrafficCapture:
    def __init__(self, interface="auto", packet_count=1000, timeout=60):
        self.interface = self._get_interface() if interface == "auto" else interface
        self.packet_count = packet_count
        self.timeout = timeout
        self.packets = deque(maxlen=10000)
        self.is_capturing = False
        self.capture_thread = None
        self.stats = {
            'total_packets': 0,
            'tcp_packets': 0,
            'udp_packets': 0,
            'icmp_packets': 0,
            'other_packets': 0
        }
        
    def _get_interface(self):
        """Auto-detect active network interface"""
        try:
            interfaces = psutil.net_if_addrs()
            for iface in interfaces:
                if iface != 'lo' and iface != 'Loopback':
                    return iface
            return list(interfaces.keys())[0]
        except:
            return "eth0"
    
    def packet_callback(self, packet):
        """Process captured packet"""
        try:
            packet_info = {
                'timestamp': datetime.now(),
                'src_ip': None,
                'dst_ip': None,
                'src_port': None,
                'dst_port': None,
                'protocol': 'OTHER',
                'length': len(packet),
                'flags': None
            }
            
            if IP in packet:
                packet_info['src_ip'] = packet[IP].src
                packet_info['dst_ip'] = packet[IP].dst
                
                if TCP in packet:
                    packet_info['protocol'] = 'TCP'
                    packet_info['src_port'] = packet[TCP].sport
                    packet_info['dst_port'] = packet[TCP].dport
                    packet_info['flags'] = str(packet[TCP].flags)
                    self.stats['tcp_packets'] += 1
                    
                elif UDP in packet:
                    packet_info['protocol'] = 'UDP'
                    packet_info['src_port'] = packet[UDP].sport
                    packet_info['dst_port'] = packet[UDP].dport
                    self.stats['udp_packets'] += 1
                    
                elif ICMP in packet:
                    packet_info['protocol'] = 'ICMP'
                    self.stats['icmp_packets'] += 1
                else:
                    self.stats['other_packets'] += 1
            
            self.stats['total_packets'] += 1
            self.packets.append(packet_info)
            
        except Exception as e:
            print(f"Error processing packet: {e}")
    
    def start_capture(self):
        """Start packet capture in background thread"""
        if not SCAPY_AVAILABLE:
            print("Starting simulation mode...")
            self.is_capturing = True
            self.capture_thread = threading.Thread(target=self._simulate_traffic)
            self.capture_thread.daemon = True
            self.capture_thread.start()
            return
        
        self.is_capturing = True
        self.capture_thread = threading.Thread(target=self._capture_packets)
        self.capture_thread.daemon = True
        self.capture_thread.start()
    
    def _capture_packets(self):
        """Capture packets using Scapy"""
        try:
            sniff(
                iface=self.interface,
                prn=self.packet_callback,
                store=False,
                stop_filter=lambda x: not self.is_capturing
            )
        except Exception as e:
            print(f"Capture error: {e}")
            self.is_capturing = False
    
    def _simulate_traffic(self):
        """Simulate network traffic for testing"""
        import random
        
        protocols = ['TCP', 'UDP', 'ICMP']
        ips = [f"192.168.1.{i}" for i in range(1, 50)]
        
        while self.is_capturing:
            packet_info = {
                'timestamp': datetime.now(),
                'src_ip': random.choice(ips),
                'dst_ip': random.choice(ips),
                'src_port': random.randint(1024, 65535),
                'dst_port': random.choice([80, 443, 22, 3306, 8080]),
                'protocol': random.choice(protocols),
                'length': random.randint(64, 1500),
                'flags': random.choice(['S', 'SA', 'A', 'PA', 'F'])
            }
            
            self.packets.append(packet_info)
            self.stats['total_packets'] += 1
            
            if packet_info['protocol'] == 'TCP':
                self.stats['tcp_packets'] += 1
            elif packet_info['protocol'] == 'UDP':
                self.stats['udp_packets'] += 1
            else:
                self.stats['icmp_packets'] += 1
            
            time.sleep(random.uniform(0.01, 0.1))
    
    def stop_capture(self):
        """Stop packet capture"""
        self.is_capturing = False
        if self.capture_thread:
            self.capture_thread.join(timeout=2)
    
    def get_packets_df(self, limit=None):
        """Get captured packets as DataFrame"""
        packets_list = list(self.packets)
        if limit:
            packets_list = packets_list[-limit:]
        return pd.DataFrame(packets_list)
    
    def get_stats(self):
        """Get capture statistics"""
        return self.stats.copy()
    
    def clear_packets(self):
        """Clear packet buffer"""
        self.packets.clear()
        self.stats = {
            'total_packets': 0,
            'tcp_packets': 0,
            'udp_packets': 0,
            'icmp_packets': 0,
            'other_packets': 0
        }
