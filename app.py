import streamlit as st

st.set_page_config(
    page_title="Your App Name",
    page_icon="🧠",
    layout="wide"
)

# ---- HEADER ----
st.title("Your App Title")
st.write("Your subtitle goes here")

# ---- ABOUT US ----
st.header("About Us")
st.write("""
We’re a team of creators and builders focused on helping you grow your online presence with sleek, modern tools and designs. From website templates to branding assets, we make it easy to launch and scale your projects.
""")

# ---- WEBSITE MOCKUP SECTION (Replaces Risk Chart) ----
st.header("Featured Website")
st.write("A cool preview of a modern website layout.")

col1, col2 = st.columns(2)

with col1:
    st.image(
        "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=1200&q=80",
        caption="Website Mockup",
        use_column_width=True
    )
    st.write("**YourBrand.com** — Clean, modern landing page with hero section, testimonials, and pricing.")

with col2:
    st.image(
        "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=80",
        caption="Live Demo Preview",
        use_column_width=True
    )
    st.write("**Live Demo** — Aesthetic design with responsive layout and smooth interactions.")

# ---- SPACE BEFORE PLANS ----
st.write("")
st.write("")
st.write("")
st.write("")

# ---- PLANS ----
st.header("Plans")
st.write("Choose the best plan for you.")
