# -*- coding: utf-8 -*-
"""StaySmart AI – Enterprise HR Intelligence (Enhanced)"""

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

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

# ================= ENHANCED STYLES WITH ANIMATIONS =================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

body { 
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    animation: gradientShift 15s ease infinite;
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.hero {
    text-align: center;
    padding: 80px 20px 40px;
    animation: fadeInDown 1s ease;
}

@keyframes fadeInDown {
    from {
        opacity: 0;
        transform: translateY(-30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.hero h1 {
    font-size: 64px;
    font-weight: 800;
    background: linear-gradient(135deg, #ffffff 0%, #e0e7ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 15px;
    text-shadow: 0 4px 20px rgba(255,255,255,0.3);
}

.hero p {
    font-size: 22px;
    color: #e0e7ff;
    font-weight: 500;
    letter-spacing: 0.5px;
}

.plan-card {
    background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
    padding: 45px;
    border-radius: 32px;
    box-shadow: 0 35px 80px rgba(0,0,0,0.25), 0 10px 30px rgba(0,0,0,0.15);
    height: 100%;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    border: 1px solid rgba(255,255,255,0.5);
    position: relative;
    overflow: hidden;
    animation: fadeInUp 0.8s ease;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.plan-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 6px;
    background: linear-gradient(90deg, #4f46e5, #7c3aed);
    opacity: 0;
    transition: opacity 0.3s ease;
}

.plan-card:hover::before {
    opacity: 1;
}

.plan-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 45px 100px rgba(0,0,0,0.35), 0 15px 40px rgba(79,70,229,0.2);
}

.plan-title {
    font-size: 32px;
    font-weight: 800;
    color: #0f172a;
    margin-top: 20px;
    margin-bottom: 10px;
}

.plan-desc {
    color: #475569;
    font-size: 17px;
    margin: 15px 0 25px;
    line-height: 1.6;
}

.price {
    font-size: 48px;
    font-weight: 800;
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 25px 0;
}

ul {
    padding-left: 0;
    list-style: none;
    color: #334155;
    font-size: 16px;
}

li {
    margin-bottom: 12px;
    padding-left: 30px;
    position: relative;
    line-height: 1.5;
}

li::before {
    content: '✓';
    position: absolute;
    left: 0;
    color: #10b981;
    font-weight: 800;
    font-size: 18px;
}

.badge {
    padding: 10px 22px;
    border-radius: 25px;
    font-weight: 700;
    display: inline-block;
    font-size: 13px;
    letter-spacing: 1px;
    text-transform: uppercase;
    animation: pulse 2s ease infinite;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}

.standard { 
    background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
    color: #1e40af;
    box-shadow: 0 4px 15px rgba(30,64,175,0.2);
}

.premium { 
    background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
    color: #92400e;
    box-shadow: 0 4px 15px rgba(146,64,14,0.2);
}

.req-box {
    background: linear-gradient(145deg, #1e293b 0%, #0f172a 100%);
    color: #e5e7eb;
    padding: 35px;
    border-radius: 24px;
    margin-top: 35px;
    border: 1px solid #334155;
    box-shadow: 0 10px 40px rgba(0,0,0,0.3);
}

.req-box h4 {
    margin-bottom: 20px;
    font-size: 20px;
    color: #f1f5f9;
}

.req-box li {
    color: #cbd5e1;
}

.req-box li::before {
    color: #60a5fa;
}

.compare {
    background: linear-gradient(145deg, #1e293b 0%, #0f172a 100%);
    padding: 35px;
    border-radius: 28px;
    margin-top: 40px;
    border: 1px solid #334155;
    box-shadow: 0 20px 60px rgba(0,0,0,0.4);
    animation: fadeIn 1s ease;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

.compare h3 {
    color: #fff;
    margin-bottom: 25px;
    font-size: 28px;
    font-weight: 700;
}

.compare table {
    width: 100%;
    border-collapse: collapse;
    border-radius: 12px;
    overflow: hidden;
}

.compare th, .compare td {
    border: 1px solid #334155;
    padding: 16px;
    text-align: center;
    color: #cbd5e1;
    transition: background 0.3s ease;
}

.compare th {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
    color: #fff;
    font-weight: 700;
    font-size: 16px;
}

.compare td {
    background: #0b1220;
}

.compare tr:hover td {
    background: #1e293b;
}

.check {
    color: #34d399;
    font-weight: 700;
    font-size: 20px;
}

.cross {
    color: #fca5a5;
    font-weight: 700;
    font-size: 20px;
}

.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
    color: white;
    border: none;
    padding: 16px 32px;
    font-size: 16px;
    font-weight: 700;
    border-radius: 16px;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 10px 30px rgba(79,70,229,0.3);
    margin-top: 20px;
}

.stButton > button:hover {
    transform: translateY(-3px);
    box-shadow: 0 15px 40px rgba(79,70,229,0.4);
}

.dashboard-header {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
    padding: 50px;
    border-radius: 32px;
    margin-bottom: 40px;
    box-shadow: 0 20px 60px rgba(79,70,229,0.4);
    animation: fadeInDown 0.8s ease;
}

.dashboard-header h1 {
    color: white;
    font-size: 48px;
    font-weight: 800;
    margin-bottom: 10px;
}

.dashboard-header p {
    color: #e0e7ff;
    font-size: 20px;
    font-weight: 500;
}

.metric-card {
    background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
    padding: 30px;
    border-radius: 24px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    border: 1px solid #e2e8f0;
    text-align: center;
    transition: all 0.3s ease;
}

.metric-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 50px rgba(0,0,0,0.15);
}

.insight-card {
    background: linear-gradient(145deg, #ffffff 0%, #fefce8 100%);
    padding: 35px;
    border-radius: 24px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    margin: 20px 0;
    border-left: 6px solid #eab308;
    animation: slideInRight 0.6s ease;
}

@keyframes slideInRight {
    from {
        opacity: 0;
        transform: translateX(30px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

.footer {
    text-align: center;
    padding: 40px 20px;
    margin-top: 60px;
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    border-radius: 24px;
    border-top: 3px solid #4f46e5;
    animation: fadeIn 1s ease;
}

.footer-content {
    color: #94a3b8;
    font-size: 15px;
    line-height: 1.8;
}

.footer-brand {
    color: #e0e7ff;
    font-weight: 700;
    font-size: 16px;
    margin-bottom: 8px;
}

.footer-team {
    color: #4f46e5;
    font-weight: 800;
    font-size: 18px;
    letter-spacing: 2px;
}
</style>
""", unsafe_allow_html=True)

# =================================================
# =============== STEP 1: PLAN SELECT ===============
# =================================================
if st.session_state.step == "plan":

    st.markdown("""
    <div class="hero">
        <h1>🧠 StaySmart AI</h1>
        <p>Predict Attrition • Reduce Risk • Retain Talent</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
        <div class="plan-card">
            <span class="badge standard">STANDARD</span>
            <div class="plan-title">HR Risk Monitoring</div>
            <div class="plan-desc">
                Identify employees who may leave and monitor risk levels with precision.
            </div>
            <div class="price">₹100 <span style="font-size:18px; font-weight:600; color:#64748b;">/ employee / month</span></div>
            <ul>
                <li>Employee flight risk score</li>
                <li>High / Medium / Low risk tags</li>
                <li>Top risk employees list</li>
                <li>Clear visual dashboards</li>
                <li>Export detailed reports</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Select Standard Plan", key="std_plan"):
            st.session_state.tier = "standard"
            st.session_state.step = "auth"
            st.rerun()

    with col2:
        st.markdown("""
        <div class="plan-card">
            <span class="badge premium">PREMIUM</span>
            <div class="plan-title">Predictive HR Intelligence</div>
            <div class="plan-desc">
                Deep insights into why employees leave and personalized retention strategies.
            </div>
            <div class="price">₹150 <span style="font-size:18px; font-weight:600; color:#64748b;">/ employee / month</span></div>
            <ul>
                <li>Everything in Standard</li>
                <li>Attrition cost estimation</li>
                <li>Key reason analysis</li>
                <li>AI-powered retention recommendations</li>
                <li>Leadership-ready insights</li>
                <li>Advanced analytics & visualizations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Select Premium Plan", key="prm_plan"):
            st.session_state.tier = "premium"
            st.session_state.step = "auth"
            st.rerun()

    # ================= COMPARISON TABLE =================
    st.markdown("""
    <div class="compare">
        <h3>📊 Detailed Plan Comparison</h3>
        <table>
            <tr>
                <th>Feature</th>
                <th>Standard</th>
                <th>Premium</th>
            </tr>
            <tr>
                <td><strong>Flight Risk Score</strong></td>
                <td class="check">✔</td>
                <td class="check">✔</td>
            </tr>
            <tr>
                <td><strong>Risk Categories</strong></td>
                <td class="check">✔</td>
                <td class="check">✔</td>
            </tr>
            <tr>
                <td><strong>Visual Dashboards</strong></td>
                <td class="check">✔</td>
                <td class="check">✔</td>
            </tr>
            <tr>
                <td><strong>Data Export</strong></td>
                <td class="check">✔</td>
                <td class="check">✔</td>
            </tr>
            <tr>
                <td><strong>AI Retention Recommendations</strong></td>
                <td class="cross">✘</td>
                <td class="check">✔</td>
            </tr>
            <tr>
                <td><strong>Attrition Cost Estimation</strong></td>
                <td class="cross">✘</td>
                <td class="check">✔</td>
            </tr>
            <tr>
                <td><strong>Advanced Analytics</strong></td>
                <td class="cross">✘</td>
                <td class="check">✔</td>
            </tr>
            <tr>
                <td><strong>Leadership Insights</strong></td>
                <td class="cross">✘</td>
                <td class="check">✔</td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

    # ================= FOOTER =================
    st.markdown("""
    <div class="footer">
        <div class="footer-brand">StaySmart AI - Enterprise HR Intelligence Platform</div>
        <div class="footer-content">
            Powered by Advanced Machine Learning & Predictive Analytics
        </div>
        <div style="margin-top: 20px;">
            <div class="footer-team">EXQ-16</div>
            <div class="footer-content">© 2026 All Rights Reserved</div>
        </div>
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
    <div class="plan-card" style="max-width:700px; margin:60px auto;">
        <span class="badge {'standard' if tier=='standard' else 'premium'}">
            {tier.upper()} PLAN
        </span>
        <p style="margin-top:15px; font-weight:700; color:#334155; font-size:18px">{price}</p>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="req-box">
        <h4>📄 Employee Data Requirements</h4>
        <ul>
            <li>Satisfaction Score (1–10)</li>
            <li>Engagement Score (1–10)</li>
            <li>Months since last salary hike</li>
            <li>Overtime hours per month</li>
            <li>Distance from home (km)</li>
        </ul>
        <p style="font-size:15px; color:#94a3b8; margin-top:20px;">
        💡 Missing fields? Our AI will intelligently estimate them for accurate predictions.
        </p>
    </div>
    """, unsafe_allow_html=True)

    key = st.text_input(
        "🔐 Enter License Key",
        placeholder="SSAI-XXXX-XXXX-XXXX",
        type="password"
    )

    if st.button("Verify & Open Dashboard", key="verify_btn"):
        if key.strip().upper() in [k.upper() for k in LICENSE_KEYS[tier]]:
            st.session_state.authenticated = True
            st.session_state.step = "dashboard"
            st.session_state.nav = "Dashboard"
            st.success("✅ License verified successfully!")
            st.rerun()
        else:
            st.error("❌ Invalid license key for selected plan")

    st.markdown("</div>", unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <div class="footer-brand">StaySmart AI - Enterprise HR Intelligence Platform</div>
        <div style="margin-top: 20px;">
            <div class="footer-team">EXQ-16</div>
            <div class="footer-content">© 2026 All Rights Reserved</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.stop()

# =================================================
# =============== STEP 3: DASHBOARD ================
# =================================================
if not st.session_state.authenticated:
    st.stop()

st.markdown("""
<div class="dashboard-header">
    <h1>🧠 StaySmart AI Dashboard</h1>
    <p>AI-Powered Employee Attrition Intelligence & Retention Insights</p>
</div>
""", unsafe_allow_html=True)

# ================= FILE UPLOAD =================
file = st.file_uploader("📂 Upload Employee Data (CSV)", type=["csv"])
if not file:
    st.info("📊 Upload your employee data CSV to begin comprehensive analysis")
    st.markdown("""
    <div class="footer">
        <div class="footer-brand">StaySmart AI - Enterprise HR Intelligence Platform</div>
        <div style="margin-top: 20px;">
            <div class="footer-team">EXQ-16</div>
            <div class="footer-content">© 2026 All Rights Reserved</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
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

# ================= PLAN FEATURE NOTIFICATION =================
if st.session_state.tier == "standard":
    st.warning("📦 You are using the STANDARD plan. Upgrade to Premium for advanced analytics, cost estimation & AI retention recommendations.")

# ================= KEY METRICS =================
st.markdown("### 📊 Key Metrics Overview")
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <h2 style="color:#4f46e5; font-size:42px; margin:0;">{len(df)}</h2>
        <p style="color:#64748b; margin:10px 0 0;">Total Employees</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    high_risk = int((df['risk_category']=="High").sum())
    st.markdown(f"""
    <div class="metric-card">
        <h2 style="color:#dc2626; font-size:42px; margin:0;">{high_risk}</h2>
        <p style="color:#64748b; margin:10px 0 0;">High Risk</p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    med_risk = int((df['risk_category']=="Medium").sum())
    st.markdown(f"""
    <div class="metric-card">
        <h2 style="color:#f59e0b; font-size:42px; margin:0;">{med_risk}</h2>
        <p style="color:#64748b; margin:10px 0 0;">Medium Risk</p>
    </div>
    """, unsafe_allow_html=True)

with c4:
    avg_risk = df['flight_risk'].mean()
    st.markdown(f"""
    <div class="metric-card">
        <h2 style="color:#4f46e5; font-size:42px; margin:0;">{avg_risk:.1f}%</h2>
        <p style="color:#64748b; margin:10px 0 0;">Avg Risk Score</p>
    </div>
    """, unsafe_allow_html=True)

# ================= VISUALIZATIONS =================
st.markdown("---")
st.markdown("### 📈 Risk Distribution Analysis")

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(8, 6))
    colors = ['#10b981', '#f59e0b', '#dc2626']
    risk_counts = df['risk_category'].value_counts()
    ax.bar(risk_counts.index, risk_counts.values, color=colors, alpha=0.8, edgecolor='white', linewidth=2)
    ax.set_xlabel('Risk Category', fontsize=13, fontweight='bold')
    ax.set_ylabel('Number of Employees', fontsize=13, fontweight='bold')
    ax.set_title('Employee Risk Distribution', fontsize=15, fontweight='bold', pad=20)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    st.pyplot(fig)

with col2:
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    colors2 = ['#10b981', '#f59e0b', '#dc2626']
    wedges, texts, autotexts = ax2.pie(
        df['risk_category'].value_counts().values,
        labels=df['risk_category'].value_counts().index,
        autopct='%1.1f%%',
        colors=colors2,
        startangle=90,
        textprops={'fontsize': 12, 'fontweight': 'bold'}
    )
    ax2.set_title('Risk Category Distribution', fontsize=15, fontweight='bold', pad=20)
    st.pyplot(fig2)

# ================= PREMIUM FEATURES =================
if st.session_state.tier == "premium":
    st.markdown("---")
    st.markdown("### 🎯 Premium Insights & Analytics")
    
    # Advanced visualizations
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("#### Satisfaction vs Engagement")
        fig3, ax3 = plt.subplots(figsize=(8, 6))
        scatter = ax3.scatter(
            df['satisfaction_score'],
            df['engagement_score'],
            c=df['flight_risk'],
            cmap='RdYlGn_r',
            s=100,
            alpha=0.6,
            edgecolors='white',
            linewidth=1
        )
        ax3.set_xlabel('Satisfaction Score', fontsize=12, fontweight='bold')
        ax3.set_ylabel('Engagement Score', fontsize=12, fontweight='bold')
        ax3.set_title('Employee Satisfaction vs Engagement', fontsize=14, fontweight='bold', pad=15)
        ax3.grid(alpha=0.3, linestyle='--')
        plt.colorbar(scatter, label='Flight Risk %')
        plt.tight_layout()
        st.pyplot(fig3)
    
    with col4:
        st.markdown("#### Top Risk Factors")
        factors = {
            'Low Satisfaction': (10 - df['satisfaction_score'].mean()) * 10,
            'Low Engagement': (10 - df['engagement_score'].mean()) * 10,
            'Salary Delay': (df['last_hike_months'].mean() / 36) * 100,
            'High Overtime': (df['overtime_hours'].mean() / 80) * 100,
            'Distance': (df['distance_from_home'].mean() / 40) * 100
        }
        fig4, ax4 = plt.subplots(figsize=(8, 6))
        ax4.barh(list(factors.keys()), list(factors.values()), color='#7c3aed', alpha=0.8)
        ax4.set_xlabel('Impact Score', fontsize=12, fontweight='bold')
        ax4.set_title('Key Attrition Risk Factors', fontsize=14, fontweight='bold', pad=15)
        ax4.grid(axis='x', alpha=0.3, linestyle='--')
        plt.tight_layout()
        st.pyplot(fig4)
    
    # Cost Estimation
    st.markdown("---")
    st.markdown("### 💰 Attrition Cost Analysis")
    
    avg_salary = 50000  # Default average monthly salary
    replacement_cost_multiplier = 1.5
    high_risk_count = int((df['risk_category']=="High").sum())
    estimated_cost = high_risk_count * avg_salary * replacement_cost_multiplier
    
    col5, col6 = st.columns(2)
    
    with col5:
        st.markdown(f"""
        <div class="insight-card">
            <h3 style="color:#92400e; margin:0 0 15px;">💸 Potential Cost Impact</h3>
            <h2 style="color:#0f172a; font-size:38px; margin:10px 0;">₹{estimated_cost:,.0f}</h2>
            <p style="color:#64748b; margin:10px 0 0;">Estimated cost if high-risk employees leave (based on ₹{avg_salary:,}/month avg salary)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col6:
        st.markdown(f"""
        <div class="insight-card">
            <h3 style="color:#92400e; margin:0 0 15px;">⚠️ At-Risk Employees</h3>
            <h2 style="color:#0f172a; font-size:38px; margin:10px 0;">{high_risk_count}</h2>
            <p style="color:#64748b; margin:10px 0 0;">Employees requiring immediate retention action</p>
        </div>
        """, unsafe_allow_html=True)
    
    # AI Recommendations
    st.markdown("---")
    st.markdown("### 🎯 AI-Powered Retention Recommendations")
    
    st.markdown("""
    <div class="insight-card">
        <h4 style="color:#0f172a; margin:0 0 20px;">🔴 High Risk Employees (Immediate Action)</h4>
        <ul style="list-style:none; padding:0;">
            <li style="padding:10px 0; border-bottom:1px solid #e2e8f0;">
                <strong>💰 Retention Bonus:</strong> Offer competitive retention package worth 15-20% of annual salary
            </li>
            <li style="padding:10px 0; border-bottom:1px solid #e2e8f0;">
                <strong>🚀 Career Path:</strong> Discuss promotion opportunities and role expansion
            </li>
            <li style="padding:10px 0; border-bottom:1px solid #e2e8f0;">
                <strong>💬 One-on-One:</strong> Schedule immediate meeting with manager and HR
            </li>
            <li style="padding:10px 0;">
                <strong>🎓 Development:</strong> Provide training budget and skill development opportunities
            </li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="insight-card" style="background: linear-gradient(145deg, #ffffff 0%, #fef3c7 100%); border-left-color:#f59e0b;">
        <h4 style="color:#0f172a; margin:0 0 20px;">🟡 Medium Risk Employees (Proactive Engagement)</h4>
        <ul style="list-style:none; padding:0;">
            <li style="padding:10px 0; border-bottom:1px solid #e2e8f0;">
                <strong>🎯 Recognition:</strong> Implement peer recognition and achievement rewards program
            </li>
            <li style="padding:10px 0; border-bottom:1px solid #e2e8f0;">
                <strong>⚖️ Work-Life Balance:</strong> Review workload and offer flexible arrangements
            </li>
            <li style="padding:10px 0; border-bottom:1px solid #e2e8f0;">
                <strong>📊 Feedback:</strong> Conduct quarterly engagement surveys and act on results
            </li>
            <li style="padding:10px 0;">
                <strong>🤝 Team Building:</strong> Increase team collaboration and social activities
            </li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="insight-card" style="background: linear-gradient(145deg, #ffffff 0%, #d1fae5 100%); border-left-color:#10b981;">
        <h4 style="color:#0f172a; margin:0 0 20px;">🟢 Low Risk Employees (Maintain Momentum)</h4>
        <ul style="list-style:none; padding:0;">
            <li style="padding:10px 0; border-bottom:1px solid #e2e8f0;">
                <strong>🌟 Leadership:</strong> Identify and nurture high-potential talent for leadership roles
            </li>
            <li style="padding:10px 0; border-bottom:1px solid #e2e8f0;">
                <strong>💡 Innovation:</strong> Encourage participation in innovation projects and initiatives
            </li>
            <li style="padding:10px 0;">
                <strong>📈 Growth:</strong> Continue providing growth opportunities and challenging work
            </li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

else:
    # Standard Plan Limited Insights
    st.markdown("---")
    st.markdown("### 📋 Risk Analysis Summary")
    
    st.markdown("""
    <div class="insight-card">
        <h4 style="color:#0f172a; margin:0 0 15px;">✅ Analysis Complete</h4>
        <p style="color:#64748b; font-size:16px; line-height:1.8;">
            Your employee risk analysis is ready. The dashboard shows flight risk scores and categorization 
            for all employees. High-risk employees need immediate attention to prevent attrition.
        </p>
        <p style="color:#64748b; font-size:16px; line-height:1.8; margin-top:15px;">
            <strong>💡 Want more insights?</strong> Upgrade to Premium to access:
        </p>
        <ul style="margin-top:10px;">
            <li>💰 Detailed attrition cost estimation</li>
            <li>🎯 AI-powered retention recommendations</li>
            <li>📊 Advanced analytics and visualizations</li>
            <li>📈 Leadership-ready strategic insights</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ================= TOP RISK EMPLOYEES =================
st.markdown("---")
st.markdown("### 🚨 Top 10 High-Risk Employees")

top_risk = df.nlargest(10, 'flight_risk')[['flight_risk', 'risk_category', 'satisfaction_score', 'engagement_score']]
top_risk.index = range(1, len(top_risk) + 1)

st.dataframe(
    top_risk.style.background_gradient(cmap='RdYlGn_r', subset=['flight_risk'])
                  .format({'flight_risk': '{:.0f}%', 'satisfaction_score': '{:.1f}', 'engagement_score': '{:.1f}'}),
    use_container_width=True
)

# ================= DOWNLOAD REPORT =================
st.markdown("---")
st.download_button(
    "📥 Download Complete Analysis Report (CSV)",
    df.to_csv(index=False),
    "staysmart_ai_full_report.csv",
    mime="text/csv"
)

# ================= FOOTER =================
st.markdown("""
<div class="footer">
    <div class="footer-brand">StaySmart AI - Enterprise HR Intelligence Platform</div>
    <div class="footer-content">
        Powered by Advanced Machine Learning & Predictive Analytics
    </div>
    <div style="margin-top: 20px;">
        <div class="footer-team">EXQ-16</div>
        <div class="footer-content">© 2026 All Rights Reserved</div>
    </div>
</div>
""", unsafe_allow_html=True)
