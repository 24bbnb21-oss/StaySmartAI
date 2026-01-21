import streamlit as st
import pandas as pd
import numpy as np

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="StaySmart AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- SESSION STATE ----------------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "plan" not in st.session_state:
    st.session_state.plan = None

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False


# ---------------- NAVIGATION ----------------
def go(page):
    st.session_state.page = page
    st.experimental_rerun()


st.markdown("""
<style>
.big-title { font-size: 42px; font-weight: 800; }
.sub { font-size: 18px; color: #aaa; }
.card {
    padding: 25px;
    border-radius: 16px;
    background: #111;
    border: 1px solid #222;
}
</style>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("🏠 Home"):
        go("home")
with col2:
    if st.button("📊 Dashboard"):
        go("dashboard")
with col3:
    if st.button("💼 Plans"):
        go("plans")
with col4:
    if st.button("ℹ️ About"):
        go("about")


# ---------------- HOME ----------------
if st.session_state.page == "home":
    st.markdown('<div class="big-title">StaySmart AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub">Predict. Retain. Optimize your workforce.</div>', unsafe_allow_html=True)
    st.write("")
    st.success("AI-powered employee attrition intelligence")


# ---------------- PLANS ----------------
elif st.session_state.page == "plans":
    st.markdown("## Choose Your Plan")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("### Standard")
        st.markdown("""
        - Attrition Risk Score  
        - Basic Insights  
        - CSV Upload  
        """)
        if st.button("Select Standard"):
            st.session_state.plan = "standard"
            st.session_state.authenticated = True
            go("dashboard")

    with c2:
        st.markdown("### Premium 🚀")
        st.markdown("""
        - Everything in Standard  
        - Advanced Retention Strategy  
        - Risk Simulator  
        - Timeline-based Actions  
        """)
        if st.button("Select Premium"):
            st.session_state.plan = "premium"
            st.session_state.authenticated = True
            go("dashboard")


# ---------------- DASHBOARD ----------------
elif st.session_state.page == "dashboard":

    if not st.session_state.authenticated:
        st.warning("Please select a plan first.")
        go("plans")

    st.markdown("## StaySmart AI Dashboard")
    st.caption(f"Active Plan: **{st.session_state.plan.upper()}**")

    file = st.file_uploader("Upload Employee CSV", type=["csv"])

    if file:
        df = pd.read_csv(file)

        if "Attrition" not in df.columns:
            st.error("CSV must contain an 'Attrition' column")
            st.stop()

        # ----- Risk Score (Mock AI Logic) -----
        np.random.seed(42)
        df["Risk Score"] = np.random.randint(20, 95, size=len(df))

        high_risk = df[df["Risk Score"] > 70]

        st.metric("Employees Analyzed", len(df))
        st.metric("High Risk Employees", len(high_risk))

        st.subheader("Risk Distribution")
        st.bar_chart(df["Risk Score"])

        # -------- STANDARD INSIGHTS --------
        if st.session_state.plan == "standard":
            st.subheader("Standard Insights")
            st.info("""
            - Employees with risk >70 should be monitored  
            - Focus on engagement and feedback  
            - Review workload and team satisfaction  
            """)

        # -------- PREMIUM INSIGHTS --------
        if st.session_state.plan == "premium":
            st.subheader("Premium Retention Strategy")

            st.markdown("### 🔴 Immediate (0–30 days)")
            st.success("""
            - Manager 1:1 meetings  
            - Compensation review  
            - Burnout assessment  
            """)

            st.markdown("### 🟠 Short Term (1–3 months)")
            st.success("""
            - Skill upskilling programs  
            - Internal mobility options  
            - Recognition incentives  
            """)

            st.markdown("### 🟢 Long Term (3–12 months)")
            st.success("""
            - Leadership track planning  
            - Retention bonuses  
            - Career roadmap alignment  
            """)

            st.markdown("### ⚠️ Risk Simulator")
            attrition_rate = st.slider("Projected Attrition %", 5, 40, 15)
            impact = attrition_rate * 1.4

            st.warning(f"Estimated business impact score: **{impact:.2f}**")

        st.download_button(
            "Download Report",
            df.to_csv(index=False),
            "staysmart_report.csv"
        )

    else:
        st.info("Upload a CSV to begin analysis.")


# ---------------- ABOUT ----------------
elif st.session_state.page == "about":
    st.markdown("## About StaySmart AI")
    st.markdown("""
    **StaySmart AI** helps organizations proactively reduce employee attrition using:
    
    - Predictive analytics  
    - Behavioral risk modeling  
    - Actionable retention strategies  

    Built for HR leaders who want **clarity, not complexity**.
    """)

    st.caption("© 2026 StaySmart AI — All rights reserved")
