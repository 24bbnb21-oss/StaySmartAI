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
if "paid" not in st.session_state:
    st.session_state.paid = False  # NEW: payment state

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
}

.hero p {
    font-size:20px;
    color:#c7d2fe;
}

.plan-card {
    background:#ffffff;
    padding:40px;
    border-radius:28px;
    box-shadow:0 30px 70px rgba(0,0,0,0.35);
    height:100%;
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
}

.req-box h4 {
    margin-bottom:10px;
}

.req-box li {
    color:#cbd5f5;
}

.compare {
    background:#0f172a;
    padding:25px;
    border-radius:25px;
    margin-top:30px;
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
    border:1px solid #334155;
    padding:10px;
    text-align:center;
    color:#cbd5f5;
}

.compare th {
    background:#111827;
    color:#fff;
}

.compare td {
    background:#0b1220;
}

.check {
    color:#34d399;
    font-weight:700;
}

.cross {
    color:#fca5a5;
    font-weight:700;
}

/* NEW: Cool animated background */
.bg {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  background: radial-gradient(circle at 20% 20%, rgba(124,58,237,0.35), transparent 40%),
              radial-gradient(circle at 80% 30%, rgba(34,211,238,0.25), transparent 45%),
              radial-gradient(circle at 50% 80%, rgba(16,185,129,0.22), transparent 50%),
              linear-gradient(135deg, #0b1220 0%, #0a0f1a 100%);
  animation: bgmove 10s infinite alternate;
}

@keyframes bgmove {
  0% { transform: scale(1); }
  100% { transform: scale(1.02); }
}

/* NEW: Premium insight boxes */
.insight-box {
    border-radius:20px;
    padding:20px;
    color:white;
    margin-top:15px;
}
.immediate { background:#ef4444; }
.short { background:#f59e0b; }
.long { background:#10b981; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="bg"></div>', unsafe_allow_html=True)  # NEW

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

    # ================= COMPARISON TABLE =================
    st.markdown("""
    <div class="compare">
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

    # ================= PAYMENT GATEWAY (REALISTIC UI) =================
    st.markdown("## 🔒 Payment")
    if not st.session_state.paid:
        st.markdown("**Enter card details to proceed (Simulated Gateway)**")
        name = st.text_input("Name on Card")
        card = st.text_input("Card Number", max_chars=16)
        expiry = st.text_input("Expiry (MM/YY)", max_chars=5)
        cvv = st.text_input("CVV", max_chars=3, type="password")

        if st.button("Pay Now"):
            if len(card) == 16 and len(expiry) == 5 and len(cvv) == 3 and name.strip() != "":
                st.session_state.paid = True
                st.success("✅ Payment successful! Proceed to license verification.")
            else:
                st.error("❌ Payment failed. Check card details and try again.")
    else:
        st.success("Payment already completed. You can now verify your license key.")

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

# ================= NAV + LOGOUT =================
st.sidebar.title("Navigation")
if st.sidebar.button("Logout / Reset"):
    st.session_state.step = "plan"
    st.session_state.tier = None
    st.session_state.authenticated = False
    st.session_state.nav = "Home"
    st.session_state.paid = False
    st.experimental_rerun()

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

# ================= PLAN FEATURE LIMIT =================
if st.session_state.tier == "standard":
    st.warning("You are using STANDARD plan. Upgrade to Premium for Attrition Cost & Retention Tips.")

# ================= METRICS =================
c1,c2,c3 = st.columns(3)
c1.metric("Employees", len(df))
c2.metric("High Risk", int((df['risk_category']=="High").sum()))
c3.metric("Avg Risk", f"{df['flight_risk'].mean():.1f}%")

# ================= CHART =================
st.markdown("## 📊 Risk Distribution")
fig, ax = plt.subplots()
df['risk_category'].value_counts().plot(kind="bar", ax=ax)
st.pyplot(fig)

# Premium-only charts & insights
if st.session_state.tier == "premium":
    st.markdown("## 📈 Risk Breakdown")
    fig2, ax2 = plt.subplots()
    df['risk_category'].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax2)
    ax2.set_ylabel('')
    st.pyplot(fig2)

    # ================= PREMIUM INSIGHTS =================
    st.markdown("## 🧩 Retention Recommendations")

    st.markdown("""
    <div class="insight-box immediate">
        <h4>Immediate Actions</h4>
        <ul>
            <li>Offer retention bonus or salary adjustment</li>
            <li>Provide role change or project transfer</li>
            <li>Address immediate workload stress</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box short">
        <h4>Short-Term Actions</h4>
        <ul>
            <li>Increase recognition & feedback</li>
            <li>Improve engagement through team events</li>
            <li>Offer mentorship & career guidance</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box long">
        <h4>Long-Term Actions</h4>
        <ul>
            <li>Review compensation structure & hike cycle</li>
            <li>Implement leadership development</li>
            <li>Improve company culture & retention programs</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # ================= RISK SIMULATION (PREMIUM ONLY) =================
    st.markdown("## 🔥 Risk Simulation (Premium)")
    sim_months = st.slider("Simulation Months", 3, 12, 6)
    sim_risk = np.linspace(df['flight_risk'].mean(), df['flight_risk'].mean() + 10, sim_months)
    fig3, ax3 = plt.subplots()
    ax3.plot(range(1, sim_months + 1), sim_risk, marker='o')
    ax3.set_title("Risk Trend Over Time")
    ax3.set_xlabel("Months")
    ax3.set_ylabel("Avg Risk %")
    st.pyplot(fig3)

st.download_button(
    "⬇️ Download Full Report",
    df.to_csv(index=False),
    "staysmart_ai_report.csv"
)

# ================= COPYRIGHT FOOTER =================
st.markdown("""
<div style="text-align:center; margin-top:40px; color:#94a3b8; font-size:14px;">
© 2026 EXQ-16. All Rights Reserved.
</div>
""", unsafe_allow_html=True)
