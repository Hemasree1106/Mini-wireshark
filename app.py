import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

from packet_analyzer import capture_packets, get_interfaces


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Mini Wireshark",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background: #0b1120;
    color: #e5e7eb;
}

[data-testid="stSidebar"] {
    background: #111827;
    border-right: 1px solid #1f2937;
}

.main-title {
    font-size: 38px;
    font-weight: 800;
}

.subtitle {
    color: #9ca3af;
    font-size: 15px;
}

.status {
    background: #052e16;
    color: #4ade80;
    padding: 8px 15px;
    border-radius: 20px;
    font-weight: 600;
    text-align: center;
}

.metric-card {
    background: #111827;
    border: 1px solid #1f2937;
    border-radius: 14px;
    padding: 20px;
    min-height: 110px;
}

.metric-title {
    color: #9ca3af;
    font-size: 13px;
    font-weight: 600;
}

.metric-value {
    font-size: 30px;
    font-weight: 800;
    margin-top: 8px;
}

.section-title {
    font-size: 20px;
    font-weight: 700;
    margin-top: 20px;
    margin-bottom: 12px;
}

.alert {
    background: #1f1720;
    border: 1px solid #7f1d1d;
    border-radius: 10px;
    padding: 14px;
    margin-bottom: 10px;
}

.demo-box {
    background: #172554;
    border: 1px solid #2563eb;
    border-radius: 10px;
    padding: 12px;
    margin-top: 10px;
}

