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
if "step" not in st.session_state:
    st.session_state.step = "plan"   # plan → auth → dashboard
if "tier" not in st.session_state:
    st.session_state.tier = None
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# ================= LICENSE KEYS =================
LICENSE_KEYS = {
    "standard": ["SSAI-ENT-9F3K-7Q2M-AZ91"],
    "premium": ["SSAI-PRM-X8LQ-4R2Z-M9KP"]
}

# ================= GLOBAL STYLES =================
st.markdown("""
<style>
body { background:#0f172a; }

.center {
    max-width:1100px;
    margin:auto;
}

.card {
    background:white;
    padding:35px;
    border-radius:24px;
    box-shadow:0 20px 45px rgba(0,0,0,0.25);
}

.price {
    font-size:36px;
    font-weight:700;
}

.badge {
    padding:8px 18px;
    border-radius:20px;
    font-weight:600;
    display:inline-block;
}

.standard { background:#e0f2fe; color:#0369a1; }
.premium { background:#fff7ed; color:#c2410c; }

button[kind="primary"] {
    border-radius:14px !important;
    padding:14px 26px !important;
}
</style>
""", unsafe_allow_html=True)

# =================================================
# =============== STEP 1: PLAN SELECT ===============
# =================================================
if st.session_state.step == "plan":

    st.markdown("<div class='center'>", unsafe_allow_html=True)
    st.markdown("## 🚀 Welcome to **StaySmart AI**")
    st.markdown("### Enterprise HR Intelligence Platform")
    st.markdown("Choose a plan to continue")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("""
        <div class="card">
            <span class="badge standard">STANDARD</span>
            <h2>Essential Insights</h2>
            <p class="price">₹100 <span style="font-size:16px">/ employee / month</span></p>
            <ul>
                <li>Attrition risk detection</li>
                <li>Employee risk categories</li>
                <li>Top risk employee list</li>
                <li>Basic visual analytics</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Choose Standard"):
            st.session_state.tier = "standard"
            st.session_state.step = "auth"
            st.rerun()

    with c2:
        st.markdown("""
        <div class="card">
            <span class="badge premium">PREMIUM</span>
            <h2>Advanced Intelligence</h2>
            <p class="price">₹150 <span style="font-size:16px">/ employee / month</span></p>
            <ul>
                <li>Everything in Standard</li>
                <li>Attrition cost exposure</li>
                <li>Driver importance analysis</li>
                <li>Actionable HR recommendations</li>
                <li>Executive-level insights</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Choose Premium"):
            st.session_state.tier = "premium"
            st.session_state.step = "auth"
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# =================================================
# =============== STEP 2: AUTH =====================
# =================================================
if st.session_state.step == "auth":

    st.markdown("<div class='center'>", unsafe_allow_html=True)
    st.markdown("## 🔐 License Verification")

    plan_label = "STANDARD" if st.session_state.tier == "standard" else "PREMIUM"
    price_label = "₹100 / employee / month" if plan_label == "STANDARD" else "₹150 / employee / month"

    st.markdown(f"""
    <div class="card">
        <span class="badge {'standard' if plan_label=='STANDARD' else 'premium'}">{plan_label}</span>
        <p>{price_label}</p>
    """, unsafe_allow_html=True)

    key = st.text_input(
        "Enter License Key",
        placeholder="SSAI-XXXX-XXXX-XXXX",
        type="password"
    )

    if st.button("Verify & Continue"):
        if key in LICENSE_KEYS[st.session_state.tier]:
            st.session_state.authenticated = True
            st.session_state.step = "dashboard"
            st.rerun()
        else:
            st.error("❌ Invalid license key for selected plan")

    st.markdown("</div></div>", unsafe_allow_html=True)
    st.stop()

# =================================================
# =============== STEP 3: DASHBOARD ================
# =================================================
if not st.session_state.authenticated:
    st.stop()

tier = st.session_state.tier

# ================= HEADER =================
st.markdown("""
<div style="background:linear-gradient(135deg,#4f46e5,#9333ea);
padding:40px;border-radius:26px;margin-bottom:30px">
<h1 style="color:white;">StaySmart AI Dashboard</h1>
<p style="color:#e0e7ff;font-size:18px">
Predict • Prevent • Retain Talent
</p>
</div>
""", unsafe_allow_html=True)

st.markdown(
    f"<span class='badge {'standard' if tier=='standard' else 'premium'}'>"
    f"{'Standard' if tier=='standard' else 'Premium'} Plan Active</span>",
    unsafe_allow_html=True
)

# ================= FILE UPLOAD =================
file = st.file_uploader("📂 Upload Employee Dataset", type=["csv"])
if not file:
    st.info("Upload a CSV to begin analysis")
    st.stop()

df = pd.read_csv(file)
df.columns = df.columns.str.lower().str.replace(" ", "_")

# ================= REQUIRED COLUMNS =================
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

# ================= RISK LOGIC =================
risk_score = (
    (10 - df['satisfaction_score']) * 0.30 +
    (10 - df['engagement_score']) * 0.30 +
    (df['last_hike_months'] / 36) * 10 * 0.20 +
    (df['overtime_hours'] / 80) * 10 * 0.10 +
    (df['distance_from_home'] / 40) * 10 * 0.10
)

df['left'] = (risk_score > 5.5).astype(int)

X = df[list(required_cols.keys())]
y = df['left']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42)
model.fit(X_scaled, y)

df['flight_risk'] = (model.predict_proba(X_scaled)[:, 1] * 100).round(0)
df['risk_category'] = pd.cut(df['flight_risk'], [0,49,69,100], labels=["Low","Medium","High"])

# ================= KPIs =================
c1, c2, c3 = st.columns(3)
c1.metric("Total Employees", len(df))
c2.metric("High Risk Employees", int((df['risk_category']=="High").sum()))
c3.metric("Average Risk", f"{df['flight_risk'].mean():.1f}%")

if tier == "premium":
    st.metric("Estimated Attrition Exposure", f"₹{(df['risk_category']=='High').sum()*5:.1f} Lakhs")

# ================= CHART =================
st.markdown("## 📊 Risk Distribution")
fig, ax = plt.subplots()
df['risk_category'].value_counts().plot(kind="bar", ax=ax)
st.pyplot(fig)

# ================= TABLE =================
st.markdown("## 🚨 Highest Risk Employees")
st.dataframe(df.sort_values("flight_risk", ascending=False).head(10), use_container_width=True)

# ================= PREMIUM ONLY =================
if tier == "premium":
    st.markdown("## 🧠 Key Attrition Drivers")
    importance = pd.Series(model.feature_importances_, index=X.columns).sort_values()
    fig2, ax2 = plt.subplots()
    importance.plot(kind="barh", ax=ax2)
    st.pyplot(fig2)

    st.markdown("""
**Recommended Actions**
- Review compensation delays  
- Reduce overtime for high-risk groups  
- Manager-level retention conversations  
- Hybrid work for long-commute employees
""")

# ================= EXPORT =================
st.download_button(
    "⬇️ Download Full Report",
    df.to_csv(index=False),
    "staysmart_ai_report.csv"
)
