from scapy.all import sniff, IP, TCP, UDP
from datetime import datetime


def analyze_packet(packet):
    """
    Extract useful information from a network packet.
    """

    packet_info = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "protocol": "OTHER",
        "source": "N/A",
        "destination": "N/A",
        "source_port": "N/A",
        "destination_port": "N/A",
        "size": len(packet)
    }

    # Check for IP layer
    if IP in packet:

        packet_info["source"] = packet[IP].src
        packet_info["destination"] = packet[IP].dst

        # TCP
        if TCP in packet:

            packet_info["protocol"] = "TCP"
            packet_info["source_port"] = packet[TCP].sport
            packet_info["destination_port"] = packet[TCP].dport

        # UDP
        elif UDP in packet:

            packet_info["protocol"] = "UDP"
            packet_info["source_port"] = packet[UDP].sport
            packet_info["destination_port"] = packet[UDP].dport

    return packet_info


def capture_packets(count=20, interface=None):
    """
    Capture packets from the selected network interface.
    """

    captured_packets = []

    def process_packet(packet):

        packet_info = analyze_packet(packet)
        captured_packets.append(packet_info)

    sniff(
        iface=interface,
        prn=process_packet,
        count=count,
        store=False
    )

    return captured_packets


if __name__ == "__main__":

    print("=" * 50)
    print("       MINI WIRESHARK PACKET ANALYZER")
    print("=" * 50)

    print("\nStarting packet capture...")
    print("Press Ctrl+C to stop.\n")

    packets = capture_packets(count=10)

    print("\nCaptured Packets")
    print("-" * 50)

    for packet in packets:

        print(
            f"{packet['time']} | "
            f"{packet['protocol']} | "
            f"{packet['source']} → "
            f"{packet['destination']} | "
            f"{packet['size']} bytes"
        )

    print("\nCapture complete.")
