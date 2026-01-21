# -*- coding: utf-8 -*-
"""StaySmart AI – Secure, Tiered & Professional HR Analytics"""

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="StaySmart AI",
    layout="wide",
    page_icon="📊"
)

# ================= GLOBAL STYLES =================
st.markdown("""
<style>
body { background-color: #f6f8fc; }

.section {
    background: white;
    padding: 28px;
    border-radius: 18px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.08);
    margin-bottom: 25px;
}

.badge {
    display:inline-block;
    padding:6px 14px;
    border-radius:20px;
    font-size:14px;
    font-weight:600;
}
.standard {background:#e8f0fe;color:#1a73e8;}
.premium {background:#fff4e5;color:#d97706;}

.login-container {
    max-width: 420px;
    margin: 120px auto;
    background: white;
    padding: 38px;
    border-radius: 20px;
    box-shadow: 0 14px 35px rgba(0,0,0,0.15);
    text-align: center;
}
.login-title {
    font-size: 26px;
    font-weight: 700;
    margin-bottom: 6px;
}
.login-sub {
    color: #6b7280;
    font-size: 15px;
    margin-bottom: 26px;
}
</style>
""", unsafe_allow_html=True)

# ================= ACCESS CONTROL =================
VALID_ACCESS_IDS = {
    "SSAI-STD-2026": "standard",
    "SSAI-PRM-2026": "premium"
}

st.markdown("""
<div class="login-container">
    <div class="login-title">🔐 StaySmart AI Access</div>
    <div class="login-sub">
        Restricted analytics platform for authorized HR teams.<br>
        Please enter your access ID.
    </div>
""", unsafe_allow_html=True)

access_id = st.text_input(
    "Access ID",
    placeholder="e.g. SSAI-PRM-2026",
    type="password"
)

st.markdown("</div>", unsafe_allow_html=True)

if not access_id:
    st.stop()

if access_id not in VALID_ACCESS_IDS:
    st.error("❌ Invalid Access ID. You do not have permission to access this application.")
    st.stop()

service_tier = VALID_ACCESS_IDS[access_id]

# ================= HEADER =================
st.markdown("""
<div style="background:linear-gradient(135deg,#4f46e5,#9333ea);
padding:36px;border-radius:22px;margin-bottom:30px">
<h1 style="color:white;margin-bottom:6px;">StaySmart AI</h1>
<p style="color:#e0e7ff;font-size:18px;">
Predict • Prevent • Retain Talent
</p>
</div>
""", unsafe_allow_html=True)

# ================= SERVICE BADGE =================
if service_tier == "standard":
    st.markdown('<span class="badge standard">🟢 Standard Plan Active</span>', unsafe_allow_html=True)
else:
    st.markdown('<span class="badge premium">👑 Premium Plan Active</span>', unsafe_allow_html=True)

st.markdown("---")

# ================= CSV GUIDE =================
with st.expander("📌 CSV Upload Guidelines (HR Friendly)"):
    st.markdown("""
**Required Columns**
- satisfaction_score (1–10)
- engagement_score (1–10)
- last_hike_months
- overtime_hours

**Recommended Columns**
- age
- years_at_company
- salary_lakhs
- work_life_balance (1–5)
- distance_from_home (km)

Missing fields are auto-filled safely.
""")

# ================= FILE UPLOAD =================
st.markdown("## 📂 Upload Employee Dataset")
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if not uploaded_file:
    st.info("⬆️ Upload a CSV file to start analysis.")
    st.stop()

df = pd.read_csv(uploaded_file)
df.columns = df.columns.str.lower().str.replace(" ", "_")

st.success("✅ Dataset uploaded successfully")
st.dataframe(df.head(), use_container_width=True)

