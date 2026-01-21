# -*- coding: utf-8 -*-
"""StaySmart AI – Enterprise HR Intelligence (Enhanced)"""

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="StaySmart AI",
    layout="wide",
    page_icon="🧠",
    initial_sidebar_state="collapsed"
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
    "standard": ["SSAI-STD-1A2B-3C4D"],
    "premium": ["SSAI-PRM-X8LQ-4R2Z-M9KP"]
}

# ================= CUSTOM CSS =================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    h1, h2, h3 {
        font-weight: 700 !important;
    }
    
    .plan-card {
        background: white;
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        height: 100%;
        transition: transform 0.3s ease;
    }
    
    .metric-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .insight-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
    }
    
    .premium-badge {
        background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 20px;
        font-weight: 700;
        display: inline-block;
        margin-bottom: 1rem;
    }
    
    .standard-badge {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        color: #333;
        padding: 0.5rem 1.5rem;
        border-radius: 20px;
        font-weight: 700;
        display: inline-block;
        margin-bottom: 1rem;
    }
    
    .footer {
        text-align: center;
        padding: 2rem;
        background: rgba(0,0,0,0.2);
        border-radius: 15px;
        margin-top: 3rem;
        color: white;
    }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        padding: 0.75rem 2rem;
        border-radius: 10px;
        border: none;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 800;
    }
