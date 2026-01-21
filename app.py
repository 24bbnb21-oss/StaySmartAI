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
    page_icon="📊"
)

# ================= SESSION STATE =================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.tier = None

# ================= LICENSE KEYS =================
VALID_KEYS = {
    # Standard – ₹100 / employee / month
    "SSAI-ENT-9F3K-7Q2M-AZ91": "standard",

    # Premium – ₹150 / employee / month
    "SSAI-PRM-X8LQ-4R2Z-M9KP": "premium"
}

# ================= GLOBAL STYLES =================
st.markdown("""
<style>
body { background-color:#f6f8fc; }

.card {
    background:white;
    padding:28px;
    border-radius:18px;
    box-shadow:0 10px 25px rgba(0,0,0,0.08);
    margin-bottom:25px;
}

.login-box {
    max-width:420px;
    margin:140px auto;
    background:white;
    padding:40px;
    border-radius:22px;
    box-shadow:0 16px 40px rgba(0,0,0,0.18);
    text-align:center;
}

.badge {
    display:inline-block;
    padding:8px 18px;
    border-radius:22px;
    font-size:15px;
    font-weight:600;
}

.standard {background:#e8f0fe;color:#1a73e8;}
.premium {background:#fff4e5;color:#d97706;}
</style>
""", unsafe_allow_html=True)

# ================= ACCESS PAGE =================
if not st.session_state.authenticated:

    st.markdown("""
    <div class="login-box">
        <h2>🔐 StaySmart AI</h2>
        <p style="color:#6b7280">
        Enterprise HR Intelligence Platform<br>
        Authorized Access Only
        </p>
    """, unsafe_allow_html=True)

    license_key = st.text_input(
        "License Key",
        placeholder="SSAI-XXXX-XXXX-XXXX",
        type="password"
    )

    if st.button("Verify Access"):
        if license_key in VALID_KEYS:
            st.session_state.authenticated = True
            st.session_state.tier = VALID_KEYS[license_key]
            st.rerun()   # ✅ FIXED
        else:
            st.error("❌ Invalid license key")

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ================= DASHBOARD =================
tier = st.session_state.tier

# ================= HEADER =================
st.markdown("""
<div style="background:linear-gradient(135deg,#4f46e5,#9333ea);
padding:36px;border-radius:22px;margin-bottom:30px">
<h1 style="color:white;">StaySmart AI</h1>
<p style="color:#e0e7ff;font-size:18px">
Predict • Prevent • Retain Talent
</p>
</div>
""", unsafe_allow_html=True)

if tier == "standard":
    st.markdown('<span class="badge standard">🟢 Standard Plan — ₹100 / employee / month</span>', unsafe_allow_html=True)
else:
    st.markdown('<span class="badge premium">👑 Premium Plan — ₹150 / employee / month</span>', unsafe_allow_html=True)

st.markdown("---")

# ================= CSV GUIDE =================
with st.expander("📌 Required CSV Parameters"):
    st.markdown("""
**Mandatory (recommended for accuracy):**
- satisfaction_score (1–10)
- engagement_score (1–10)
- last_hike_months
- overtime_hours
- distance_from_home (km)

**Optional but useful:**
- age
- years_at_company
- salary_lakhs
- work_life_balance (1–5)
""")

# ================= FILE UPLOAD =================
file = st.file_uploader("📂 Upload Employee Dataset", type=["csv"])
if not file:
    st.info("Upload a CSV to continue")
    st.stop()

df = pd.read_csv(file)
df.columns = df.columns.str.lower().str.replace(" ", "_")

# ================= SAFE COLUMN HANDLING =================
required_cols = {
    'satisfaction_score': (1, 10),
    'engagement_score': (1, 10),
    'last_hike_months': (0, 36),
    'overtime_hours': (0, 80),
    'distance_from_home': (1, 40)
}

for col, (low, high) in required_cols.items():
    if col not in df.columns:
        st.warning(f"⚠️ '{col}' not found. Using neutral defaults.")
        df[col] = np.clip(np.random.normal((low+high)/2, 2, len(df)), low, high)

# ================= EXPLAINABLE RISK LOGIC =================
risk_score = (
    (10 - df['satisfaction_score']) * 0.30 +
    (10 - df['engagement_score']) * 0.30 +
    (df['last_hike_months'] / 36) * 10 * 0.20 +
    (df['overtime_hours'] / 80) * 10 * 0.10 +
    (df['distance_from_home'] / 40) * 10 * 0.10
)

df['left'] = (risk_score > 5.5).astype(int)

features = list(required_cols.keys())
X = df[features]
y = df['left']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=6,
    random_state=42
)
model.fit(X_scaled, y)

df['flight_risk'] = (model.predict_proba(X_scaled)[:, 1] * 100).round(0)

df['risk_category'] = pd.cut(
    df['flight_risk'],
    bins=[0, 49, 69, 100],
    labels=["Low Risk", "Medium Risk", "High Risk"]
)

# ================= KPIs =================
c1, c2, c3 = st.columns(3)
c1.metric("Total Employees", len(df))
c2.metric("High Risk Employees", int((df['risk_category']=="High Risk").sum()))
c3.metric("Average Flight Risk", f"{df['flight_risk'].mean():.1f}%")

if tier == "premium":
    estimated_cost = (df['risk_category']=="High Risk").sum() * 500000
    st.metric("Estimated Attrition Exposure", f"₹{estimated_cost/1e7:.2f} Cr")

# ================= VISUAL =================
st.markdown("## 📊 Risk Distribution")
fig, ax = plt.subplots()
df['risk_category'].value_counts().plot(kind="bar", ax=ax)
st.pyplot(fig)

# ================= HIGH RISK TABLE =================
st.markdown("## 🚨 Employees Needing Attention")
st.dataframe(
    df.sort_values("flight_risk", ascending=False).head(10),
    use_container_width=True
)

# ================= PREMIUM INSIGHTS =================
if tier == "premium":
    st.markdown("## 🧠 What’s Driving Attrition")
    importance = pd.Series(
        model.feature_importances_,
        index=features
    ).sort_values()

    fig2, ax2 = plt.subplots()
    importance.plot(kind="barh", ax=ax2)
    st.pyplot(fig2)

    st.markdown("""
**Recommended Actions:**
- Prioritize employees with low engagement + high overtime  
- Address delayed salary hikes  
- Reduce commute burden where possible  
- Initiate manager check-ins for top 10% risk
""")

# ================= EXPORT =================
st.download_button(
    "⬇️ Download Full Analysis",
    df.to_csv(index=False),
    "staysmart_ai_report.csv"
)
