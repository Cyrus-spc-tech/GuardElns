import scapy.all as scapy
from scapy.layers.inet import IP, TCP, UDP

def sniff_traffic():
    def packet_callback(packet):
        if IP in packet:
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            protocol = packet[IP].proto
            packet_size = len(packet)
            timestamp = packet.time
            output = f"src_ip={src_ip}, dst_ip={dst_ip}, protocol={protocol}, packet_size={packet_size}, timestamp={timestamp}"
            if TCP in packet:
                src_port = packet[TCP].sport
                dst_port = packet[TCP].dport
                output += f", src_port={src_port}, dst_port={dst_port}"
            elif UDP in packet:
                src_port = packet[UDP].sport
                dst_port = packet[UDP].dport
                output += f", src_port={src_port}, dst_port={dst_port}"
            print(output)

    # Find your network interface
    iface = scapy.config.conf.iface = scapy.config.conf.iface or scapy.config.conf.interfaces.keys()[0]
    scapy.sniff(iface=iface, prn=packet_callback, store=0) 
