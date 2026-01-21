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
    animation: fadeIn 1s ease-in-out;
}

.hero p {
    font-size:20px;
    color:#c7d2fe;
    animation: fadeIn 2s ease-in-out;
}

.plan-card {
    background:#ffffff;
    padding:40px;
    border-radius:28px;
    box-shadow:0 30px 70px rgba(0,0,0,0.35);
    height:100%;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.plan-card:hover {
    transform: translateY(-10px);
    box-shadow:0 40px 90px rgba(0,0,0,0.45);
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
    animation: fadeIn 1.5s ease-in-out;
}

.req-box h4 {
    margin-bottom:10px;
}

.req-box li {
    color:#cbd5f5;
}

.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #0b1220;
    color: #c7d2fe;
    text-align: center;
    padding: 12px;
    font-size: 14px;
    opacity: 0.8;
}

@keyframes fadeIn {
    0% { opacity: 0; transform: translateY(20px); }
    100% { opacity: 1; transform: translateY(0); }
}
</style>
""", unsafe_allow_html=True)

# ================= SIDEBAR NAV =================
st.sidebar.title("StaySmart AI")
st.sidebar.write("Enterprise HR Intelligence")

nav = st.sidebar.radio(
    "Navigate",
    ["Home", "Dashboard", "About"],
    index=["Home", "Dashboard", "About"].index(st.session_state.nav)
)
st.session_state.nav = nav

# 👉 Auto-switch to Dashboard after login
if st.session_state.step == "dashboard":
    st.session_state.nav = "Dashboard"

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
        <div class="plan-card">
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

    st.stop()

# =================================================
# =============== STEP 2: AUTH =====================
# =================================================
if st.session_state.step == "auth":

    tier = st.session_state.tier
    price = "₹100 / employee / month" if tier == "standard" else "₹150 / employee / month"

    st.markdown(f"""
    <div class="plan-card" style="max-width:620px;margin:auto;">
        <span class="badge {'standard' if tier=='standard' else 'premium'}">
            {tier.upper()} PLAN
        </span>
        <p style="margin-top:10px;font-weight:600;color:#334155">{price}</p>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="req-box">
        <h4>📄 Employee Data Required</h4>
        <ul>
            <li>Satisfaction Score (1–10)</li>
            <li>Engagement Score (1–10)</li>
            <li>Months since last salary hike</li>
            <li>Overtime hours per month</li>
            <li>Distance from home (km)</li>
        </ul>
        <p style="font-size:14px;color:#94a3b8">
        If some fields are missing, the system will estimate them.
        </p>
    </div>
    """, unsafe_allow_html=True)

    key = st.text_input(
        "Enter License Key",
        placeholder="SSAI-XXXX-XXXX-XXXX",
        type="password"
    )

    if st.button("Verify & Open Dashboard"):
        if key.strip().upper() in [k.upper() for k in LICENSE_KEYS[tier]]:
            st.session_state.authenticated = True
            st.session_state.step = "dashboard"
            st.session_state.nav = "Dashboard"
            st.rerun()
        else:
            st.error("❌ Invalid license key for selected plan")

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# =================================================
# =============== STEP 3: DASHBOARD ================
# =================================================
if not st.session_state.authenticated:
    st.stop()

st.markdown("""
<div style="background:linear-gradient(135deg,#4f46e5,#7c3aed);
padding:40px;border-radius:30px;margin-bottom:30px">
<h1 style="color:white;">StaySmart AI Dashboard</h1>
<p style="color:#e0e7ff;font-size:18px">
AI-powered employee attrition insights
</p>
</div>
""", unsafe_allow_html=True)

# ================= FILE UPLOAD =================
file = st.file_uploader("📂 Upload Employee CSV", type=["csv"])
if not file:
    st.info("Upload employee data to begin analysis")
    st.stop()

df = pd.read_csv(file)
df.columns = df.columns.str.lower().str.replace(" ", "_")

required_cols = {
    'satisfaction_score': (1,10),
    'engagement_score': (1,10),
    'last_hike_months': (0,36),
    'overtime_hours': (0,80),
    'distance_from_home': (1,40)
}

for col,(lo,hi) in required_cols.items():
    if col not in df.columns:
        df[col] = np.clip(np.random.normal((lo+hi)/2,2,len(df)), lo, hi)

risk_score = (
    (10-df['satisfaction_score'])*0.3 +
    (10-df['engagement_score'])*0.3 +
    (df['last_hike_months']/36)*10*0.2 +
    (df['overtime_hours']/80)*10*0.1 +
    (df['distance_from_home']/40)*10*0.1
)

df['left'] = (risk_score > 5.5).astype(int)

X = df[list(required_cols.keys())]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42)
model.fit(X_scaled, df['left'])

df['flight_risk'] = (model.predict_proba(X_scaled)[:,1]*100).round(0)
df['risk_category'] = pd.cut(df['flight_risk'], [0,49,69,100], labels=["Low","Medium","High"])

# ================= METRICS =================
c1,c2,c3 = st.columns(3)
c1.metric("Employees", len(df))
c2.metric("High Risk", int((df['risk_category']=="High").sum()))
c3.metric("Avg Risk", f"{df['flight_risk'].mean():.1f}%")

# ================= RISK SUMMARY =================
st.markdown("""
<div style="background:#0b1220; padding:25px; border-radius:25px; color:white; margin-bottom:20px">
<h2 style="margin:0">🧠 Summary Insights</h2>
<p style="margin:0; color:#cbd5f5">
Based on employee data, your top risk areas are:
</p>
</div>
""", unsafe_allow_html=True)

high = int((df['risk_category']=="High").sum())
med = int((df['risk_category']=="Medium").sum())
low = int((df['risk_category']=="Low").sum())

st.write(f"High Risk: **{high}** employees")
st.write(f"Medium Risk: **{med}** employees")
st.write(f"Low Risk: **{low}** employees")

# ================= CHART =================
st.markdown("## 📊 Risk Distribution")
fig, ax = plt.subplots()
df['risk_category'].value_counts().plot(kind="bar", ax=ax)
st.pyplot(fig)

# ================= PIE CHART =================
st.markdown("## 📈 Risk Breakdown")
fig2, ax2 = plt.subplots()
df['risk_category'].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax2)
ax2.set_ylabel('')
st.pyplot(fig2)

# ================= DATA TABLE =================
st.markdown("## 🧾 Employee Risk Table")
st.dataframe(df.head(10))

# ================= SIMULATOR =================
st.markdown("## 🎛️ Risk Simulator")

satisfaction = st.slider("Satisfaction Score", 1, 10, 5)
engagement = st.slider("Engagement Score", 1, 10, 5)
hike = st.slider("Months since last hike", 0, 36, 12)
ot = st.slider("Overtime hours", 0, 80, 20)
dist = st.slider("Distance from home", 1, 40, 10)

sim_score = (
    (10-satisfaction)*0.3 +
    (10-engagement)*0.3 +
    (hike/36)*10*0.2 +
    (ot/80)*10*0.1 +
    (dist/40)*10*0.1
)

st.write(f"Estimated Flight Risk Score: **{sim_score:.2f}**")

# ================= DOWNLOAD =================
st.download_button(
    "⬇️ Download Full Report",
    df.to_csv(index=False),
    "staysmart_ai_report.csv"
)

# ================= FOOTER =================
st.markdown("""
<div class="footer">
    © 2026 EXQ-16. All rights reserved. • StaySmart AI
</div>
""", unsafe_allow_html=True)
