# -*- coding: utf-8 -*-
"""StaySmart AI – Enterprise HR Intelligence Platform"""

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
    "standard": ["SSAI-STD-A9F4-KP72-QM81"],
    "premium": ["SSAI-PRM-X8LQ-4R2Z-M9KP"]
}

# ================= GLOBAL STYLES =================
st.markdown("""
<style>
body { background:#0b1220; }

.hero {
    text-align:center;
    padding:80px 20px 40px;
}

.hero h1 {
    font-size:54px;
    font-weight:800;
    color:white;
}

.hero p {
    font-size:20px;
    color:#c7d2fe;
}

.card {
    background:rgba(255,255,255,0.95);
    padding:40px;
    border-radius:26px;
    box-shadow:0 25px 60px rgba(0,0,0,0.35);
    height:100%;
}

.price {
    font-size:42px;
    font-weight:800;
}

.badge {
    padding:8px 18px;
    border-radius:20px;
    font-weight:600;
    display:inline-block;
}

.standard { background:#e0f2fe; color:#0369a1; }
.premium { background:#fff7ed; color:#c2410c; }

.req {
    background:#0f172a;
    color:#e5e7eb;
    padding:25px;
    border-radius:18px;
    margin-top:25px;
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
        <div class="card">
            <span class="badge standard">STANDARD</span>
            <h2>HR Risk Monitoring</h2>
            <p class="price">₹100 <span style="font-size:16px">/ employee / month</span></p>
            <ul>
                <li>Employee attrition risk scoring</li>
                <li>High / Medium / Low risk classification</li>
                <li>Top risk employee dashboard</li>
                <li>Basic visual analytics</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Select Standard Plan"):
            st.session_state.tier = "standard"
            st.session_state.step = "auth"
            st.rerun()

    with col2:
        st.markdown("""
        <div class="card">
            <span class="badge premium">PREMIUM</span>
            <h2>Predictive HR Intelligence</h2>
            <p class="price">₹150 <span style="font-size:16px">/ employee / month</span></p>
            <ul>
                <li>Everything in Standard</li>
                <li>Attrition cost exposure</li>
                <li>Key driver importance</li>
                <li>Actionable retention strategies</li>
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

    plan = st.session_state.tier
    price = "₹100 / employee / month" if plan == "standard" else "₹150 / employee / month"

    st.markdown(f"""
    <div class="card" style="max-width:600px;margin:auto;">
        <span class="badge {'standard' if plan=='standard' else 'premium'}">
            {plan.upper()} PLAN
        </span>
        <p style="margin-top:10px;font-weight:600">{price}</p>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="req">
    <h4>📄 Required Employee Data Columns</h4>
    <ul>
        <li>Satisfaction Score (1–10)</li>
        <li>Engagement Score (1–10)</li>
        <li>Months Since Last Salary Hike</li>
        <li>Overtime Hours per Month</li>
        <li>Distance from Home (km)</li>
    </ul>
    <p style="font-size:14px;color:#94a3b8">
    Missing values will be intelligently estimated for analysis.
    </p>
    </div>
    """, unsafe_allow_html=True)

    key = st.text_input(
        "Enter License Key",
        placeholder="SSAI-XXXX-XXXX-XXXX",
        type="password"
    )

    if st.button("Verify & Open Dashboard"):
        if key in LICENSE_KEYS[plan]:
            st.session_state.authenticated = True
            st.session_state.step = "dashboard"
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

tier = st.session_state.tier

st.markdown("""
<div style="background:linear-gradient(135deg,#4f46e5,#7c3aed);
padding:40px;border-radius:28px;margin-bottom:30px">
<h1 style="color:white;">StaySmart AI Dashboard</h1>
<p style="color:#e0e7ff;font-size:18px">
AI-powered employee attrition intelligence
</p>
</div>
""", unsafe_allow_html=True)

st.markdown(
    f"<span class='badge {'standard' if tier=='standard' else 'premium'}'>"
    f"{'Standard' if tier=='standard' else 'Premium'} Active</span>",
    unsafe_allow_html=True
)

# ================= FILE UPLOAD =================
file = st.file_uploader("📂 Upload Employee CSV", type=["csv"])
if not file:
    st.info("Upload employee data to begin analysis")
    st.stop()

df = pd.read_csv(file)
df.columns = df.columns.str.lower().str.replace(" ", "_")

required_cols = {
    'satisfaction_score': (1, 10),
    'engagement_score': (1, 10),
    'last_hike_months': (0, 36),
    'overtime_hours': (0, 80),
    'distance_from_home': (1, 40)
}

for col, (low, high) in required_cols.items():
    if col not in df.columns:
        df[col] = np.clip(np.random.normal((low+high)/2, 2, len(df)), low, high)

risk_score = (
    (10 - df['satisfaction_score']) * 0.30 +
    (10 - df['engagement_score']) * 0.30 +
    (df['last_hike_months'] / 36) * 10 * 0.20 +
    (df['overtime_hours'] / 80) * 10 * 0.10 +
    (df['distance_from_home'] / 40) * 10 * 0.10
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

if tier == "premium":
    st.metric("Estimated Attrition Cost", f"₹{(df['risk_category']=='High').sum()*5:.1f} Lakhs")

# ================= CHART =================
st.markdown("## 📊 Risk Distribution")
fig, ax = plt.subplots()
df['risk_category'].value_counts().plot(kind="bar", ax=ax)
st.pyplot(fig)

# ================= PREMIUM =================
if tier == "premium":
    st.markdown("## 🧠 Key Attrition Drivers")
    imp = pd.Series(model.feature_importances_, index=X.columns).sort_values()
    fig2, ax2 = plt.subplots()
    imp.plot(kind="barh", ax=ax2)
    st.pyplot(fig2)

st.download_button(
    "⬇️ Download Full Analysis",
    df.to_csv(index=False),
    "staysmart_ai_report.csv"
)
