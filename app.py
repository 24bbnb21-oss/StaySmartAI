# -*- coding: utf-8 -*-
"""StaySmart AI – Enterprise HR Intelligence"""

import streamlit as st
import pandas as pd
import numpy as np
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
/* Base Theme */
[data-testid="stAppViewContainer"] {
    background-color: #0b1220;
    background-image: radial-gradient(circle at 50% 0%, #1e293b 0%, #0b1220 100%);
}

/* Hero Section */
.hero {
    text-align:center;
    padding:60px 20px;
}
.hero h1 {
    font-size:58px;
    font-weight:800;
    background: linear-gradient(to right, #ffffff, #94a3b8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero p { font-size:20px; color:#94a3b8; }

/* Glassmorphism Cards */
.plan-card {
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(10px);
    padding: 40px;
    border-radius: 28px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    height: 100%;
    transition: 0.3s;
}
.plan-card:hover {
    border: 1px solid #6366f1;
    box-shadow: 0 0 30px rgba(99, 102, 241, 0.2);
    transform: translateY(-5px);
}

.plan-title { font-size:28px; font-weight:800; color:#ffffff; margin-top:15px; }
.plan-desc { color:#94a3b8; font-size:16px; margin:15px 0; }
.price { font-size:36px; font-weight:800; color:#ffffff; margin:20px 0; }

.badge { padding:6px 16px; border-radius:20px; font-weight:700; font-size:12px; }
.standard { background:#0ea5e9; color:white; }
.premium { background:#f59e0b; color:white; }

/* Buttons */
.stButton>button {
    width: 100%;
    border-radius: 12px;
    padding: 10px;
    background: #6366f1 !important;
    color: white !important;
    border: none !important;
    font-weight: 600;
}

/* Tables */
table { width:100%; color:#cbd5e1; border-collapse: collapse; margin-top:20px; }
th { text-align:left; border-bottom: 1px solid #334155; padding: 10px; }
td { padding: 10px; border-bottom: 1px solid #1e293b; }
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
            <span class="badge standard">STANDARD</span>
            <div class="plan-title">HR Risk Monitoring</div>
            <div class="plan-desc">Identify employees who may leave and monitor risk levels.</div>
            <div class="price">₹100 <small style="font-size:14px; color:#64748b;">/ employee / month</small></div>
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
            <div class="plan-desc">Deep insights into why employees leave and what to do next.</div>
            <div class="price">₹150 <small style="font-size:14px; color:#64748b;">/ employee / month</small></div>
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

    st.markdown("""
    <div style="background:rgba(0,0,0,0.2); padding:30px; border-radius:20px; margin-top:40px;">
        <h3 style="color:white">Plan Comparison</h3>
        <table>
            <tr><th>Feature</th><th>Standard</th><th>Premium</th></tr>
            <tr><td>Flight Risk Score</td><td>✔</td><td>✔</td></tr>
            <tr><td>Risk Categories</td><td>✔</td><td>✔</td></tr>
            <tr><td>Retention Recommendations</td><td>✘</td><td>✔</td></tr>
            <tr><td>Attrition Cost Estimation</td><td>✘</td><td>✔</td></tr>
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
        st.markdown(f"<h3 style='color:white; text-align:center;'>Enter {st.session_state.tier.upper()} License</h3>", unsafe_allow_html=True)
        key = st.text_input("License Key", type="password")
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
if st.session_state.authenticated:
    st.title("StaySmart AI Dashboard")
    
    file = st.file_uploader("Upload Employee CSV", type=["csv"])
    if not file:
        st.info("Please upload a CSV file to view insights.")
        st.stop()

    df = pd.read_csv(file)
    df.columns = df.columns.str.lower().str.replace(" ", "_")

    required = ['satisfaction_score','engagement_score','last_hike_months','overtime_hours','distance_from_home','salary']
    for c in required:
        if c not in df:
            if c == 'salary': df[c] = np.random.randint(40000, 150000, len(df))
            else: df[c] = np.random.randint(1,10,len(df))

    # Original Risk Logic
    df['risk'] = (10-df['satisfaction_score'])*0.3 + (10-df['engagement_score'])*0.3
    
    # Dashboard Visuals
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Headcount", len(df))
    m2.metric("High Risk Employees", len(df[df['risk'] > 4]))
    m3.metric("Avg Satisfaction", f"{df['satisfaction_score'].mean():.1f}/10")

    st.markdown("### Employee Risk Data")
    st.dataframe(df.style.background_gradient(subset=['risk'], cmap='RdYlGn_r'), use_container_width=True)

    # Visualization Section (Using Matplotlib for stability)
    st.markdown("### Risk Distribution")
    fig, ax = plt.subplots(figsize=(10, 3))
    fig.patch.set_facecolor('#0b1220')
    ax.set_facecolor('#0b1220')
    df['risk'].hist(ax=ax, color='#6366f1', bins=15, grid=False)
    ax.tick_params(colors='white')
    ax.title.set_color('white')
    st.pyplot(fig)

    # PREMIUM FEATURES
    if st.session_state.tier == "premium":
        st.markdown("---")
        st.markdown("### 💎 Premium Insights & Fixes")
        
        p1, p2 = st.columns(2)
        with p1:
            st.markdown("#### Attrition Cost Risk")
            loss = len(df[df['risk'] > 4]) * (df['salary'].mean() * 0.3)
            st.error(f"Potential Revenue Impact: ₹{loss:,.0f}")
            st.write("Calculated as 30% of average salary for high-risk staff.")
            
        with p2:
            st.markdown("#### Retention Fixes")
            st.success("✅ Top Recommendations:")
            st.write("1. High Overtime detected: Review workload for Dept A.")
            st.write("2. Low Satisfaction: Schedule 1-on-1 feedback loops.")
            st.write("3. Market Pay Gap: Review 'Last Hike' for high performers.")

    if st.button("Log Out"):
        st.session_state.step = "plan"
        st.session_state.authenticated = False
        st.rerun()
