# -*- coding: utf-8 -*-
"""StaySmart AI – Secure Tiered HR Analytics"""

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# ================= PAGE CONFIG =================
st.set_page_config(page_title="StaySmart AI", layout="wide")

# ================= ACCESS CONTROL =================
VALID_ACCESS_IDS = {
    "SSAI-STD-2026": "standard",
    "SSAI-PRM-2026": "premium"
}

st.sidebar.markdown("## 🔐 Access Verification")
access_id = st.sidebar.text_input("Enter Access ID", type="password")

if access_id not in VALID_ACCESS_IDS:
    st.error("❌ You do not have access to this application.")
    st.stop()

service_tier = VALID_ACCESS_IDS[access_id]

# ================= HEADER =================
st.markdown("""
<div style='background:linear-gradient(135deg,#667eea,#764ba2);
padding:30px;border-radius:12px'>
<h1 style='color:white;'>🚀 StaySmart AI</h1>
<p style='color:#e0e7ff;font-size:18px'>
Predictive Talent Analytics for Bharat’s SMEs
</p>
</div>
""", unsafe_allow_html=True)

# ================= SERVICE TIER =================
st.markdown("## 🧾 Service Plan")

if service_tier == "standard":
    st.success("🟢 Standard Service Activated")
    st.markdown("""
    - Flight risk score
    - High / Medium / Low risk labels
    - Top risky employees
    - Basic insights
    """)
else:
    st.warning("👑 Premium Service Activated")
    st.markdown("""
    - Everything in Standard  
    - Root-cause analysis  
    - Cost impact analysis  
    - HR action recommendations
    """)

# ================= FRONT PAGE GUIDE =================
st.markdown("## 📌 CSV Requirements for HR Team")

with st.expander("📄 Required & Recommended Columns"):
    st.markdown("""
**Required**
- `satisfaction_score` (1–10)
- `engagement_score` (1–10)
- `last_hike_months`
- `overtime_hours`

**Recommended**
- `age`
- `years_at_company`
- `salary_lakhs`
- `work_life_balance` (1–5)
- `distance_from_home` (km)

⚠️ Missing columns are auto-filled safely.
""")

# ================= FILE UPLOAD =================
st.markdown("### 📂 Upload Employee CSV")
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if not uploaded_file:
    st.info("Upload a CSV file to begin analysis.")
    st.stop()

# ================= LOAD DATA =================
df = pd.read_csv(uploaded_file)
st.success("CSV uploaded successfully!")
st.dataframe(df.head())

df.columns = df.columns.str.lower().str.replace(" ", "_")

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
X_train, _, y_train, _ = train_test_split(
    X, y, test_size=0.2, random_state=42
)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)

model = RandomForestClassifier(n_estimators=120, random_state=42)
model.fit(X_train, y_train)

proba = model.predict_proba(scaler.transform(X))
df['flight_risk'] = (proba[:, -1] * 100).round(0)

# ================= RISK LABELS =================
def label_risk(score):
    if score >= 70:
        return "High Risk"
    elif score >= 50:
        return "Medium Risk"
    return "Low Risk"

df['risk_category'] = df['flight_risk'].apply(label_risk)

# ================= RISK REASONS =================
def reasons(row):
    r = []
    if row['satisfaction_score'] < 5: r.append("Low satisfaction")
    if row['engagement_score'] < 5: r.append("Low engagement")
    if row['last_hike_months'] > 18: r.append("No recent hike")
    if row['overtime_hours'] > 50: r.append("High overtime")
    if row['distance_from_home'] > 25: r.append("Long commute")
    return ", ".join(r[:3])

df['risk_reasons'] = df.apply(reasons, axis=1)

# ================= KPIs =================
st.markdown("## 📊 Executive Overview")
c1, c2, c3 = st.columns(3)
c1.metric("Total Employees", len(df))
c2.metric("High Risk Employees", (df['risk_category']=="High Risk").sum())
c3.metric("Avg Flight Risk", f"{df['flight_risk'].mean():.1f}")

# ================= COST IMPACT (PREMIUM) =================
if service_tier == "premium":
    cost = (df['risk_category']=="High Risk").sum() * 600000
    st.metric("💰 Potential Cost at Risk", f"₹{cost/1e7:.2f} Cr")
else:
    st.info("🔒 Cost impact available in Premium")

# ================= DISTRIBUTION =================
st.markdown("## 📈 Risk Distribution")
fig, ax = plt.subplots()
df['risk_category'].value_counts().plot(kind="bar", ax=ax)
st.pyplot(fig)

# ================= TOP EMPLOYEES =================
st.markdown("## 🚨 Employees Most Likely to Leave")
st.dataframe(
    df.sort_values("flight_risk", ascending=False)[
        ['flight_risk','risk_category','risk_reasons'] + features
    ].head(10)
)

# ================= RECOMMENDATIONS =================
if service_tier == "premium":
    st.markdown("## 🧠 AI-Powered HR Recommendations")
    st.markdown("""
**Immediate**
- Conduct 1-on-1 discussions
- Review compensation gaps
- Reduce overtime exposure

**Strategic**
- Improve growth clarity
- Monitor engagement monthly
- Strengthen manager feedback
""")
else:
    st.info("🔒 Upgrade to Premium for HR recommendations")

# ================= DOWNLOAD =================
st.download_button(
    "⬇️ Download Full Analysis",
    df.to_csv(index=False),
    file_name="staysmart_ai_results.csv"
)
