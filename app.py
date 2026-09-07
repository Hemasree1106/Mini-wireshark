import streamlit as st
import pandas as pd
from packet_analyzer import capture_packets


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
    margin-bottom: 0;
}

.subtitle {
    color: #9ca3af;
    font-size: 15px;
    margin-top: 4px;
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

if "capturing" not in st.session_state:
    st.session_state.capturing = False

if "captured_packets" not in st.session_state:
    st.session_state.captured_packets = []


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## 🛡️ Mini Wireshark")
    st.caption("Network Packet Intelligence")

    st.divider()

    st.markdown("### 📡 Capture Settings")

    interface = st.selectbox(
        "Network Interface",
        [
            "Auto Detect",
            "Wi-Fi",
            "Ethernet",
            "Loopback"
        ]
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
        default=["TCP", "UDP"]
    )

    st.divider()

    # -----------------------------------------------------
    # START CAPTURE
    # -----------------------------------------------------

    if st.button(
        "▶️ Start Capture",
        use_container_width=True
    ):

        st.session_state.capturing = True

        with st.spinner("Capturing network packets..."):

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

        st.session_state.capturing = False

    # -----------------------------------------------------
    # STOP CAPTURE
    # -----------------------------------------------------

    if st.button(
        "⏹️ Stop Capture",
        use_container_width=True
    ):

        st.session_state.capturing = False

        st.warning(
            "Capture stopped."
        )

    st.divider()

    # -----------------------------------------------------
    # SYSTEM STATUS
    # -----------------------------------------------------

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
# PROCESS CAPTURED PACKETS
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
    len(packet_df[packet_df["protocol"] == "TCP"])
    if not packet_df.empty
    else 0
)

udp_packets = (
    len(packet_df[packet_df["protocol"] == "UDP"])
    if not packet_df.empty
    else 0
)

http_packets = 0

if not packet_df.empty:

    http_packets = len(
        packet_df[
            packet_df["protocol"] == "HTTP"
        ]
    )


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
    )

    traffic = traffic.set_index("time")

    st.line_chart(
        traffic,
        height=280
    )

else:

    st.info(
        "Start packet capture to display live network traffic."
    )


# =========================================================
# PACKET INSPECTOR + ALERTS
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
            "No packets available. "
            "Start a capture to inspect packets."
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

    http_detected = False

    if not packet_df.empty:

        http_detected = (
            "HTTP" in packet_df["protocol"].values
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

    if not packet_df.empty:

        large_packets = packet_df[
            packet_df["size"] > 1500
        ]

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

    if not http_detected and packet_df.empty:

        st.info(
            "No security alerts yet."
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
            "Protocol statistics will appear "
            "after packet capture."
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
            "Network endpoints will appear "
            "after packet capture."
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">

        Mini Wireshark • Python + Scapy + Streamlit

        <br>

        Network monitoring and packet analysis platform

    </div>
    """,
    unsafe_allow_html=True
)
