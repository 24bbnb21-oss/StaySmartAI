# -*- coding: utf-8 -*-
"""StaySmart AI – Enterprise HR Intelligence"""

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score
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
if "paid" not in st.session_state:
    st.session_state.paid = False

# ================= LICENSE KEYS =================
LICENSE_KEYS = {
    "standard": ["SSAI-STD-1A2B-3C4D"],
    "premium": ["SSAI-PRM-X8LQ-4R2Z-M9KP"]
}

# ================= STYLES =================
st.markdown("""
<style>
body {
    background: radial-gradient(circle at top left, #1f2a63, #0b1220 60%, #060a12 100%);
    color:#e5e7eb;
    font-family: "Segoe UI", sans-serif;
    transition: background 0.5s ease;
}

.fade {
    animation: fadeIn 0.9s ease-in-out;
}

@keyframes fadeIn {
    from {opacity: 0; transform: translateY(10px);}
    to {opacity: 1; transform: translateY(0px);}
}

.hero {
    text-align:center;
    padding:70px 20px 30px;
}

.hero h1 {
    font-size:52px;
    font-weight:800;
    color:white;
}

.hero p {
    font-size:20px;
    color:#c7d2fe;
}

.plan-card {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    padding:40px;
    border-radius:28px;
    box-shadow:0 30px 70px rgba(0,0,0,0.35);
    height:100%;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.plan-card:hover{
    transform: translateY(-6px);
    box-shadow:0 40px 90px rgba(0,0,0,0.55);
}

.plan-title {
    font-size:28px;
    font-weight:800;
    color:#e5e7eb;
    margin-top:15px;
}

.plan-desc {
    color:#cbd5f5;
    font-size:16px;
    margin:15px 0;
}

.price {
    font-size:40px;
    font-weight:800;
    color:#fff;
    margin:20px 0;
}

ul {
    padding-left:20px;
    color:#cbd5f5;
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
    background: rgba(15,23,42,0.85);
    color:#e5e7eb;
    padding:28px;
    border-radius:20px;
    margin-top:30px;
    border: 1px solid rgba(255,255,255,0.12);
}

.req-box h4 {
    margin-bottom:10px;
}

.req-box li {
    color:#cbd5f5;
}

.compare {
    background: rgba(15,23,42,0.75);
    padding:25px;
    border-radius:25px;
    margin-top:30px;
    border: 1px solid rgba(255,255,255,0.12);
}

.compare h3 {
    color:#fff;
    margin-bottom:10px;
}

.compare table {
    width:100%;
    border-collapse:collapse;
}

.compare th, .compare td {
    border:1px solid rgba(255,255,255,0.12);
    padding:10px;
    text-align:center;
    color:#cbd5f5;
}

.compare th {
    background:#111827;
    color:#fff;
}

.compare td {
    background: rgba(11,18,32,0.75);
}

.check {
    color:#34d399;
    font-weight:700;
}

.cross {
    color:#fca5a5;
    font-weight:700;
}

.dashboard-header {
    background: linear-gradient(135deg,#4f46e5,#7c3aed);
    padding:40px;
    border-radius:30px;
    margin-bottom:30px;
    border: 1px solid rgba(255,255,255,0.2);
}

.dashboard-header h1, .dashboard-header p {
    margin:0;
}

.insight-card {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius:20px;
    padding:20px;
    transition: transform 0.3s ease;
}
.insight-card:hover{
    transform: translateY(-4px);
}

.insight-title {
    font-weight:800;
    font-size:18px;
    color:#fff;
}

.insight-desc {
    color:#cbd5f5;
    margin-top:6px;
    font-size:14px;
}

.insight-value {
    font-size:24px;
    font-weight:800;
    margin-top:10px;
}

.actions {
    display:flex;
    gap:15px;
}

.action-box {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius:20px;
    padding:18px;
}

.action-box h4 {
    margin:0;
    color:#fff;
}

.action-box p {
    margin:6px 0 0 0;
    color:#cbd5f5;
    font-size:14px;
}

.action-box .tag {
    display:inline-block;
    padding:6px 10px;
    border-radius:15px;
    font-weight:700;
    margin-top:10px;
    font-size:12px;
}

.tag-high { background:#fca5a5; color:#7f1d1d; }
.tag-med { background:#fde68a; color:#92400e; }
.tag-low { background:#a7f3d0; color:#064e3b; }

.logo {
    display:flex;
    align-items:center;
    gap:12px;
    margin-bottom:20px;
}
.logo img {
    height:44px;
    width:44px;
    border-radius:12px;
    border: 1px solid rgba(255,255,255,0.2);
}
.logo h2 {
    margin:0;
    font-size:22px;
    font-weight:800;
    color:#fff;
}

.payment-box {
    background: rgba(15,23,42,0.85);
    padding:25px;
    border-radius:25px;
    border: 1px solid rgba(255,255,255,0.12);
    margin-top:20px;
}

.payment-box h3 {
    margin-top:0;
    color:#fff;
}

.payment-box input {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    color:#e5e7eb;
    padding:10px;
    border-radius:10px;
    width:100%;
}

.payment-box button {
    background: linear-gradient(135deg,#4f46e5,#7c3aed);
    color:#fff;
    padding:12px 20px;
    border:none;
    border-radius:12px;
    font-weight:800;
    cursor:pointer;
}

.footer {
    text-align:center;
    margin-top:40px;
    color:#94a3b8;
    font-size:14px;
}
</style>
""", unsafe_allow_html=True)

