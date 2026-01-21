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
/* ... keep all previous CSS unchanged ... */

.footer {
    text-align:center;
    margin-top:40px;
    color:#94a3b8;
    font-size:14px;
}

.website-box {
    background: rgba(15,23,42,0.85);
    padding:25px;
    border-radius:25px;
    border: 1px solid rgba(255,255,255,0.12);
    margin-top:25px;
}

.website-box h3 {
    margin-top:0;
    color:#fff;
}

.website-box p {
    color:#cbd5f5;
}

.website-box img {
    border-radius:18px;
    border: 1px solid rgba(255,255,255,0.12);
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

    # ======= PROFESSIONAL FRONT PAGE CONTENT =======
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

    # ======= NEW COOL WEBSITE SECTION =======
    st.markdown("""
    <div class="website-box fade" style="max-width:1000px;margin:auto;">
        <h3>Live Dashboard Preview</h3>
        <p>Experience a clean, modern HR dashboard layout designed for fast decision making.</p>
        <div style="display:flex; gap:20px; justify-content:center; flex-wrap:wrap;">
            <img src="https://img.icons8.com/fluency/96/000000/combo-chart.png"/>
            <img src="https://img.icons8.com/fluency/96/000000/data-sheet.png"/>
            <img src="https://img.icons8.com/fluency/96/000000/analytics.png"/>
        </div>
        <p style="margin-top:15px;color:#94a3b8">
        Secure, scalable, and built for enterprises.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ======= SPACE BEFORE PLANS =======
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
    st.markdown("## 📈 Risk Breakdown")
    fig2, ax2 = plt.subplots()
    df['risk_category'].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax2)
    ax2.set_ylabel('')
    st.pyplot(fig2)

    st.markdown("## 🧩 Retention Recommendations")
    st.write("Top retention actions based on risk score:")
    st.write("- High Risk: Offer retention bonus or role change")
    st.write("- Medium Risk: Increase engagement & recognition")
    st.write("- Low Risk: Keep motivation high")

st.download_button(
    "⬇️ Download Full Report",
    df.to_csv(index=False),
    "staysmart_ai_report.csv"
)

# ================= ABOUT US FOOTER =================
st.markdown("""
<div class="footer">
<b>About Us</b><br>
StaySmart AI is a HR intelligence tool built for modern enterprises. Our AI predicts attrition risk and helps HR teams retain top talent using data-driven insights.<br>
© 2026 EXQ-16. All Rights Reserved.
</div>
""", unsafe_allow_html=True)
