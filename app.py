import streamlit as st
import pandas as pd

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Mini Wireshark",
    page_icon="🛡️",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

.stApp {
    background: #0b1120;
    color: #e5e7eb;
}

[data-testid="stSidebar"] {
    background: #111827;
}

.main-title {
    font-size: 38px;
    font-weight: 800;
    margin-bottom: 0;
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

# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.markdown("## 🛡️ Mini Wireshark")
    st.caption("Network Packet Intelligence")

    st.divider()

    st.markdown("### 📡 Capture Settings")

    interface = st.selectbox(
        "Network Interface",
        ["Auto Detect", "Wi-Fi", "Ethernet", "Loopback"]
    )

    packet_limit = st.slider(
        "Packet Limit",
        10,
        1000,
        100
    )

    protocol = st.multiselect(
        "Protocol Filter",
        ["TCP", "UDP", "HTTP", "DNS", "ICMP"],
        default=["TCP", "UDP"]
    )

    st.divider()

    start = st.button(
        "▶️ Start Capture",
        use_container_width=True
    )

    stop = st.button(
        "⏹️ Stop Capture",
        use_container_width=True
    )

    st.divider()

    st.markdown("### ⚙️ System Status")

    st.success("Scapy Engine Ready")
    st.success("Analyzer Operational")

# ---------------- HEADER ----------------

col1, col2 = st.columns([4, 1])

with col1:

    st.markdown(
        '<div class="main-title">🛡️ Mini Wireshark</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Real-time network packet analysis and security monitoring'
        '</div>',
        unsafe_allow_html=True
    )

with col2:

    st.markdown(
        '<div class="status">● SYSTEM ONLINE</div>',
        unsafe_allow_html=True
    )

st.write("")

# ---------------- METRICS ----------------

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">📦 TOTAL PACKETS</div>
        <div class="metric-value">12,842</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">🔵 TCP TRAFFIC</div>
        <div class="metric-value">7,231</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">🟣 UDP TRAFFIC</div>
        <div class="metric-value">4,982</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">🌐 HTTP TRAFFIC</div>
        <div class="metric-value">629</div>
    </div>
    """, unsafe_allow_html=True)

# ---------------- TRAFFIC ----------------

st.markdown(
    '<div class="section-title">📈 Network Traffic</div>',
    unsafe_allow_html=True
)

traffic = pd.DataFrame({
    "Packets": [
        120, 180, 145, 210, 190,
        250, 220, 280, 260, 310,
        290, 350, 320, 380, 360
    ]
})

st.line_chart(
    traffic,
    height=280
)

# ---------------- PACKET INSPECTOR ----------------

left, right = st.columns([2.2, 1])

with left:

    st.markdown(
        '<div class="section-title">🔍 Packet Inspector</div>',
        unsafe_allow_html=True
    )

    packets = pd.DataFrame({

        "Time": [
            "14:32:01",
            "14:32:02",
            "14:32:03",
            "14:32:04",
            "14:32:05",
            "14:32:06"
        ],

        "Protocol": [
            "TCP",
            "UDP",
            "TCP",
            "HTTP",
            "UDP",
            "DNS"
        ],

        "Source IP": [
            "192.168.1.5",
            "192.168.1.5",
            "192.168.1.10",
            "192.168.1.5",
            "192.168.1.10",
            "192.168.1.10"
        ],

        "Destination": [
            "142.250.72.14",
            "8.8.8.8",
            "142.250.72.14",
            "93.184.216.34",
            "8.8.8.8",
            "8.8.8.8"
        ],

        "Port": [
            443,
            53,
            443,
            80,
            53,
            53
        ],

        "Size": [
            "1240 B",
            "128 B",
            "982 B",
            "640 B",
            "156 B",
            "92 B"
        ]
    })

    st.dataframe(
        packets,
        use_container_width=True,
        hide_index=True
    )

# ---------------- ALERTS ----------------

with right:

    st.markdown(
        '<div class="section-title">⚠️ Security Alerts</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="alert">
        🔴 <b>HIGH</b><br>
        HTTP traffic detected<br>
        <small>Unencrypted HTTP communication</small>
    </div>

    <div class="alert">
        🟠 <b>MEDIUM</b><br>
        High traffic source<br>
        <small>Unusual packet activity detected</small>
    </div>

    <div class="alert">
        🟠 <b>MEDIUM</b><br>
        Multiple connections<br>
        <small>Repeated TCP connections detected</small>
    </div>
    """, unsafe_allow_html=True)

# ---------------- ANALYTICS ----------------

a1, a2 = st.columns(2)

with a1:

    st.markdown(
        '<div class="section-title">📊 Protocol Distribution</div>',
        unsafe_allow_html=True
    )

    protocol_data = pd.DataFrame({
        "Protocol": ["TCP", "UDP", "HTTP", "DNS"],
        "Packets": [7231, 4982, 629, 412]
    })

    st.bar_chart(
        protocol_data.set_index("Protocol")
    )

with a2:

    st.markdown(
        '<div class="section-title">🌐 Top Network Endpoints</div>',
        unsafe_allow_html=True
    )

    endpoints = pd.DataFrame({
        "IP Address": [
            "192.168.1.5",
            "8.8.8.8",
            "142.250.72.14",
            "192.168.1.10"
        ],

        "Packets": [
            4231,
            2180,
            1642,
            1321
        ]
    })

    st.dataframe(
        endpoints,
        use_container_width=True,
        hide_index=True
    )

# ---------------- FOOTER ----------------

st.markdown("""
<div class="footer">
    Mini Wireshark • Python + Scapy + Streamlit
    <br>
    Network monitoring and packet analysis platform
</div>
""", unsafe_allow_html=True)