# =================================================
# =============== STEP 1: PLAN SELECT ===============
# =================================================
if st.session_state.step == "plan":

    st.markdown("""
    <div class="logo">
        <img src="https://img.icons8.com/fluency/48/000000/brain.png" />
        <h2>StaySmart AI</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="hero fade">
        <h1>StaySmart AI</h1>
        <p>Predict Attrition • Reduce Risk • Retain Talent</p>
    </div>
    """, unsafe_allow_html=True)

    # ======= NEW PROFESSIONAL FRONT PAGE CONTENT =======
    st.markdown("""
    <div class="req-box fade" style="max-width:1000px;margin:auto;">
        <h4>What StaySmart AI Provides</h4>
        <p style="color:#cbd5f5">
        StaySmart AI uses employee data to predict attrition risk and provide actionable insights to HR teams.
        This helps reduce turnover cost, improve employee engagement, and retain top performers.
        </p>
        <div class="actions">
            <div class="action-box">
                <h4>1) Data Ingestion</h4>
                <p>Upload employee CSV or integrate HRMS data</p>
            </div>
            <div class="action-box">
                <h4>2) AI Risk Scoring</h4>
                <p>Real-time attrition risk prediction</p>
            </div>
            <div class="action-box">
                <h4>3) Retention Actions</h4>
                <p>Get recommendations to retain high performers</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ======= NEW SECTION IN PLACE OF SAMPLE GRAPH =======
    st.markdown("""
    <div class="compare fade" style="margin-top:30px;">
        <h3>Why StaySmart AI?</h3>
        <p style="color:#cbd5f5; font-size:16px;">
            StaySmart AI provides HR teams with data-driven attrition prediction, helping you retain your best talent.
            Get instant insights, clear risk indicators, and actionable retention recommendations.
        </p>
        <div style="display:flex; gap:15px; justify-content:center; flex-wrap:wrap; margin-top:15px;">
            <div style="background:rgba(255,255,255,0.08); padding:15px; border-radius:20px; border:1px solid rgba(255,255,255,0.12); width:220px;">
                <h4 style="color:#fff; margin:0;">📌 Risk Prediction</h4>
                <p style="color:#cbd5f5; margin:8px 0 0 0;">Predict flight risk in real-time.</p>
            </div>
            <div style="background:rgba(255,255,255,0.08); padding:15px; border-radius:20px; border:1px solid rgba(255,255,255,0.12); width:220px;">
                <h4 style="color:#fff; margin:0;">🧠 AI Insights</h4>
                <p style="color:#cbd5f5; margin:8px 0 0 0;">Understand WHY employees leave.</p>
            </div>
            <div style="background:rgba(255,255,255,0.08); padding:15px; border-radius:20px; border:1px solid rgba(255,255,255,0.12); width:220px;">
                <h4 style="color:#fff; margin:0;">🛡️ Retention Tips</h4>
                <p style="color:#cbd5f5; margin:8px 0 0 0;">Actionable steps to retain talent.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ================= TRUST LOGOS =================
    st.markdown("""
    <div class="compare fade">
        <h3>Trusted By</h3>
        <div style="display:flex; gap:25px; justify-content:center; flex-wrap:wrap;">
            <div style="text-align:center; padding:15px;">
                <img src="https://img.icons8.com/fluency/48/000000/briefcase.png" />
                <p>Enterprise</p>
            </div>
            <div style="text-align:center; padding:15px;">
                <img src="https://img.icons8.com/fluency/48/000000/company.png" />
                <p>HR Teams</p>
            </div>
            <div style="text-align:center; padding:15px;">
                <img src="https://img.icons8.com/fluency/48/000000/analytics.png" />
                <p>Data Teams</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ======= ADD SPACE BEFORE PLANS =======
    st.markdown("<br><br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="plan-card fade">
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
        <div class="plan-card fade">
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

    # ================= COMPARISON TABLE =================
    st.markdown("""
    <div class="compare fade">
        <h3>Plan Comparison</h3>
        <table>
            <tr>
                <th>Feature</th>
                <th>Standard</th>
                <th>Premium</th>
            </tr>
            <tr>
                <td>Flight Risk Score</td>
                <td class="check">✔</td>
                <td class="check">✔</td>
            </tr>
            <tr>
                <td>Risk Categories</td>
                <td class="check">✔</td>
                <td class="check">✔</td>
            </tr>
            <tr>
                <td>Retention Recommendations</td>
                <td class="cross">✘</td>
                <td class="check">✔</td>
            </tr>
            <tr>
                <td>Attrition Cost Estimation</td>
                <td class="cross">✘</td>
                <td class="check">✔</td>
            </tr>
            <tr>
                <td>Leadership Insights</td>
                <td class="cross">✘</td>
                <td class="check">✔</td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

    st.stop()

# =================================================
# =============== STEP 2: AUTH =====================
# =================================================
if st.session_state.step == "auth":

    tier = st.session_state.tier
    price_per_employee = 100 if tier == "standard" else 150
    price = f"₹{price_per_employee} / employee / month"

    st.markdown("""
    <div class="logo">
        <img src="https://img.icons8.com/fluency/48/000000/brain.png" />
        <h2>StaySmart AI</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="plan-card fade" style="max-width:620px;margin:auto;">
        <span class="badge {'standard' if tier=='standard' else 'premium'}">
            {tier.upper()} PLAN
        </span>
        <p style="margin-top:10px;font-weight:600;color:#cbd5f5">{price}</p>
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

    # ================= PAYMENT SIMULATION =================
    st.markdown("""
    <div class="payment-box fade">
        <h3>🏢 Company Subscription Payment</h3>
        <p style="color:#cbd5f5">
        Enter company billing details to proceed. (Simulation only)
        </p>
    """, unsafe_allow_html=True)

    employees = st.number_input("Number of Employees", min_value=1, value=10)
    months = st.number_input("Subscription Duration (months)", min_value=1, value=3)

    total_amount = employees * months * price_per_employee

    st.markdown(f"""
    <div style="margin-top:10px; color:#cbd5f5;">
        <b>Payment Summary:</b><br>
        Employees: {employees} <br>
        Duration: {months} months <br>
        <b>Total Amount:</b> ₹{total_amount}
    </div>
    """, unsafe_allow_html=True)

    company_name = st.text_input("Company Name")
    company_email = st.text_input("Company Email")
    gstin = st.text_input("GSTIN (Optional)")

    if st.button("Pay Now"):
        st.session_state.paid = True
        st.success("Payment Successful ✓")

    # This ensures license key appears only after payment is done
    if st.session_state.paid:
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
<div class="logo">
    <img src="https://img.icons8.com/fluency/48/000000/brain.png" />
    <h2>StaySmart AI</h2>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="dashboard-header fade">
<h1>StaySmart AI Dashboard</h1>
<p style="font-size:18px">AI-powered employee attrition insights</p>
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

# MODEL TARGET (risk-based)
risk_score = (
    (10-df['satisfaction_score'])*0.3 +
    (10-df['engagement_score'])*0.3 +
    (df['last_hike_months']/36)*10*0.2 +
    (df['overtime_hours']/80)*10*0.1 +
    (df['distance_from_home']/40)*10*0.1
)

df['left'] = (risk_score > 5.5).astype(int)

X = df[list(required_cols.keys())]
y = df['left']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# TRAIN TEST SPLIT FOR BETTER ACCURACY
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=200, max_depth=8, random_state=42)
model.fit(X_train, y_train)

# Accuracy
acc = model.score(X_test, y_test)
cv_acc = cross_val_score(model, X_scaled, y, cv=5).mean()

df['flight_risk'] = (model.predict_proba(X_scaled)[:,1]*100).round(0)
df['risk_category'] = pd.cut(df['flight_risk'], [0,49,69,100], labels=["Low","Medium","High"])

# ================= PLAN FEATURE LIMIT =================
if st.session_state.tier == "standard":
    st.warning("You are using STANDARD plan. Upgrade to Premium for Attrition Cost & Retention Tips.")

# ================= METRICS =================
c1,c2,c3 = st.columns(3)
c1.metric("Employees", len(df))
c2.metric("High Risk", int((df['risk_category']=="High").sum()))
c3.metric("Avg Risk", f"{df['flight_risk'].mean():.1f}%")

# Accuracy Metrics
st.markdown(f"**Model Accuracy:** {acc*100:.2f}%  |  **Cross-Validation:** {cv_acc*100:.2f}%")

# ================= CHART =================
st.markdown("## 📊 Risk Distribution")
fig, ax = plt.subplots(figsize=(8,3))
df['risk_category'].value_counts().plot(kind="bar", ax=ax)
ax.set_title("Risk Category Distribution")
ax.set_xlabel("Risk Category")
ax.set_ylabel("Number of Employees")
ax.grid(axis='y', linestyle='--', alpha=0.5)
st.pyplot(fig)

# ================= NEW GRAPH: Risk by Overtime =================
st.markdown("## 📈 Risk vs Overtime Hours")
fig2, ax2 = plt.subplots(figsize=(8,3))
ax2.scatter(df['overtime_hours'], df['flight_risk'])
ax2.set_title("Overtime vs Flight Risk")
ax2.set_xlabel("Overtime Hours")
ax2.set_ylabel("Flight Risk (%)")
ax2.grid(True, linestyle='--', alpha=0.5)
st.pyplot(fig2)

# ================= VISUAL INSIGHTS =================
st.markdown("## 🧠 Insights")

ins1, ins2, ins3 = st.columns(3)
with ins1:
    st.markdown("""
    <div class="insight-card fade">
        <div class="insight-title">Satisfaction Impact</div>
        <div class="insight-desc">Low satisfaction increases risk quickly.</div>
        <div class="insight-value">{:.1f}%</div>
    </div>
    """.format((10-df['satisfaction_score']).mean()*10), unsafe_allow_html=True)

with ins2:
    st.markdown("""
    <div class="insight-card fade">
        <div class="insight-title">Engagement Impact</div>
        <div class="insight-desc">Low engagement is a strong attrition driver.</div>
        <div class="insight-value">{:.1f}%</div>
    </div>
    """.format((10-df['engagement_score']).mean()*10), unsafe_allow_html=True)

with ins3:
    st.markdown("""
    <div class="insight-card fade">
        <div class="insight-title">Overtime Pressure</div>
        <div class="insight-desc">High overtime increases burnout risk.</div>
        <div class="insight-value">{:.1f}%</div>
    </div>
    """.format((df['overtime_hours']/80).mean()*100), unsafe_allow_html=True)

# Premium-only charts & insights
if st.session_state.tier == "premium":
    st.markdown("## 📈 Risk Breakdown (Premium)")
    fig3, ax3 = plt.subplots(figsize=(6,4))
    df['risk_category'].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax3)
    ax3.set_ylabel('')
    ax3.set_title("Risk Category %")
    st.pyplot(fig3)

    # ================= NEW GRAPH: Risk by Satisfaction =================
    st.markdown("## 📊 Satisfaction vs Risk (Premium)")
    fig4, ax4 = plt.subplots(figsize=(8,3))
    ax4.scatter(df['satisfaction_score'], df['flight_risk'])
    ax4.set_title("Satisfaction vs Flight Risk")
    ax4.set_xlabel("Satisfaction Score")
    ax4.set_ylabel("Flight Risk (%)")
    ax4.grid(True, linestyle='--', alpha=0.5)
    st.pyplot(fig4)

    st.markdown("## 🧩 Retention Recommendations (Premium)")
    st.write("Top retention actions based on risk score:")

    st.markdown("### 🔴 High Risk (70%+)")
    st.write("- Immediate retention bonus or compensation review")
    st.write("- Immediate 1:1 manager meeting (within 24 hrs)")
    st.write("- Role change or internal transfer")
    st.write("- Flexible work hours or work-from-home options")
    st.write("- Fast-track promotion or career path clarity")
    st.write("- Offer training/skill upgrade plan")
    st.write("- Reduce workload or redistribute tasks")
    st.write("- Provide mentorship & leadership support")

    st.markdown("### 🟠 Medium Risk (50% - 69%)")
    st.write("- Short-term recognition & rewards")
    st.write("- Improve engagement through team events")
    st.write("- Provide feedback & growth plan")
    st.write("- Increase visibility in projects")
    st.write("- Offer flexible schedule for 2-4 weeks")
    st.write("- Mentorship program enrollment")
    st.write("- Quarterly salary review / appraisal")
    st.write("- Provide skill-building training")

    st.markdown("### 🟢 Low Risk (Below 50%)")
    st.write("- Keep motivation high with recognition")
    st.write("- Encourage internal growth & promotions")
    st.write("- Provide continuous learning & training")
    st.write("- Maintain transparent communication")
    st.write("- Improve employee wellness & work-life balance")
    st.write("- Ensure career path clarity")

    # ================= FLIGHT RISK SIMULATION =================
    st.markdown("## ✨ Flight Risk Simulation (Premium)")
    st.write("Adjust values and simulate the employee flight risk.")

    sim_satisfaction = st.slider("Satisfaction Score (1-10)", 1, 10, 6)
    sim_engagement = st.slider("Engagement Score (1-10)", 1, 10, 6)
    sim_hike = st.slider("Months since last hike", 0, 36, 12)
    sim_overtime = st.slider("Overtime hours/month", 0, 80, 10)
    sim_distance = st.slider("Distance from home (km)", 1, 40, 10)

    sim_df = pd.DataFrame([{
        "satisfaction_score": sim_satisfaction,
        "engagement_score": sim_engagement,
        "last_hike_months": sim_hike,
        "overtime_hours": sim_overtime,
        "distance_from_home": sim_distance
    }])

    sim_scaled = scaler.transform(sim_df)
    sim_risk = model.predict_proba(sim_scaled)[0][1] * 100

    st.markdown(f"### **Predicted Flight Risk: {sim_risk:.0f}%**")
    if sim_risk >= 70:
        st.warning("High Risk — Immediate retention action required")
    elif sim_risk >= 50:
        st.info("Medium Risk — Take action soon")
    else:
        st.success("Low Risk — Maintain engagement")

st.download_button(
    "⬇️ Download Full Report",
    df.to_csv(index=False),
    "staysmart_ai_report.csv"
)

# ================= ABOUT US SECTION =================
st.markdown("""
<div class="compare fade" style="margin-top:30px;">
    <h3>About Us</h3>
    <p style="color:#cbd5f5; font-size:16px;">
        StaySmart AI is built for modern enterprises to help HR teams predict attrition risk and retain top talent.
        Our AI analyzes employee engagement, satisfaction, overtime and more to provide actionable insights.
    </p>
</div>
""", unsafe_allow_html=True)

# ================= ABOUT US FOOTER =================
st.markdown("""
<div class="footer">
<b>About Us</b><br>
StaySmart AI is a HR intelligence tool built for modern enterprises. Our AI predicts attrition risk and helps HR teams retain top talent using data-driven insights.<br>
© 2026 EXQ-16. All Rights Reserved.
</div>
""", unsafe_allow_html=True)
