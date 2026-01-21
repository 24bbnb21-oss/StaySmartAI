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

.badge {
    padding:8px 18px;
    border-radius:20px;
    font-weight:700;
    display:inline-block;
}

.standard { background:#e0f2fe; color:#0369a1; }
.premium { background:#fff7ed; color:#c2410c; }

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
            <h3>HR Risk Monitoring</h3>
            <p>Identify employees who may leave and monitor risk levels.</p>
            <h2>₹100 / employee / month</h2>
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
            <h3>Predictive HR Intelligence</h3>
            <p>Deep insights into why employees leave and what to do next.</p>
            <h2>₹150 / employee / month</h2>
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

    # ================= ABOUT US (ENHANCED) =================
    st.markdown("""
    <div style="margin-top:90px;padding:70px;
    background:linear-gradient(135deg,#020617,#0f172a,#1e1b4b);
    border-radius:45px;">
        
        <h2 style="color:white;text-align:center;font-size:44px;">
            About StaySmart AI
        </h2>

        <p style="color:#c7d2fe;text-align:center;font-size:18px;
        max-width:1000px;margin:25px auto;">
            StaySmart AI is an enterprise-grade HR intelligence platform designed
            to help organizations predict employee attrition before it happens.
        </p>

        <p style="color:#94a3b8;text-align:center;font-size:17px;
        max-width:1000px;margin:auto;">
            By combining behavioral indicators, engagement metrics, and machine
            learning models, StaySmart AI delivers clear, actionable insights
            that empower HR leaders to reduce turnover, protect talent, and
            drive long-term workforce stability.
        </p>

        <div style="display:flex;justify-content:center;gap:40px;margin-top:40px;">
            <div style="color:#e0e7ff;font-size:16px;">🔍 Predict Risk</div>
            <div style="color:#e0e7ff;font-size:16px;">📊 Analyze Patterns</div>
            <div style="color:#e0e7ff;font-size:16px;">🤝 Retain Talent</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ================= FOOTER =================
    st.markdown("""
    <div style="text-align:center;margin-top:50px;
    color:#94a3b8;font-size:14px;">
        © 2026 StaySmart AI. All Rights Reserved. <br>
        Team Code: <strong>EXQ-16</strong>
    </div>
    """, unsafe_allow_html=True)

    st.stop()
