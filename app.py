# ================= IMPORTS =================
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="StaySmart AI",
    layout="wide",
    page_icon="🧠"
)

# ================= SESSION STATE =================
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "step" not in st.session_state:
    st.session_state.step = "plan"
if "tier" not in st.session_state:
    st.session_state.tier = None
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# ================= SIDEBAR NAV =================
with st.sidebar:
    st.markdown("## 🧠 StaySmart AI")
    st.session_state.page = st.radio(
        "Navigate",
        ["Home", "Dashboard", "About Us"]
    )
    st.markdown("---")
    st.caption("© EXQ-16")

# ================= GLOBAL STYLES =================
st.markdown("""
<style>
html { scroll-behavior:smooth; }

.hero {
    min-height:90vh;
    background:linear-gradient(135deg,#4f46e5,#7c3aed);
    display:flex;
    align-items:center;
    justify-content:center;
    text-align:center;
    border-radius:30px;
    padding:60px;
}

.hero h1 {
    font-size:64px;
    font-weight:900;
    color:white;
}

.hero p {
    font-size:22px;
    color:#e0e7ff;
}

.glass {
    background:rgba(255,255,255,0.08);
    backdrop-filter: blur(18px);
    border-radius:28px;
    padding:40px;
    box-shadow:0 30px 80px rgba(0,0,0,0.35);
}

.pulse {
    animation:pulseGlow 3s infinite;
}

@keyframes pulseGlow {
    0% { box-shadow:0 0 25px rgba(124,58,237,0.4); }
    50% { box-shadow:0 0 60px rgba(124,58,237,0.8); }
    100% { box-shadow:0 0 25px rgba(124,58,237,0.4); }
}

.footer {
    text-align:center;
    padding:40px;
    color:#94a3b8;
}
</style>
""", unsafe_allow_html=True)

# =================================================
# ================= HOME PAGE =====================
# =================================================
if st.session_state.page == "Home":

    st.markdown("""
    <div class="hero">
        <div>
            <h1>StaySmart AI</h1>
            <p>Enterprise HR Intelligence Platform</p>
            <p>Predict Attrition • Retain Talent • Reduce Cost</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown("## Choose Your Plan")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="glass pulse">
            <h3>Standard</h3>
            <p>₹100 / employee / month</p>
            <ul>
                <li>Flight risk prediction</li>
                <li>Risk categorization</li>
                <li>Visual dashboards</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Select Standard"):
            st.session_state.tier = "standard"
            st.session_state.step = "payment"
            st.session_state.page = "Dashboard"
            st.rerun()

    with col2:
        st.markdown("""
        <div class="glass pulse">
            <h3>Premium</h3>
            <p>₹150 / employee / month</p>
            <ul>
                <li>Everything in Standard</li>
                <li>Risk simulator</li>
                <li>Immediate / Short / Long-term retention</li>
                <li>Leadership insights</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Select Premium"):
            st.session_state.tier = "premium"
            st.session_state.step = "payment"
            st.session_state.page = "Dashboard"
            st.rerun()

    st.markdown("""
    <div class="footer">
        © 2026 EXQ-16. All rights reserved.
    </div>
    """, unsafe_allow_html=True)

    st.stop()

# =================================================
# ================= ABOUT PAGE ====================
# =================================================
if st.session_state.page == "About Us":
    st.markdown("""
    <div class="glass">
        <h2>About EXQ-16</h2>
        <p>
        EXQ-16 is an innovation-driven analytics team focused on building
        enterprise-grade AI systems.
        </p>
        <p>
        StaySmart AI was designed to help organizations proactively reduce
        attrition, understand workforce risks, and build long-term retention
        strategies using data-driven intelligence.
        </p>
        <p>
        Built for performance. Designed for leadership.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# =================================================
# ================= DASHBOARD =====================
# =================================================
if st.session_state.page == "Dashboard":

    # If user clicks Dashboard without selecting plan
    if st.session_state.tier is None:
        st.info("Please select a plan to continue.")
        st.session_state.page = "Home"
        st.rerun()

    # ---------------- PAYMENT STEP ----------------
    if st.session_state.step == "payment":
        st.success("Payment Successful (Demo)")
        if st.button("Continue"):
            st.session_state.step = "auth"
            st.rerun()
        st.stop()

    # ---------------- AUTH STEP ----------------
    if st.session_state.step == "auth":
        key = st.text_input("Enter Access Key", type="password")
        if st.button("Verify"):
            st.session_state.authenticated = True
            st.session_state.step = "dashboard"
            st.rerun()
        st.stop()

    # ---------------- FINAL DASHBOARD ----------------
    if not st.session_state.authenticated:
        st.stop()

    st.markdown("## StaySmart AI Dashboard")
    st.markdown("Upload employee CSV to begin analysis")

    # ---------- YOUR EXISTING DASHBOARD LOGIC CONTINUES BELOW ----------
    # (CSV upload, ML model, charts, premium insights etc.)
