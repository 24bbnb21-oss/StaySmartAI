# -*- coding: utf-8 -*-
"""StaySmart AI – Enterprise HR Intelligence (Restored Logic + Pro UI)"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px # Added for better visuals

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
/* Modern Dark Theme */
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at 50% -20%, #1e293b, #020617);
}

/* Hero Section */
.hero { text-align:center; padding:60px 0; }
.hero h1 {
    font-size: 55px; font-weight: 800;
    background: linear-gradient(90deg, #fff, #94a3b8);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero p { color: #94a3b8; font-size: 1.2rem; }

/* Plan Cards - Glassmorphism */
.plan-card {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    padding: 35px;
    border-radius: 25px;
    transition: 0.4s;
}
.plan-card:hover {
    border-color: #6366f1;
    box-shadow: 0 0 25px rgba(99, 102, 241, 0.2);
}

.price { font-size: 32px; font-weight: 800; color: #fff; margin: 15px 0; }
.badge {
    padding: 5px 12px; border-radius: 8px; font-weight: 700; font-size: 12px;
}
.standard-badge { background: #0ea5e922; color: #0ea5e9; border: 1px solid #0ea5e944; }
.premium-badge { background: #f59e0b22; color: #f59e0b; border: 1px solid #f59e0b44; }

/* Buttons */
.stButton button {
    border-radius: 12px; width: 100%; font-weight: 600; padding: 10px;
    background: #6366f1 !important; color: white !important; border: none !important;
}

/* Compare Table */
.compare-container {
    background: rgba(0,0,0,0.2); border-radius: 20px; padding: 30px; margin-top: 40px;
}
</style>
""", unsafe_allow_html=True)

# =================================================
# =============== STEP 1: PLAN SELECT ===============
# =================================================
if st.session_state.step == "plan":
    st.markdown('<div class="hero"><h1>StaySmart AI</h1><p>Predict Attrition • Reduce Risk • Retain Talent</p></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="plan-card">
            <span class="badge standard-badge">STANDARD</span>
            <h2 style="color:white; margin-top:10px;">HR Risk Monitoring</h2>
            <p style="color:#94a3b8;">Identify employees who may leave and monitor risk levels.</p>
            <div class="price">₹100 <span style="font-size:16px; color:#64748b;">/ employee / month</span></div>
            <ul style="color:#cbd5e1; font-size:14px;">
                <li>Employee flight risk score</li>
                <li>High / Medium / Low risk tags</li>
                <li>Top risk employees list</li>
                <li>Visual Risk Dashboards</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Select Standard Plan", key="sel_std"):
            st.session_state.tier = "standard"
            st.session_state.step = "auth"
            st.rerun()

    with col2:
        st.markdown("""
        <div class="plan-card">
            <span class="badge premium-badge">PREMIUM</span>
            <h2 style="color:white; margin-top:10px;">Predictive HR Intelligence</h2>
            <p style="color:#94a3b8;">Deep insights into why employees leave and what to do next.</p>
            <div class="price">₹150 <span style="font-size:16px; color:#64748b;">/ employee / month</span></div>
            <ul style="color:#cbd5e1; font-size:14px;">
                <li>Everything in Standard</li>
                <li>Attrition cost estimation</li>
                <li>Key reason analysis</li>
                <li>Retention recommendations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Select Premium Plan", key="sel_prm"):
            st.session_state.tier = "premium"
            st.session_state.step = "auth"
            st.rerun()

    st.markdown("""
    <div class="compare-container">
        <h3 style="color:white; margin-bottom:20px;">Feature Comparison</h3>
        <table style="width:100%; color:#94a3b8;">
            <tr style="border-bottom:1px solid #334155;"><th style="text-align:left;">Feature</th><th>Standard</th><th>Premium</th></tr>
            <tr><td>Flight Risk Score</td><td>✔</td><td>✔</td></tr>
            <tr><td>Retention Recommendations</td><td>✘</td><td>✔</td></tr>
            <tr><td>Financial Risk Impact</td><td>✘</td><td>✔</td></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# =================================================
# =============== STEP 2: AUTH =====================
# =================================================
if st.session_state.step == "auth":
    col_x, col_y, col_z = st.columns([1,2,1])
    with col_y:
        st.markdown(f"<h3 style='text-align:center; color:white;'>Enter {st.session_state.tier.upper()} License</h3>", unsafe_allow_html=True)
        key = st.text_input("License Key", type="password")
        if st.button("Unlock Dashboard"):
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
if st.session_state.authenticated:
    st.title("StaySmart AI Dashboard")
    
    file = st.file_uploader("Upload Employee Data (CSV)", type=["csv"])
    if not file:
        st.info("Awaiting CSV upload...")
        st.stop()

    df = pd.read_csv(file)
    df.columns = df.columns.str.lower().str.replace(" ", "_")

    # Data Simulation logic
    required = ['satisfaction_score','engagement_score','last_hike_months','overtime_hours','distance_from_home','salary']
    for c in required:
        if c not in df:
            if 'salary' in c: df[c] = np.random.randint(30000, 150000, len(df))
            else: df[c] = np.random.randint(1,10,len(df))

    # Risk Math
    df['risk'] = ((10-df['satisfaction_score'])*0.4 + (df['overtime_hours']*0.2) + (10-df['engagement_score'])*0.4).clip(0,10)
    
    # Visuals
    c1, c2, c3 = st.columns(3)
    c1.metric("Headcount", len(df))
    c2.metric("High Risk Staff", len(df[df['risk'] > 7]))
    c3.metric("Avg Engagement", f"{df['engagement_score'].mean():.1f}/10")

    # Chart Area
    st.markdown("### 📈 Risk Distribution")
    fig = px.histogram(df, x="risk", nbins=20, color_discrete_sequence=['#6366f1'])
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 📋 Employee Risk Table")
    st.dataframe(df[['satisfaction_score', 'engagement_score', 'risk']].style.background_gradient(cmap='RdYlGn_r'), use_container_width=True)

    # ================= PREMIUM INSIGHTS =================
    if st.session_state.tier == "premium":
        st.markdown("---")
        st.markdown("### 💎 Executive Intelligence (Premium)")
        
        # Attrition Cost Logic
        avg_salary = df['salary'].mean()
        high_risk_count = len(df[df['risk'] > 7])
        potential_loss = high_risk_count * (avg_salary * 0.5) # 50% of salary as turnover cost
        
        p1, p2 = st.columns(2)
        with p1:
            st.error(f"Financial Risk Exposure: ₹{potential_loss:,.0f}")
            st.write("Calculated based on 50% of annual salary for high-risk individuals.")
        
        with p2:
            st.markdown("**Core Attrition Drivers:**")
            st.warning("1. High Overtime Hours\n2. Low Engagement Score\n3. Tenure vs Market Pay")

        st.markdown("### 🛠 Retention Recommendations")
        rec_col1, rec_col2 = st.columns(2)
        with rec_col1:
            st.success("**Immediate Actions**")
            st.write("* Initiate stay-interviews for Top 10 High-Risk staff.\n* Review workload for departments with >8 overtime hours.")
        with rec_col2:
            st.success("**Strategic Moves**")
            st.write("* Adjust Hike cycles for employees under-market.\n* Launch Engagement Program for remote staff.")

    else:
        st.info("💡 Upgrade to Premium to see Attrition Cost Analysis and Retention Recommendations.")

    if st.button("Log Out"):
        st.session_state.step = "plan"
        st.session_state.authenticated = False
        st.rerun()
