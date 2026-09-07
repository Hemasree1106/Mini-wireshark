from scapy.all import sniff, IP, TCP, UDP, get_if_list
from datetime import datetime


# =========================================================
# GET AVAILABLE NETWORK INTERFACES
# =========================================================

def get_interfaces():
    """
    Return all network interfaces available on the system.
    """

    try:
        return get_if_list()

    except Exception:
        return []


# =========================================================
# ANALYZE PACKET
# =========================================================

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

    # -----------------------------------------------------
    # IP PACKET
    # -----------------------------------------------------

    if IP in packet:

        packet_info["source"] = packet[IP].src
        packet_info["destination"] = packet[IP].dst

        # -------------------------------------------------
        # TCP
        # -------------------------------------------------

        if TCP in packet:

            packet_info["protocol"] = "TCP"

            packet_info["source_port"] = packet[TCP].sport

            packet_info["destination_port"] = packet[TCP].dport

        # -------------------------------------------------
        # UDP
        # -------------------------------------------------

        elif UDP in packet:

            packet_info["protocol"] = "UDP"

            packet_info["source_port"] = packet[UDP].sport

            packet_info["destination_port"] = packet[UDP].dport

    return packet_info


# =========================================================
# CAPTURE PACKETS
# =========================================================

def capture_packets(count=20, interface=None):
    """
    Capture packets from a selected network interface.
    """

    # Auto-detection
    if interface == "Auto Detect":
        interface = None

    captured_packets = []

    # -----------------------------------------------------
    # PROCESS EACH PACKET
    # -----------------------------------------------------

    def process_packet(packet):

        packet_info = analyze_packet(packet)

        captured_packets.append(packet_info)

    # -----------------------------------------------------
    # START SCAPY CAPTURE
    # -----------------------------------------------------

    sniff(
        iface=interface,
        prn=process_packet,
        count=count,
        store=False
    )

    return captured_packets


# =========================================================
# TEST MODE
# =========================================================

if __name__ == "__main__":

    print("=" * 60)

    print(
        "           MINI WIRESHARK"
    )

    print(
        "        NETWORK PACKET ANALYZER"
    )

    print("=" * 60)

    print("\nAvailable Network Interfaces:")

    interfaces = get_interfaces()

    if interfaces:

        for index, interface in enumerate(
            interfaces,
            start=1
        ):

            print(
                f"{index}. {interface}"
            )

    else:

        print(
            "No network interfaces detected."
        )

    print("\nStarting packet capture...")

    print(
        "Press Ctrl+C to stop.\n"
    )

    try:

        packets = capture_packets(
            count=10
        )

        print(
            "\nCaptured Packets"
        )

        print(
            "-" * 60
        )

        for packet in packets:

            print(
                f"{packet['time']} | "
                f"{packet['protocol']} | "
                f"{packet['source']} → "
                f"{packet['destination']} | "
                f"{packet['size']} bytes"
            )

        print(
            "\nCapture complete."
        )

    except KeyboardInterrupt:

        print(
            "\nCapture stopped by user."
        )

    except Exception as error:

        print(
            f"\nCapture failed: {error}"
        )
