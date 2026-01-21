# -*- coding: utf-8 -*-
"""StaySmart AI - Enhanced Dashboard"""

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

st.set_page_config(page_title="StaySmart AI", layout="wide")

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

# ================= FRONT PAGE GUIDE =================
st.markdown("## 📌 CSV Requirements for HR Team")

with st.expander("📄 Required & Recommended Columns (Click to Expand)", expanded=True):
    st.markdown("""
**Required (core drivers):**
- `satisfaction_score` (1–10)
- `engagement_score` (1–10)
- `last_hike_months` (months since last increment)
- `overtime_hours` (monthly average)

**Recommended (improves accuracy):**
- `age`
- `years_at_company`
- `salary_lakhs`
- `work_life_balance` (1–5)
- `distance_from_home` (km travelled daily)

> ⚠️ If a column is missing, StaySmart AI auto-fills smart defaults.
""")

st.markdown("### 📂 Upload Employee CSV")
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

# ================= MAIN LOGIC =================
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("CSV uploaded successfully!")
    st.dataframe(df.head())

    # ================= PREPROCESS =================
    df.columns = df.columns.str.lower().str.replace(" ", "_")

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
    X_train, X_test, y_train, y_test = train_test_split(
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
        else:
            return "Low Risk"

    df['risk_category'] = df['flight_risk'].apply(label_risk)

    # ================= INSIGHT REASONS =================
    def reason(row):
        reasons = []
        if row['satisfaction_score'] < 5: reasons.append("Low satisfaction")
        if row['engagement_score'] < 5: reasons.append("Low engagement")
        if row['last_hike_months'] > 18: reasons.append("No recent hike")
        if row['overtime_hours'] > 50: reasons.append("High overtime")
        if row['distance_from_home'] > 25: reasons.append("Long commute")
        return ", ".join(reasons[:3])

    df['risk_reasons'] = df.apply(reason, axis=1)

    # ================= KPI CARDS =================
    st.markdown("## 📊 Executive Overview")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Employees", len(df))
    c2.metric("High Risk Employees", (df['risk_category']=="High Risk").sum())
    c3.metric("Avg Flight Risk", f"{df['flight_risk'].mean():.1f}")

    # ================= COST IMPACT =================
    avg_replacement_cost = 6_00_000
    cost_risk = (df['risk_category']=="High Risk").sum() * avg_replacement_cost
    st.metric("💰 Potential Cost at Risk", f"₹{cost_risk/1e7:.2f} Cr")

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

    # ================= DOWNLOAD =================
    st.download_button(
        "⬇️ Download Full Analysis",
        df.to_csv(index=False),
        file_name="staysmart_ai_results.csv"
    )

else:
    st.info("Upload a CSV file to begin employee flight-risk analysis.")
