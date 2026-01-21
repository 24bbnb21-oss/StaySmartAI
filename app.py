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

.compare table {
    width:100%;
    border-collapse:collapse;
}

.compare th, .compare td {
    border:1px solid #334155;
    padding:10px;
    text-align:center;
    color:#cbd5f5;
}

.compare th {
    background:#111827;
    color:#fff;
}

.check { color:#34d399; font-weight:700; }
.cross { color:#fca5a5; font-weight:700; }

/* === Glow Animation === */
@keyframes softGlow {
    0% {
        box-shadow:0 0 25px rgba(99,102,241,0.25),
                   0 0 60px rgba(124,58,237,0.15);
        transform:translateY(0);
    }
    50% {
        box-shadow:0 0 45px rgba(99,102,241,0.45),
                   0 0 90px rgba(124,58,237,0.30);
        transform:translateY(-4px);
    }
    100% {
        box-shadow:0 0 25px rgba(99,102,241,0.25),
                   0 0 60px rgba(124,58,237,0.15);
        transform:translateY(0);
    }
}

.glow {
    animation:softGlow 4s ease-in-out infinite;
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
        <div class="plan-card glow">
            <span class="badge standard">STANDARD</span>
            <div class="plan-title">HR Risk Monitoring</div>
            <div class="plan-desc">
                Identify employees who may leave and monitor risk levels.
            </div>
            <div class="price">₹100 <span style="font-size:16px">/ employee / month</span></div>
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
        <div class="plan-card glow">
            <span class="badge premium">PREMIUM</span>
            <div class="plan-title">Predictive HR Intelligence</div>
            <div class="plan-desc">
                Deep insights into why employees leave and what to do next.
            </div>
            <div class="price">₹150 <span style="font-size:16px">/ employee / month</span></div>
            <ul>
                <li>Everything in Standard</li>
                <li>Attrition cost estimation</li>
                <li>Key reason analysis</li>
                <li>Retention recommendations</li>
                <li>Leadership-ready insights</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Select Premium Plan"):
            st.session_state.tier = "premium"
            st.session_state.step = "auth"
            st.rerun()

    st.markdown("""
    <div class="compare glow">
        <h3 style="color:white;">Plan Comparison</h3>
        <table>
            <tr><th>Feature</th><th>Standard</th><th>Premium</th></tr>
            <tr><td>Flight Risk Score</td><td class="check">✔</td><td class="check">✔</td></tr>
            <tr><td>Risk Categories</td><td class="check">✔</td><td class="check">✔</td></tr>
            <tr><td>Retention Recommendations</td><td class="cross">✘</td><td class="check">✔</td></tr>
            <tr><td>Attrition Cost Estimation</td><td class="cross">✘</td><td class="check">✔</td></tr>
            <tr><td>Leadership Insights</td><td class="cross">✘</td><td class="check">✔</td></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

    # ===== ABOUT US =====
    st.markdown("""
    <div style="margin-top:80px;padding:60px;border-radius:30px;
    background:linear-gradient(135deg,#020617,#0f172a);
    box-shadow:0 0 80px rgba(79,70,229,0.25);">
        <h2 style="color:white;font-size:38px;font-weight:800;">About StaySmart AI</h2>
        <p style="color:#c7d2fe;font-size:18px;max-width:900px;">
        StaySmart AI is an enterprise-grade HR intelligence platform that helps
        organizations predict attrition, reduce people risk, and retain talent proactively.
        </p>
        <p style="color:#94a3b8;font-size:16px;max-width:900px;">
        Powered by machine learning, StaySmart AI turns raw employee data into
        leadership-ready insights — enabling HR teams to act before attrition happens.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.stop()

# =================================================
# =============== STEP 2 & 3 (UNCHANGED) ===========
# =================================================
# Everything below remains EXACTLY as your working version
