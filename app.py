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
defaults = {
    "page": "Home",
    "step": "plan",        # plan → payment → auth → dashboard
    "tier": None,
    "authenticated": False
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("## 🧠 StaySmart AI")
    st.session_state.page = st.radio(
        "Navigate",
        ["Home", "Dashboard", "About Us"],
        index=["Home", "Dashboard", "About Us"].index(st.session_state.page)
    )
    st.markdown("---")
    st.caption("© EXQ-16")

# ================= GLOBAL STYLES =================
st.markdown("""
<style>
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
.hero h1 { font-size:64px; color:white; font-weight:900; }
.hero p { font-size:22px; color:#e0e7ff; }

.glass {
    background:rgba(255,255,255,0.08);
    backdrop-filter: blur(18px);
    border-radius:28px;
    padding:40px;
    box-shadow:0 30px 80px rgba(0,0,0,0.35);
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

    st.markdown("## Choose Your Plan")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="glass">
            <h3>Standard</h3>
            <p>₹100 / employee / month</p>
            <ul>
                <li>Flight risk prediction</li>
                <li>Risk categorization</li>
                <li>Visual dashboards</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Select Standard", key="std"):
            st.session_state.tier = "standard"
            st.session_state.step = "payment"
            st.session_state.page = "Dashboard"
            st.rerun()

    with col2:
        st.markdown("""
        <div class="glass">
            <h3>Premium</h3>
            <p>₹150 / employee / month</p>
            <ul>
                <li>Everything in Standard</li>
                <li>Risk simulator</li>
                <li>Immediate / Short / Long-term retention</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Select Premium", key="prm"):
            st.session_state.tier = "premium"
            st.session_state.step = "payment"
            st.session_state.page = "Dashboard"
            st.rerun()

    st.markdown("""
    <div class="footer">
        © 2026 EXQ-16. All rights reserved.
    </div>
    """, unsafe_allow_html=True)

# =================================================
# ================= ABOUT PAGE ====================
# =================================================
elif st.session_state.page == "About Us":
    st.markdown("""
    <div class="glass">
        <h2>About EXQ-16</h2>
        <p>
        EXQ-16 is an innovation-driven team building enterprise-grade AI
        solutions for decision intelligence.
        </p>
        <p>
        StaySmart AI helps organizations proactively identify attrition risks
        and design effective retention strategies.
        </p>
    </div>
    """, unsafe_allow_html=True)

# =================================================
# ================= DASHBOARD =====================
# =================================================
elif st.session_state.page == "Dashboard":

    # If no plan chosen → redirect
    if st.session_state.tier is None:
        st.warning("Please select a plan to continue.")
        st.session_state.page = "Home"
        st.rerun()

    # -------- PAYMENT --------
    if st.session_state.step == "payment":
        st.success("Payment Successful (Demo)")
        if st.button("Continue to Access Code"):
            st.session_state.step = "auth"
            st.rerun()

    # -------- AUTH --------
    elif st.session_state.step == "auth":
        key = st.text_input("Enter Access Key", type="password")
        if st.button("Verify"):
            st.session_state.authenticated = True
            st.session_state.step = "dashboard"
            st.rerun()

    # -------- FINAL DASHBOARD --------
    elif st.session_state.step == "dashboard" and st.session_state.authenticated:
        st.markdown("## StaySmart AI Dashboard")
        st.info("Upload employee CSV to begin analysis")

        # ⬇️ YOUR EXISTING ML / CSV / MODEL LOGIC CONTINUES HERE ⬇️
