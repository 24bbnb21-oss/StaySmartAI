import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Your Dashboard")

# Sample data (Replace with your actual data)
data = {
    "Category": ["A", "B", "C", "D"],
    "Value": [10, 20, 30, 40]
}
df = pd.DataFrame(data)

st.write("### Data Table")
st.dataframe(df)

# ---- MATPLOTLIB BAR CHART ----
st.write("### Bar Chart")

fig, ax = plt.subplots()
ax.bar(df["Category"], df["Value"])
ax.set_xlabel("Category")
ax.set_ylabel("Value")
ax.set_title("Bar Chart")

st.pyplot(fig)

# ---- MATPLOTLIB LINE CHART ----
st.write("### Line Chart")

fig2, ax2 = plt.subplots()
ax2.plot(df["Category"], df["Value"], marker='o')
ax2.set_xlabel("Category")
ax2.set_ylabel("Value")
ax2.set_title("Line Chart")

st.pyplot(fig2)
