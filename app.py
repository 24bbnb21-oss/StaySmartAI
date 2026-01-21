# -*- coding: utf-8 -*-
"""StaySmart AI – Enterprise HR Intelligence"""

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
if "step" not in st.session_state:
    st.session_state.step = "plan"
if "tier" not in st.session_state:
    st.session_state.tier = None
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# ================= LICENSE KEYS =================
LICENSE_KEYS = {
    "standard": ["SSAI-STD-1A2B-3C4D"],
    "premium": ["SSAI-PRM-X8LQ-4R2Z-M9KP"]
}

# ================= STYLES =================
st.markdown("""
<style>
body { background:#0b1220; }

.hero { text-align:center; padding:70px 20px 30px; }
.hero h1 { font-size:52px; font-weight:800; color:white; }
.hero p { font-size:20px; color:#c7d2fe; }

.plan-card {
    background:#ffffff;
    padding:40px;
    border-radius:28px;
}

.badge { padding:8px 18px; border-radius:20px; font-weight:700; }
.standard { background:#e0f2fe; color:#0369a1; }
.premium { background:#fff7ed; color:#c2410c; }

@keyframes softGlow {
    0% { box-shadow:0 0 25px rgba(99,102,241,0.25); }
    50% { box-shadow:0 0 50px rgba(99,102,241,0.45); }
    100% { box-shadow:0 0 25px rgba(99,102,241,0.25); }
}
.glow { animation:softGlow 4s ease-in-out infinite; }
</style>
""", unsafe_allow_html=True)

# =================================================
# STEP 1: PLAN SELECTION
# =================================================
if st.session_state.step == "plan":

    st.markdown("""
    <div class="hero">
        <h1>StaySmart AI</h1>
        <p>Predict Attrition • Reduce Risk • Retain Talent</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("""
        <div class="plan-card glow">
            <span class="badge standard">STANDARD</span>
            <h3>HR Risk Monitoring</h3>
            <p>Flight risk scores & dashboards</p>
            <h2>₹100 / employee</h2>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Select Standard"):
            st.session_state.tier = "standard"
            st.session_state.step = "auth"
            st.rerun()

    with c2:
        st.markdown("""
        <div class="plan-card glow">
            <span class="badge premium">PREMIUM</span>
            <h3>Predictive HR Intelligence</h3>
            <p>Retention + cost insights</p>
            <h2>₹150 / employee</h2>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Select Premium"):
            st.session_state.tier = "premium"
            st.session_state.step = "auth"
            st.rerun()

    st.markdown("""
    <div style="margin-top:60px;color:#c7d2fe;">
    <h2>About StaySmart AI</h2>
    <p>Enterprise-grade AI to predict attrition and retain talent.</p>
    </div>
    """, unsafe_allow_html=True)

# =================================================
# STEP 2: PAYMENT + ACCESS KEY
# =================================================
elif st.session_state.step == "auth":

    tier = st.session_state.tier
    price = "₹100" if tier == "standard" else "₹150"

    st.markdown(f"""
    <div class="plan-card glow" style="max-width:500px;margin:auto;">
        <span class="badge {'standard' if tier=='standard' else 'premium'}">
            {tier.upper()} PLAN
        </span>
        <h2>{price} / employee</h2>
        <p>Complete payment, then enter access key</p>
    </div>
    """, unsafe_allow_html=True)

    st.info("💳 Payment gateway placeholder (to be added later)")

    key = st.text_input("Enter Access Key", type="password")

    if st.button("Verify & Continue"):
        if key in LICENSE_KEYS[tier]:
            st.session_state.authenticated = True
            st.session_state.step = "dashboard"
            st.rerun()
        else:
            st.error("Invalid access key")

# =================================================
# STEP 3: DASHBOARD
# =================================================
elif st.session_state.step == "dashboard" and st.session_state.authenticated:

    st.success("Access Granted ✔")
    file = st.file_uploader("Upload Employee CSV", type=["csv"])

    if file:
        df = pd.read_csv(file)
        st.write(df.head())

        st.metric("Employees", len(df))
        st.info("Insights generated successfully")
