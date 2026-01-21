import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random

# ==========================
# PAGE SETTINGS
# ==========================
st.set_page_config(page_title="StaySmart AI", layout="wide")

# ==========================
# SESSION STATE
# ==========================
if "step" not in st.session_state:
    st.session_state.step = "plan"
if "tier" not in st.session_state:
    st.session_state.tier = None

# ==========================
# STYLE
# ==========================
st.markdown("""
<style>
body {
    background-color: #0b0f1a;
    color: white;
}
h1, h2, h3, h4 {
    color: white;
}
.plan-card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 20px;
    padding: 20px;
    margin: 10px;
}
.badge {
    padding: 5px 10px;
    border-radius: 10px;
    font-weight: bold;
}
.standard { background: #2a6cff; }
.premium { background: #9b59b6; }
table {
    width: 100%;
    border-collapse: collapse;
}
th, td {
    padding: 10px;
    border: 1px solid rgba(255,255,255,0.15);
}
th {
    background: rgba(255,255,255,0.08);
}
</style>
""", unsafe_allow_html=True)

# ==========================
# COVER PAGE
# ==========================
if st.session_state.step == "plan":
    st.markdown("""
    <div style="text-align:center; padding:20px;">
        <h1 style="font-size:48px; font-weight:700;">StaySmart AI</h1>
        <p style="font-size:18px; color:#cbd5f5;">Predict Attrition • Reduce Risk • Retain Talent</p>
    </div>
    """ , unsafe_allow_html=True)

    st.markdown("""
    <div style="max-width:1100px; margin:auto; padding:20px;">
        <div style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.12); border-radius:20px; padding:20px;">
            <h3>What StaySmart AI Provides</h3>
            <p style="color:#cbd5f5; line-height:1.7;">
                StaySmart AI helps HR teams predict which employees may leave, why they might leave, and what actions to take to retain them.
                It uses employee data to calculate risk scores, provide insights, and recommend retention strategies that are actionable and measurable.
            </p>
            <div style="display:flex; gap:20px; justify-content:center; flex-wrap:wrap;">
                <div style="background: rgba(255,255,255,0.06); padding:15px; border-radius:20px; border:1px solid rgba(255,255,255,0.12); width:260px;">
                    <h4>1) Data Ingestion</h4>
                    <p style="color:#cbd5f5;">Upload employee CSV or connect HRMS</p>
                </div>
                <div style="background: rgba(255,255,255,0.06); padding:15px; border-radius:20px; border:1px solid rgba(255,255,255,0.12); width:260px;">
                    <h4>2) AI Risk Scoring</h4>
                    <p style="color:#cbd5f5;">Real-time attrition risk prediction</p>
                </div>
                <div style="background: rgba(255,255,255,0.06); padding:15px; border-radius:20px; border:1px solid rgba(255,255,255,0.12); width:260px;">
                    <h4>3) Retention Actions</h4>
                    <p style="color:#cbd5f5;">Get practical steps to retain talent</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="plan-card">
            <span class="badge standard">STANDARD</span>
            <h3>HR Risk Monitoring</h3>
            <p>Identify employees who may leave and monitor risk levels.</p>
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
            <h3>Predictive HR Intelligence</h3>
            <p>Deep insights into why employees leave and what to do next.</p>
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

    st.stop()

# ==========================
# AUTH (LOGIN / DATA UPLOAD)
# ==========================
if st.session_state.step == "auth":
    st.markdown("<h2>Upload Employee Data</h2>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        # REQUIRED COLUMNS CHECK
        required_cols = ["employee_id","department","satisfaction_score","flight_risk","attrition"]
        if all(col in df.columns for col in required_cols):
            st.session_state.step = "dashboard"
            st.session_state.df = df
            st.success("Data Uploaded Successfully!")
            st.experimental_rerun()
        else:
            st.error("Missing required columns. Please ensure your CSV contains: employee_id, department, satisfaction_score, flight_risk, attrition")

# ==========================
# DASHBOARD
# ==========================
if st.session_state.step == "dashboard":
    df = st.session_state.df

    st.markdown("<h1>Dashboard</h1>", unsafe_allow_html=True)

    # ----------------------------
    # Flight Risk Simulation (KEEP IT)
    # ----------------------------
    st.markdown("## Flight Risk Simulation")
    sim_score = st.slider("Select Satisfaction Score", 1, 10, 5)
    sim_overtime = st.slider("Overtime Hours", 0, 30, 10)
    sim_workload = st.slider("Workload Level (1-10)", 1, 10, 6)

    # Simple simulation logic
    base_risk = (10 - sim_score) * 8
    overtime_risk = sim_overtime * 1.2
    workload_risk = sim_workload * 3
    final_risk = min(100, base_risk + overtime_risk + workload_risk)

    st.markdown(f"### Predicted Flight Risk: **{final_risk:.2f}%**")

    # ----------------------------
    # 2 GRAPHS SIDE BY SIDE (Dark + Mature)
    # ----------------------------
    st.markdown("<br><br><h2>Insights</h2>", unsafe_allow_html=True)

    def plot_satisfaction_risk(df):
        df["satisfaction_bin"] = pd.cut(df["satisfaction_score"], bins=8)
        grouped = df.groupby("satisfaction_bin")["flight_risk"].mean().reset_index()

        fig, ax = plt.subplots(figsize=(8,4))
        ax.plot(grouped["satisfaction_bin"].astype(str), grouped["flight_risk"], marker="o", linewidth=2)
        ax.set_title("Satisfaction vs Flight Risk (Average)", color="white", fontsize=16)
        ax.set_xlabel("Satisfaction Score (Binned)", color="white")
        ax.set_ylabel("Avg Flight Risk (%)", color="white")
        ax.grid(True, linestyle="--", alpha=0.5)
        ax.tick_params(axis="x", rotation=45, colors="white")
        ax.tick_params(axis="y", colors="white")
        ax.spines["bottom"].set_color("white")
        ax.spines["top"].set_color("white")
        ax.spines["left"].set_color("white")
        ax.spines["right"].set_color("white")
        fig.patch.set_facecolor("#0b0f1a")
        ax.set_facecolor("#0b0f1a")
        return fig

    def plot_department_attrition(df):
        dept = df.groupby("department")["attrition"].mean().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(8,4))
        ax.barh(dept.index, dept.values, height=0.6)
        ax.set_title("Attrition Rate by Department", color="white", fontsize=16)
        ax.set_xlabel("Attrition Rate (%)", color="white")
        ax.set_ylabel("Department", color="white")
        ax.grid(True, axis="x", linestyle="--", alpha=0.5)
        ax.tick_params(axis="x", colors="white")
        ax.tick_params(axis="y", colors="white")
        ax.spines["bottom"].set_color("white")
        ax.spines["top"].set_color("white")
        ax.spines["left"].set_color("white")
        ax.spines["right"].set_color("white")
        fig.patch.set_facecolor("#0b0f1a")
        ax.set_facecolor("#0b0f1a")
        return fig

    col1, col2 = st.columns(2)

    with col1:
        st.pyplot(plot_satisfaction_risk(df))

    with col2:
        st.pyplot(plot_department_attrition(df))

    # ----------------------------
    # PREMIUM INSIGHTS (Retention Recommendations)
    # ----------------------------
    if st.session_state.tier == "premium":
        st.markdown("<br><br><h2>Retention Recommendations</h2>", unsafe_allow_html=True)

        # Immediate
        st.markdown("### 🔥 Immediate Actions")
        st.write("""
        - Have a one-on-one conversation within 24 hours  
        - Provide immediate recognition for recent performance  
        - Clarify role expectations & workload  
        - Resolve any pending HR issues immediately  
        """)

        # Short-term
        st.markdown("### ⏳ Short Term (1-4 weeks)")
        st.write("""
        - Offer flexible work schedule / WFH options  
        - Provide training / upskilling opportunities  
        - Create clear career path discussion  
        - Reduce overtime and redistribute workload  
        """)

        # Long-term
        st.markdown("### 🧠 Long Term (1-6 months)")
        st.write("""
        - Launch mentorship & leadership development  
        - Improve internal mobility & promotion pipeline  
        - Conduct employee engagement surveys quarterly  
        - Build strong culture & recognition programs  
        """)

    st.markdown("<br><br><h2>Footer</h2>", unsafe_allow_html=True)
    st.write("StaySmart AI • Built for HR Teams")

