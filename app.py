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
if "nav" not in st.session_state:
    st.session_state.nav = "Home"

# ================= LICENSE KEYS =================
LICENSE_KEYS = {
    "standard": ["SSAI-STD-1A2B-3C4D"],
    "premium": ["SSAI-PRM-X8LQ-4R2Z-M9KP"]
}

# ================= STYLES =================
st.markdown("""
<style>
body { background:#0b1220; }

.hero {
    text-align:center;
    padding:70px 20px 30px;
}

.hero h1 {
    font-size:52px;
    font-weight:800;
    color:white;
}

.hero p {
    font-size:20px;
    color:#c7d2fe;
}

.plan-card {
    background:#ffffff;
    padding:40px;
    border-radius:28px;
    box-shadow:0 30px 70px rgba(0,0,0,0.35);
    height:100%;
}

.plan-title {
    font-size:28px;
    font-weight:800;
    color:#0f172a;
    margin-top:15px;
}

.plan-desc {
    color:#475569;
    font-size:16px;
    margin:15px 0;
}

.price {
    font-size:40px;
    font-weight:800;
    color:#111827;
    margin:20px 0;
}

ul {
    padding-left:20px;
    color:#334155;
    font-size:15px;
}

li {
    margin-bottom:8px;
}

.badge {
    padding:8px 18px;
    border-radius:20px;
    font-weight:700;
    display:inline-block;
}

.standard { background:#e0f2fe; color:#0369a1; }
.premium { background:#fff7ed; color:#c2410c; }

.req-box {
    background:#0f172a;
    color:#e5e7eb;
    padding:28px;
    border-radius:20px;
    margin-top:30px;
}

.compare {
    background:#0f172a;
    padding:25px;
    border-radius:25px;
    margin-top:30px;
}
</style>
""", unsafe_allow_html=True)

# =================================================
# =============== STEP 1: PLAN SELECT ===============
# =================================================
if st.session_state.step == "plan":

    st.markdown("""
    <div class="hero">
        <h1>StaySmart AI</h1>
        <p>Predict Attrition • Reduce Risk • Retain Talent</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="plan-card">
            <span class="badge standard">STANDARD</span>
            <div class="plan-title">HR Risk Monitoring</div>
            <div class="plan-desc">
                Identify employees who may leave and monitor risk levels.
            </div>
            <div class="price">₹100 / employee / month</div>
            <ul>
                <li>Employee flight risk score</li>
                <li>High / Medium / Low risk tags</li>
                <li>Top risk employees list</li>
                <li>Clear visual dashboards</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Select Standard Plan"):
            st.session_state.tier = "standard"
            st.session_state.step = "auth"
            st.rerun()

    with col2:
        st.markdown("""
        <div class="plan-card">
            <span class="badge premium">PREMIUM</span>
            <div class="plan-title">Predictive HR Intelligence</div>
            <div class="plan-desc">
                Deep insights into why employees leave and what to do next.
            </div>
            <div class="price">₹150 / employee / month</div>
            <ul>
                <li>Everything in Standard</li>
                <li>Attrition cost estimation</li>
                <li>Key reason analysis</li>
                <li>Retention recommendations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Select Premium Plan"):
            st.session_state.tier = "premium"
            st.session_state.step = "auth"
            st.rerun()

    # ================= COMPARISON =================
    st.markdown("""
    <div class="compare">
        <h3 style="color:white">Plan Comparison</h3>
        <table style="width:100%;color:#cbd5f5">
            <tr><th>Feature</th><th>Standard</th><th>Premium</th></tr>
            <tr><td>Flight Risk Score</td><td>✔</td><td>✔</td></tr>
            <tr><td>Risk Categories</td><td>✔</td><td>✔</td></tr>
            <tr><td>Retention Recommendations</td><td>✘</td><td>✔</td></tr>
            <tr><td>Attrition Cost Estimation</td><td>✘</td><td>✔</td></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

    # ================= ABOUT US =================
    st.markdown("""
    <div style="margin-top:80px;padding:60px;background:linear-gradient(135deg,#020617,#0f172a);
    border-radius:40px;">
        <h2 style="color:white;text-align:center;font-size:42px;">About StaySmart AI</h2>
        <p style="color:#c7d2fe;text-align:center;font-size:18px;max-width:900px;margin:auto;">
        StaySmart AI helps organizations predict employee attrition, reduce risk,
        and make confident HR decisions using machine learning insights.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.stop()

# =================================================
# =============== STEP 2: AUTH =====================
# =================================================
if st.session_state.step == "auth":

    key = st.text_input("Enter License Key", type="password")

    if st.button("Verify & Open Dashboard"):
        if key.strip().upper() in [k.upper() for k in LICENSE_KEYS[st.session_state.tier]]:
            st.session_state.authenticated = True
            st.session_state.step = "dashboard"
            st.rerun()
        else:
            st.error("Invalid license key")

    st.stop()

# =================================================
# =============== STEP 3: DASHBOARD ================
# =================================================
if not st.session_state.authenticated:
    st.stop()

st.title("StaySmart AI Dashboard")

file = st.file_uploader("Upload Employee CSV", type=["csv"])
if not file:
    st.stop()

df = pd.read_csv(file)
df.columns = df.columns.str.lower().str.replace(" ", "_")

required = ['satisfaction_score','engagement_score','last_hike_months','overtime_hours','distance_from_home']
for c in required:
    if c not in df:
        df[c] = np.random.randint(1,10,len(df))

risk = (10-df['satisfaction_score'])*0.3 + (10-df['engagement_score'])*0.3
df['risk'] = risk

st.write(df.head())