.footer {
    text-align: center;
    color: #6b7280;
    margin-top: 40px;
    font-size: 12px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SESSION STATE
# =========================================================

if "captured_packets" not in st.session_state:
    st.session_state.captured_packets = []

if "demo_mode" not in st.session_state:
    st.session_state.demo_mode = False


# =========================================================
# DEMO PACKET GENERATOR
# =========================================================

def generate_demo_packets(count=80):

    protocols = ["TCP", "UDP", "HTTP", "DNS", "ICMP"]

    source_ips = [
        "192.168.1.10",
        "192.168.1.15",
        "192.168.1.20",
        "192.168.1.25",
        "192.168.1.30"
    ]

    destination_ips = [
        "142.250.183.14",
        "8.8.8.8",
        "1.1.1.1",
        "104.18.32.47",
        "172.217.160.78",
        "13.107.42.12"
    ]

    packets = []

    start_time = datetime.now()

    for i in range(count):

        protocol = random.choices(
            protocols,
            weights=[40, 25, 12, 18, 5],
            k=1
        )[0]

        source = random.choice(source_ips)
        destination = random.choice(destination_ips)

        source_port = random.choice(
            [1024, 2048, 3128, 49152, 52000, 55000, 60000]
        )

        if protocol == "HTTP":
            destination_port = 80

        elif protocol == "DNS":
            destination_port = 53

        elif protocol == "TCP":
            destination_port = random.choice(
                [80, 443, 22, 8080]
            )

        elif protocol == "UDP":
            destination_port = random.choice(
                [53, 123, 443, 500, 4500]
            )

        else:
            destination_port = "N/A"

        packet_size = random.randint(64, 1490)

        # Occasionally create a large packet
        if random.random() < 0.08:
            packet_size = random.randint(1501, 2200)

        packet_time = (
            start_time + timedelta(seconds=i)
        ).strftime("%H:%M:%S")

        packets.append({
            "time": packet_time,
            "protocol": protocol,
            "source": source,
            "destination": destination,
            "source_port": source_port,
            "destination_port": destination_port,
            "size": packet_size
        })

    return packets


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## 🛡️ Mini Wireshark")
    st.caption("Network Packet Intelligence")

    st.divider()

    st.markdown("### 📡 Capture Settings")

    # -----------------------------------------------------
    # REAL NETWORK INTERFACES
    # -----------------------------------------------------

    interfaces = get_interfaces()

    interface_options = ["Auto Detect"] + interfaces

    interface = st.selectbox(
        "Network Interface",
        interface_options
    )

    packet_limit = st.slider(
        "Packet Limit",
        min_value=10,
        max_value=1000,
        value=100
    )

    protocol_filter = st.multiselect(
        "Protocol Filter",
        ["TCP", "UDP", "HTTP", "DNS", "ICMP"],
        default=["TCP", "UDP", "HTTP", "DNS", "ICMP"]
    )

    st.divider()

    # =====================================================
    # DEMO TRAFFIC
    # =====================================================

    st.markdown("### 🎮 Presentation Mode")

    if st.button(
        "🎲 Generate Demo Traffic",
        use_container_width=True
    ):

        demo_packets = generate_demo_packets(
            packet_limit
        )

        st.session_state.captured_packets = demo_packets
        st.session_state.demo_mode = True

        st.success(
            f"Generated {len(demo_packets)} demo packets."
        )

    if st.session_state.demo_mode:

        st.markdown(
            """
            <div class="demo-box">
                🎮 <b>DEMO MODE ACTIVE</b><br>
                Simulated network traffic is being displayed.
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    # =====================================================
    # REAL PACKET CAPTURE
    # =====================================================

    if st.button(
        "▶️ Start Real Capture",
        use_container_width=True
    ):

        st.session_state.demo_mode = False

        with st.spinner(
            "Capturing real network packets..."
        ):

            try:

                interface_name = (
                    None
                    if interface == "Auto Detect"
                    else interface
                )

                packets = capture_packets(
                    count=packet_limit,
                    interface=interface_name
                )

                st.session_state.captured_packets = packets

                st.success(
                    f"Captured {len(packets)} packets."
                )

            except Exception as error:

                st.error(
                    f"Packet capture failed: {error}"
                )

    # =====================================================
    # CLEAR
    # =====================================================

    if st.button(
        "🗑️ Clear Packets",
        use_container_width=True
    ):

        st.session_state.captured_packets = []
        st.session_state.demo_mode = False

        st.success("Packet data cleared.")

    st.divider()

    # =====================================================
    # SYSTEM STATUS
    # =====================================================

    st.markdown("### ⚙️ System Status")

    st.success("Scapy Engine Ready")
    st.success("Analyzer Operational")


# =========================================================
# HEADER
# =========================================================

header_left, header_right = st.columns([4, 1])

with header_left:

    st.markdown(
        '<div class="main-title">'
        '🛡️ Mini Wireshark'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Real-time network packet analysis and security monitoring'
        '</div>',
        unsafe_allow_html=True
    )

with header_right:

    st.markdown(
        '<div class="status">'
        '● SYSTEM ONLINE'
        '</div>',
        unsafe_allow_html=True
    )

st.write("")


# =========================================================
# PACKET DATA
# =========================================================

packets = st.session_state.captured_packets

if packets:

    packet_df = pd.DataFrame(packets)

else:

    packet_df = pd.DataFrame(
        columns=[
            "time",
            "protocol",
            "source",
            "destination",
            "source_port",
            "destination_port",
            "size"
        ]
    )


# =========================================================
# FILTER PACKETS
# =========================================================

if not packet_df.empty and protocol_filter:

    filtered_packets = packet_df[
        packet_df["protocol"].isin(protocol_filter)
    ]

else:

    filtered_packets = packet_df


# =========================================================
# METRICS
# =========================================================

total_packets = len(packet_df)

tcp_packets = (
    len(packet_df[
        packet_df["protocol"] == "TCP"
    ])
    if not packet_df.empty else 0
)

udp_packets = (
    len(packet_df[
        packet_df["protocol"] == "UDP"
    ])
    if not packet_df.empty else 0
)

http_packets = (
    len(packet_df[
        packet_df["protocol"] == "HTTP"
    ])
    if not packet_df.empty else 0
)


# =========================================================
# METRIC CARDS
# =========================================================

c1, c2, c3, c4 = st.columns(4)


with c1:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">
                📦 TOTAL PACKETS
            </div>
            <div class="metric-value">
                {total_packets:,}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with c2:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">
                🔵 TCP TRAFFIC
            </div>
            <div class="metric-value">
                {tcp_packets:,}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with c3:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">
                🟣 UDP TRAFFIC
            </div>
            <div class="metric-value">
                {udp_packets:,}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with c4:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">
                🌐 HTTP TRAFFIC
            </div>
            <div class="metric-value">
                {http_packets:,}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# NETWORK TRAFFIC
# =========================================================

st.markdown(
    '<div class="section-title">'
    '📈 Network Traffic'
    '</div>',
    unsafe_allow_html=True
)

if not packet_df.empty:

    traffic = (
        packet_df
        .groupby("time")
        .size()
        .reset_index(name="Packets")
        .set_index("time")
    )

    st.line_chart(
        traffic,
        height=280
    )

else:

    st.info(
        "Generate demo traffic or start a real capture "
        "to display network traffic."
    )


# =========================================================
# PACKET INSPECTOR + SECURITY ALERTS
# =========================================================

left, right = st.columns([2.2, 1])


# =========================================================
# PACKET INSPECTOR
# =========================================================

with left:

    st.markdown(
        '<div class="section-title">'
        '🔍 Packet Inspector'
        '</div>',
        unsafe_allow_html=True
    )

    if not filtered_packets.empty:

        display_df = filtered_packets.rename(
            columns={
                "time": "Time",
                "protocol": "Protocol",
                "source": "Source IP",
                "destination": "Destination IP",
                "source_port": "Source Port",
                "destination_port": "Destination Port",
                "size": "Size (Bytes)"
            }
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No packets match the selected protocol filter."
        )


# =========================================================
# SECURITY ALERTS
# =========================================================

with right:

    st.markdown(
        '<div class="section-title">'
        '⚠️ Security Alerts'
        '</div>',
        unsafe_allow_html=True
    )

    # HTTP ALERT

    http_detected = (
        not packet_df.empty
        and "HTTP" in packet_df["protocol"].values
    )

    if http_detected:

        st.markdown(
            """
            <div class="alert">
                🔴 <b>HIGH</b><br>
                HTTP traffic detected<br>
                <small>
                Unencrypted HTTP communication found.
                </small>
            </div>
            """,
            unsafe_allow_html=True
        )

    # LARGE PACKET ALERT

    if not packet_df.empty:

        large_packets = packet_df[
            packet_df["size"] > 1500
        ]

    else:

        large_packets = pd.DataFrame()

    if not large_packets.empty:

        st.markdown(
            """
            <div class="alert">
                🟠 <b>MEDIUM</b><br>
                Large packet detected<br>
                <small>
                Packet size exceeds 1500 bytes.
                </small>
            </div>
            """,
            unsafe_allow_html=True
        )

    if not http_detected and large_packets.empty:

        st.info(
            "No security alerts detected."
        )


# =========================================================
# ANALYTICS
# =========================================================

analytics1, analytics2 = st.columns(2)


# =========================================================
# PROTOCOL DISTRIBUTION
# =========================================================

with analytics1:

    st.markdown(
        '<div class="section-title">'
        '📊 Protocol Distribution'
        '</div>',
        unsafe_allow_html=True
    )

    if not packet_df.empty:

        protocol_data = (
            packet_df["protocol"]
            .value_counts()
            .rename_axis("Protocol")
            .reset_index(name="Packets")
        )

        st.bar_chart(
            protocol_data.set_index("Protocol")
        )

    else:

        st.info(
            "Protocol statistics will appear after capture."
        )


# =========================================================
# TOP NETWORK ENDPOINTS
# =========================================================

with analytics2:

    st.markdown(
        '<div class="section-title">'
        '🌐 Top Network Endpoints'
        '</div>',
        unsafe_allow_html=True
    )

    if not packet_df.empty:

        endpoints = (
            packet_df["destination"]
            .value_counts()
            .head(10)
            .rename_axis("IP Address")
            .reset_index(name="Packets")
        )

        st.dataframe(
            endpoints,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "Network endpoints will appear after capture."
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    "Mini Wireshark • Python + Scapy + Streamlit\n\n"
    "Network monitoring and packet analysis platform"
)