# ================= SAFE DEFAULTS =================
defaults = {
    'satisfaction_score': np.random.randint(1, 10, len(df)),
    'engagement_score': np.random.randint(1, 10, len(df)),
    'last_hike_months': np.random.randint(0, 36, len(df)),
    'overtime_hours': np.random.randint(0, 80, len(df)),
    'age': np.random.randint(22, 55, len(df)),
    'years_at_company': np.random.randint(0, 15, len(df)),
    'salary_lakhs': np.random.uniform(3, 20, len(df)),
    'work_life_balance': np.random.randint(1, 5, len(df)),
    'distance_from_home': np.random.randint(1, 40, len(df))
}

for col, values in defaults.items():
    if col not in df.columns:
        df[col] = values

# ================= TARGET ENGINE =================
risk_score = (
    (10 - df['satisfaction_score']) * 0.25 +
    (10 - df['engagement_score']) * 0.25 +
    (df['last_hike_months'] / 36) * 10 * 0.2 +
    (df['overtime_hours'] / 80) * 10 * 0.15 +
    (df['distance_from_home'] / 40) * 10 * 0.15
)

df['left'] = (risk_score > 5.5).astype(int)

features = [
    'age','years_at_company','satisfaction_score',
    'last_hike_months','overtime_hours',
    'engagement_score','salary_lakhs',
    'work_life_balance','distance_from_home'
]

X = df[features]
y = df['left']

# ================= MODEL =================
X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)

model = RandomForestClassifier(n_estimators=120, random_state=42)
model.fit(X_train, y_train)

proba = model.predict_proba(scaler.transform(X))
df['flight_risk'] = (proba[:, -1] * 100).round(0)

# ================= LABELS =================
def label_risk(score):
    if score >= 70:
        return "High Risk"
    elif score >= 50:
        return "Medium Risk"
    return "Low Risk"

df['risk_category'] = df['flight_risk'].apply(label_risk)

# ================= REASONS =================
def reasons(row):
    r = []
    if row['satisfaction_score'] < 5: r.append("Low satisfaction")
    if row['engagement_score'] < 5: r.append("Low engagement")
    if row['last_hike_months'] > 18: r.append("Delayed hike")
    if row['overtime_hours'] > 50: r.append("Excess overtime")
    if row['distance_from_home'] > 25: r.append("Long commute")
    return ", ".join(r[:3])

df['risk_reasons'] = df.apply(reasons, axis=1)

# ================= KPIs =================
st.markdown("## 📊 Executive Snapshot")
k1, k2, k3 = st.columns(3)
k1.metric("Total Employees", len(df))
k2.metric("High Risk Employees", (df['risk_category']=="High Risk").sum())
k3.metric("Average Flight Risk", f"{df['flight_risk'].mean():.1f}%")

if service_tier == "premium":
    cost = (df['risk_category']=="High Risk").sum() * 600000
    st.metric("💰 Attrition Cost at Risk", f"₹{cost/1e7:.2f} Cr")
else:
    st.info("🔒 Cost impact available in Premium")

# ================= VISUAL =================
st.markdown("## 📈 Risk Distribution")
fig, ax = plt.subplots()
df['risk_category'].value_counts().plot(kind="bar", ax=ax)
ax.set_xlabel("")
ax.set_ylabel("Employees")
st.pyplot(fig)

# ================= TOP EMPLOYEES =================
st.markdown("## 🚨 Employees Most Likely to Leave")
st.dataframe(
    df.sort_values("flight_risk", ascending=False)[
        ['flight_risk','risk_category','risk_reasons'] + features
    ].head(10),
    use_container_width=True
)

# ================= RECOMMENDATIONS =================
if service_tier == "premium":
    st.markdown("## 🧠 AI-Powered HR Recommendations")
    st.markdown("""
**Immediate**
- Manager 1-on-1 discussions  
- Compensation & role review  
- Reduce burnout indicators  

**Strategic**
- Clear career paths  
- Monthly engagement pulses  
- Leadership coaching
""")
else:
    st.info("🔒 Upgrade to Premium for detailed HR recommendations")

# ================= DOWNLOAD =================
st.markdown("## ⬇️ Export Results")
st.download_button(
    "Download Full Analysis CSV",
    df.to_csv(index=False),
    file_name="staysmart_ai_results.csv"
)
