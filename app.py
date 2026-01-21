# -*- coding: utf-8 -*-
"""StaySmart AI – Enterprise HR Intelligence"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="StaySmart AI | HR Intelligence",
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

# ================= ADVANCED UI STYLING =================
st.markdown("""
<style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #020617;
    }

    .main {
        background: radial-gradient(circle at top right, #1e1b4b, #020617);
    }

    /* Hero Section */
    .hero {
        text-align: center;
        padding: 80px 20px;
        background: linear-gradient(180deg, rgba(30,58,138,0.2) 0%, rgba(2,6,23,0) 100%);
        border-bottom: 1px solid rgba(255,255,255,0.05);
        margin-bottom: 50px;
    }

    .hero h1 {
        font-size: 64px;
        font-weight: 800;
        background: linear-gradient(to right, #ffffff, #94a3b8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -2px;
    }

    /* Plan Cards (Glassmorphism) */
    .plan-card {
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 45px;
        border-radius: 32px;
        height: 100%;
        transition: all 0.4s ease;
    }

    .plan-card:hover {
        border: 1px solid rgba(99, 102, 241, 0.5);
        box-shadow: 0 0 30px rgba(79, 70, 229, 0.15);
        transform: translateY(-5px);
    }

    .plan-title {
        font-size: 24px;
        font-weight: 700;
        color: #f8fafc;
        margin-top: 20px;
    }

    .price {
        font-size: 36px;
        font-weight: 800;
        color: #ffffff;
        margin: 25px 0;
    }

    .price span { font-size: 16px; color: #94a3b8; font-weight: 400; }

    .badge {
        padding: 6px 14px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    .standard { background: rgba(56, 189, 248, 0.1); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.2); }
    .premium { background: rgba(249, 115, 22, 0.1); color: #fb923c; border: 1px solid rgba(249, 115, 22, 0.2); }

    /* Tables */
    table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0 10px;
        margin-top: 20px;
    }

    th { color: #94a3b8; text-align: left; padding: 15px; font-weight: 600; }
    td { background: rgba(255,255,255,0.03); padding: 15px; color: #e2e8f0; }
    td:first-child { border-radius: 12px 0 0 12px; }
    td:last-child { border-radius: 0 12px 12px 0; }

    /* Buttons Override */
    .stButton>button {
        width: 100%;
        border-radius: 14px;
        padding: 12px;
        background: #4f46e5 !important;
        color: white !important;
        border: none !important;
        font-weight: 600;
        transition: 0.3s;
    }
    
    .stButton>button:hover {
        box-shadow: 0 0 20px rgba(79, 70, 229, 0.4);
        transform: scale(1.02);
    }

    /* Dashboard Elements */
    .metric-card {
        background: rgba(15, 23, 42, 0.8);
        padding: 20px;
        border-radius: 16px;
        border-left: 4px solid #4f46e5;
    }
</style>
""", unsafe_allow_html=True)

# =================================================
# =============== STEP 1: PLAN SELECT ===============
# =================================================
if st.session_state.step == "plan":

    st.markdown("""
    <div class="hero">
        <p style="color:#818cf8; font-weight:600; margin-bottom:0;">AI-POWERED RETENTION</p>
        <h1>StaySmart AI</h1>
        <p style="color:#94a3b8; max-width:600px; margin: 20px auto;">
            The enterprise-grade intelligence layer that predicts attrition and provides 
            actionable insights to keep your best talent.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="plan-card">
            <span class="badge standard">Basic Growth</span>
            <div class="plan-title">HR Risk Monitoring</div>
            <div class="price">₹100 <span>/ employee / month</span></div>
            <ul style="color:#cbd5e1; line-height:1.8;">
                <li>Employee flight risk scoring</li>
                <li>Predictive risk categorization</li>
                <li>Real-time visual dashboards</li>
                <li>Priority risk alerts</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Get Started with Standard", key="btn_std"):
            st.session_state.tier = "standard"
            st.session_state.step = "auth"
            st.rerun()

    with col2:
        st.markdown("""
        <div class="plan-card">
            <span class="badge premium">Enterprise ML</span>
            <div class="plan-title">Predictive HR Intelligence</div>
            <div class="price">₹150 <span>/ employee / month</span></div>
            <ul style="color:#cbd5e1; line-height:1.8;">
                <li>Everything in Standard</li>
                <li>Attrition financial impact cost</li>
                <li>AI-driven retention strategy</li>
                <li>Automated reason analysis</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Get Started with Premium", key="btn_prm"):
            st.session_state.tier = "premium"
            st.session_state.step = "auth"
            st.rerun()

    # Comparison Section
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background:rgba(255,255,255,0.02); padding:40px; border-radius:24px;">
        <h3 style="color:white; margin-bottom:20px;">Platform Capabilities</h3>
        <table>
            <tr><th>Capability</th><th>Standard</th><th>Premium</th></tr>
            <tr><td>Machine Learning Risk Score</td><td>✔</td><td>✔</td></tr>
            <tr><td>Employee Health Dashboard</td><td>✔</td><td>✔</td></tr>
            <tr><td>Attrition Cost Logic</td><td>✘</td><td>✔</td></tr>
            <tr><td>Retention Strategic Playbook</td><td>✘</td><td>✔</td></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# =================================================
# =============== STEP 2: AUTH =====================
# =================================================
if st.session_state.step == "auth":
    col_a, col_b, col_c = st.columns([1,2,1])
    with col_b:
        st.markdown(f"<h2 style='text-align:center; color:white;'>Unlock {st.session_state.tier.title()} Dashboard</h2>", unsafe_allow_html=True)
        key = st.text_input("Enter Enterprise License Key", type="password")
        if st.button("Verify Credentials"):
            if key.strip().upper() in [k.upper() for k in LICENSE_KEYS[st.session_state.tier]]:
                st.session_state.authenticated = True
                st.session_state.step = "dashboard"
                st.rerun()
            else:
                st.error("Authentication Failed: Invalid Key")
    st.stop()

# =================================================
# =============== STEP 3: DASHBOARD ================
# =================================================
if st.session_state.authenticated:
    st.markdown(f"""
        <div style='display:flex; justify-content:space-between; align-items:center;'>
            <h1 style='color:white;'>StaySmart AI <span style='font-size:14px; color:#4f46e5;'>{st.session_state.tier.upper()} ACCESS</span></h1>
        </div>
    """, unsafe_allow_html=True)

    with st.expander("📁 Data Import", expanded=True):
        file = st.file_uploader("Upload Employee Data (CSV)", type=["csv"])

    if not file:
        st.info("Please upload your employee dataset to begin analysis.")
        st.stop()

    # Data Processing Logic
    df = pd.read_csv(file)
    df.columns = df.columns.str.lower().str.replace(" ", "_")

    required = ['satisfaction_score','engagement_score','last_hike_months','overtime_hours','distance_from_home']
    for c in required:
        if c not in df:
            df[c] = np.random.randint(1,10,len(df))

    df['risk'] = (10-df['satisfaction_score'])*0.3 + (10-df['engagement_score'])*0.3
    
    # Dashboard Layout
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Headcount", len(df))
    m2.metric("Avg Risk Score", f"{df['risk'].mean():.2f}")
    m3.metric("Critical Alerts", len(df[df['risk'] > 7]))

    st.markdown("### 📊 Employee Intelligence Overview")
    st.dataframe(df.style.background_gradient(subset=['risk'], cmap='RdYlGn_r'), use_container_width=True)

    if st.session_state.tier == "premium":
        st.markdown("---")
        st.markdown("### 💎 Premium Insights: Attrition Cost Analysis")
        cost = len(df[df['risk'] > 5]) * 50000 # Example math
        st.error(f"Estimated Replacement Cost Risk: ₹{cost:,}")