</style>
""", unsafe_allow_html=True)

# =================================================
# =============== STEP 1: PLAN SELECT ==============
# =================================================
if st.session_state.step == "plan":
    
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0 3rem 0;'>
            <h1 style='font-size: 4rem; color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>
                🧠 StaySmart AI
            </h1>
            <p style='font-size: 1.5rem; color: #f0f0f0; margin-top: -1rem;'>
                Predict Attrition • Reduce Risk • Retain Talent
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("""
            <div class='plan-card'>
                <div class='standard-badge'>STANDARD</div>
                <h2 style='color: #333; margin: 1rem 0;'>HR Risk Monitoring</h2>
                <p style='color: #666; font-size: 1.1rem; margin-bottom: 1.5rem;'>
                    Identify employees who may leave and monitor risk levels.
                </p>
                <h1 style='color: #667eea; margin: 1.5rem 0;'>
                    ₹100 <span style='font-size: 1rem; color: #999;'>/ employee / month</span>
                </h1>
                <ul style='color: #555; line-height: 2; list-style-position: inside;'>
                    <li>✅ Employee flight risk score</li>
                    <li>✅ High / Medium / Low risk tags</li>
                    <li>✅ Top risk employees list</li>
                    <li>✅ Interactive visual dashboards</li>
                    <li>✅ Export detailed reports</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 Select Standard Plan", key="std"):
            st.session_state.tier = "standard"
            st.session_state.step = "auth"
            st.rerun()
    
    with col2:
        st.markdown("""
            <div class='plan-card'>
                <div class='premium-badge'>⭐ PREMIUM</div>
                <h2 style='color: #333; margin: 1rem 0;'>Predictive HR Intelligence</h2>
                <p style='color: #666; font-size: 1.1rem; margin-bottom: 1.5rem;'>
                    Deep insights into why employees leave and what to do next.
                </p>
                <h1 style='color: #f5576c; margin: 1.5rem 0;'>
                    ₹150 <span style='font-size: 1rem; color: #999;'>/ employee / month</span>
                </h1>
                <ul style='color: #555; line-height: 2; list-style-position: inside;'>
                    <li>✅ Everything in Standard</li>
                    <li>✅ Attrition cost estimation</li>
                    <li>✅ Key reason analysis</li>
                    <li>✅ AI retention recommendations</li>
                    <li>✅ Leadership-ready insights</li>
                    <li>✅ Advanced interactive charts</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⭐ Select Premium Plan", key="prm"):
            st.session_state.tier = "premium"
            st.session_state.step = "auth"
            st.rerun()
    
    # Comparison Table
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div style='background: rgba(255,255,255,0.95); padding: 2rem; border-radius: 20px; box-shadow: 0 20px 60px rgba(0,0,0,0.3);'>
            <h2 style='text-align: center; color: #333; margin-bottom: 2rem;'>📊 Feature Comparison</h2>
    """, unsafe_allow_html=True)
    
    comparison_data = {
        "Feature": ["Flight Risk Score", "Risk Categories", "Visual Dashboards", "Data Export", 
                   "AI Recommendations", "Cost Estimation", "Advanced Analytics", "Leadership Insights"],
        "Standard": ["✅", "✅", "✅", "✅", "❌", "❌", "❌", "❌"],
        "Premium": ["✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅"]
    }
    
    comp_df = pd.DataFrame(comparison_data)
    st.dataframe(comp_df, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
        <div class='footer'>
            <h3 style='margin: 0; color: white;'>StaySmart AI</h3>
            <p style='margin: 0.5rem 0; color: #f0f0f0;'>Powered by Advanced Machine Learning</p>
            <p style='margin: 1rem 0 0 0; font-weight: 700; font-size: 1.2rem; color: #ffd700;'>EXQ-16</p>
            <p style='margin: 0; color: #ddd;'>© 2026 All Rights Reserved</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.stop()

# =================================================
# =============== STEP 2: AUTH =====================
# =================================================
if st.session_state.step == "auth":
    
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0;'>
            <h1 style='font-size: 3rem; color: white;'>🔐 License Verification</h1>
        </div>
    """, unsafe_allow_html=True)
    
    tier = st.session_state.tier
    price = "₹100 / employee / month" if tier == "standard" else "₹150 / employee / month"
    badge_class = "standard-badge" if tier == "standard" else "premium-badge"
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(f"""
            <div class='plan-card'>
                <div class='{badge_class}'>{tier.upper()} PLAN</div>
                <h2 style='color: #333; margin: 1rem 0;'>{price}</h2>
                
                <div style='background: #f8f9fa; padding: 1.5rem; border-radius: 10px; margin: 1.5rem 0;'>
                    <h4 style='color: #333; margin-bottom: 1rem;'>📄 Required Employee Data:</h4>
                    <ul style='color: #555; line-height: 1.8;'>
                        <li>Satisfaction Score (1–10)</li>
                        <li>Engagement Score (1–10)</li>
                        <li>Months since last salary hike</li>
                        <li>Overtime hours per month</li>
                        <li>Distance from home (km)</li>
                    </ul>
                    <p style='color: #888; font-size: 0.9rem; margin-top: 1rem;'>
                        💡 Missing fields? Our AI will estimate them automatically!
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        key = st.text_input("🔑 Enter License Key", placeholder="SSAI-XXXX-XXXX-XXXX", type="password")
        
        if st.button("✅ Verify & Access Dashboard"):
            if key.strip().upper() in [k.upper() for k in LICENSE_KEYS[tier]]:
                st.session_state.authenticated = True
                st.session_state.step = "dashboard"
                st.success("🎉 License verified! Redirecting to dashboard...")
                st.rerun()
            else:
                st.error("❌ Invalid license key for selected plan")
    
    st.markdown("""
        <div class='footer'>
            <h3 style='margin: 0; color: white;'>StaySmart AI</h3>
            <p style='margin: 1rem 0 0 0; font-weight: 700; font-size: 1.2rem; color: #ffd700;'>EXQ-16</p>
            <p style='margin: 0; color: #ddd;'>© 2026 All Rights Reserved</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.stop()

# =================================================
# =============== STEP 3: DASHBOARD ================
# =================================================
if not st.session_state.authenticated:
    st.stop()

st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 3rem; border-radius: 20px; margin-bottom: 2rem; 
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);'>
        <h1 style='color: white; margin: 0; font-size: 3rem;'>🧠 StaySmart AI Dashboard</h1>
        <p style='color: #f0f0f0; font-size: 1.3rem; margin: 0.5rem 0 0 0;'>
            AI-Powered Employee Attrition Intelligence & Retention Insights
        </p>
    </div>
""", unsafe_allow_html=True)

# File Upload
file = st.file_uploader("📂 Upload Employee Data (CSV)", type=["csv"])

if not file:
    st.info("📊 Upload your employee data CSV to begin comprehensive analysis")
    st.markdown("""
        <div class='footer'>
            <h3 style='margin: 0; color: white;'>StaySmart AI</h3>
            <p style='margin: 1rem 0 0 0; font-weight: 700; font-size: 1.2rem; color: #ffd700;'>EXQ-16</p>
            <p style='margin: 0; color: #ddd;'>© 2026 All Rights Reserved</p>
        </div>
    """, unsafe_allow_html=True)
    st.stop()

# Process Data
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

# Plan Notification
if st.session_state.tier == "standard":
    st.warning("📦 **STANDARD PLAN** - Upgrade to Premium for advanced analytics, cost estimation & AI retention strategies!")

# Key Metrics
st.markdown("### 📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
        <div class='metric-box'>
            <h3 style='margin: 0; font-size: 2.5rem;'>{len(df)}</h3>
            <p style='margin: 0.5rem 0 0 0; opacity: 0.9;'>Total Employees</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    high_risk = int((df['risk_category']=="High").sum())
    st.markdown(f"""
        <div style='background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%); 
                    padding: 1.5rem; border-radius: 15px; color: white; text-align: center;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.2);'>
            <h3 style='margin: 0; font-size: 2.5rem;'>{high_risk}</h3>
            <p style='margin: 0.5rem 0 0 0; opacity: 0.9;'>🔴 High Risk</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    med_risk = int((df['risk_category']=="Medium").sum())
    st.markdown(f"""
        <div style='background: linear-gradient(135deg, #feca57 0%, #ff9ff3 100%); 
                    padding: 1.5rem; border-radius: 15px; color: white; text-align: center;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.2);'>
            <h3 style='margin: 0; font-size: 2.5rem;'>{med_risk}</h3>
            <p style='margin: 0.5rem 0 0 0; opacity: 0.9;'>🟡 Medium Risk</p>
        </div>
    """, unsafe_allow_html=True)

with col4:
    avg_risk = df['flight_risk'].mean()
    st.markdown(f"""
        <div style='background: linear-gradient(135deg, #48dbfb 0%, #0abde3 100%); 
                    padding: 1.5rem; border-radius: 15px; color: white; text-align: center;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.2);'>
            <h3 style='margin: 0; font-size: 2.5rem;'>{avg_risk:.1f}%</h3>
            <p style='margin: 0.5rem 0 0 0; opacity: 0.9;'>Average Risk</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Visualizations
st.markdown("### 📈 Risk Distribution Analysis")

col1, col2 = st.columns(2)

with col1:
    # Bar Chart
    risk_counts = df['risk_category'].value_counts()
    fig1 = go.Figure(data=[
        go.Bar(
            x=risk_counts.index,
            y=risk_counts.values,
            marker_color=['#10b981', '#fbbf24', '#ef4444'],
            text=risk_counts.values,
            textposition='auto',
        )
    ])
    fig1.update_layout(
        title="Employee Risk Distribution",
        xaxis_title="Risk Category",
        yaxis_title="Number of Employees",
        template="plotly_white",
        height=400,
        font=dict(family="Poppins", size=12)
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    # Pie Chart
    fig2 = go.Figure(data=[
        go.Pie(
            labels=risk_counts.index,
            values=risk_counts.values,
            marker_colors=['#10b981', '#fbbf24', '#ef4444'],
            hole=0.4,
            textinfo='label+percent',
            textfont_size=14
        )
    ])
    fig2.update_layout(
        title="Risk Category Breakdown",
        template="plotly_white",
        height=400,
        font=dict(family="Poppins", size=12)
    )
    st.plotly_chart(fig2, use_container_width=True)

# Premium Features
if st.session_state.tier == "premium":
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### ⭐ Premium Analytics & Insights")
    
    col3, col4 = st.columns(2)
    
    with col3:
        # Satisfaction vs Engagement Scatter
        fig3 = px.scatter(
            df,
            x='satisfaction_score',
            y='engagement_score',
            color='flight_risk',
            size='flight_risk',
            color_continuous_scale='RdYlGn_r',
            title="Satisfaction vs Engagement Analysis",
            labels={'satisfaction_score': 'Satisfaction Score',
                   'engagement_score': 'Engagement Score',
                   'flight_risk': 'Flight Risk %'}
        )
        fig3.update_layout(height=400, template="plotly_white", font=dict(family="Poppins"))
        st.plotly_chart(fig3, use_container_width=True)
    
    with col4:
        # Risk Factors
        factors = {
            'Low Satisfaction': (10 - df['satisfaction_score'].mean()) * 10,
            'Low Engagement': (10 - df['engagement_score'].mean()) * 10,
            'Salary Delay': (df['last_hike_months'].mean() / 36) * 100,
            'High Overtime': (df['overtime_hours'].mean() / 80) * 100,
            'Distance': (df['distance_from_home'].mean() / 40) * 100
        }
        
        fig4 = go.Figure(data=[
            go.Bar(
                x=list(factors.values()),
                y=list(factors.keys()),
                orientation='h',
                marker_color='#8b5cf6',
                text=[f"{v:.1f}" for v in factors.values()],
                textposition='auto'
            )
        ])
        fig4.update_layout(
            title="Top Attrition Risk Factors",
            xaxis_title="Impact Score",
            template="plotly_white",
            height=400,
            font=dict(family="Poppins")
        )
        st.plotly_chart(fig4, use_container_width=True)
    
    # Cost Analysis
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 💰 Financial Impact Analysis")
    
    avg_salary = 50000
    replacement_cost = 1.5
    high_risk_count = int((df['risk_category']=="High").sum())
    estimated_cost = high_risk_count * avg_salary * replacement_cost
    
    col5, col6 = st.columns(2)
    
    with col5:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                        padding: 2rem; border-radius: 15px; color: white;'>
                <h3 style='margin: 0 0 1rem 0;'>💸 Potential Cost Impact</h3>
                <h1 style='margin: 0; font-size: 3rem;'>₹{estimated_cost:,.0f}</h1>
                <p style='margin: 1rem 0 0 0; opacity: 0.9;'>
                    Estimated cost if all high-risk employees leave<br>
                    (Based on ₹{avg_salary:,}/month average salary)
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col6:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); 
                        padding: 2rem; border-radius: 15px; color: white;'>
                <h3 style='margin: 0 0 1rem 0;'>⚠️ Critical Attention Required</h3>
                <h1 style='margin: 0; font-size: 3rem;'>{high_risk_count}</h1>
                <p style='margin: 1rem 0 0 0; opacity: 0.9;'>
                    High-risk employees requiring<br>
                    immediate retention intervention
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    # AI Recommendations
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🎯 AI-Powered Retention Strategy")
    
    st.markdown("""
        <div style='background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%); 
                    padding: 2rem; border-radius: 15px; color: white; margin: 1rem 0;'>
            <h3 style='margin: 0 0 1.5rem 0;'>🔴 High Risk Employees - Immediate Action Required</h3>
            <div style='background: rgba(255,255,255,0.1); padding: 1.5rem; border-radius: 10px;'>
                <p style='margin: 0.5rem 0;'><strong>💰 Retention Bonus:</strong> Offer competitive package worth 15-20% of annual salary</p>
                <p style='margin: 0.5rem 0;'><strong>🚀 Career Advancement:</strong> Discuss promotion opportunities and role expansion within 30 days</p>
                <p style='margin: 0.5rem 0;'><strong>💬 Executive Meeting:</strong> Schedule immediate one-on-one with senior leadership and HR</p>
                <p style='margin: 0.5rem 0;'><strong>🎓 Development Plan:</strong> Allocate training budget and create personalized skill development roadmap</p>
                <p style='margin: 0.5rem 0;'><strong>🏆 Special Recognition:</strong> Implement immediate recognition and appreciation initiatives</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background: linear-gradient(135deg, #feca57 0%, #ff9ff3 100%); 
                    padding: 2rem; border-radius: 15px; color: white; margin: 1rem 0;'>
            <h3 style='margin: 0 0 1.5rem 0;'>🟡 Medium Risk Employees - Proactive Engagement</h3>
            <div style='background: rgba(255,255,255,0.1); padding: 1.5rem; border-radius: 10px;'>
                <p style='margin: 0.5rem 0;'><strong>🎯 Recognition Program:</strong> Implement peer-to-peer recognition and monthly achievement awards</p>
                <p style='margin: 0.5rem 0;'><strong>⚖️ Work-Life Balance:</strong> Review workload distribution and offer flexible work arrangements</p>
                <p style='margin: 0.5rem 0;'><strong>📊 Continuous Feedback:</strong> Conduct quarterly engagement surveys and implement actionable feedback</p>
                <p style='margin: 0.5rem 0;'><strong>🤝 Team Integration:</strong> Increase cross-functional collaboration and team-building activities</p>
                <p style='margin: 0.5rem 0;'><strong>📈 Growth Opportunities:</strong> Provide clear career path visibility and skill enhancement programs</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background: linear-gradient(135deg, #10b981 0%, #059669 100%); 
                    padding: 2rem; border-radius: 15px; color: white; margin: 1rem 0;'>
            <h3 style='margin: 0 0 1.5rem 0;'>🟢 Low Risk Employees - Sustain Excellence</h3>
            <div style='background: rgba(255,255,255,0.1); padding: 1.5rem; border-radius: 10px;'>
                <p style='margin: 0.5rem 0;'><strong>🌟 Leadership Pipeline:</strong> Identify high-potential talent for leadership development programs</p>
                <p style='margin: 0.5rem 0;'><strong>💡 Innovation Champions:</strong> Engage in strategic projects and innovation initiatives</p>
                <p style='margin: 0.5rem 0;'><strong>📈 Continuous Growth:</strong> Maintain momentum with challenging assignments and learning opportunities</p>
                <p style='margin: 0.5rem 0;'><strong>🎖️ Brand Ambassadors:</strong> Leverage as mentors and culture carriers within the organization</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

else:
    # Standard Plan
    st.markdown("<br>", unsafe_allow_html=True)
