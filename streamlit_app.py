import streamlit as st

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Tata Motors Sentiment Dashboard", layout="wide")

# ---------- CUSTOM CSS FOR BACKGROUND ----------
page_bg = """
<style>
    .stApp {
        background-color: #e6f0fa; /* light blue shade */
    }
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ---------- HEADER SECTION ----------
col_logo, col_header = st.columns([1, 8])
with col_logo:
    st.image("notebooks/data/tataimg.png", width=120)

with col_header:
    st.markdown(
        """
        <h1 style='text-align: left; color: #1769aa; margin-bottom:0px;'>
            Tata Motors Social Sentiment Dashboard
        </h1>
        <p style='text-align: left; color: #222; font-size:16px; margin-top:0px;'>
            Real-time Sentiment Analysis across multiple platforms
        </p>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# ---------- PLATFORM SELECTION ROW ----------
st.markdown("### 📊 Select a Platform")

col1, col2, col3 = st.columns(3)

with col1:
    img_col, txt_col = st.columns([1, 2])
    with img_col:
        st.image("notebooks/data/yt.png", width=70)
    with txt_col:
        st.markdown(
            "<div style='display:flex;align-items:center;height:70px;'>"
            "<span style='font-size:20px;font-weight:600;text-align:left;margin-left:8px;'>YouTube</span>"
            "</div>", unsafe_allow_html=True
        )

with col2:
    img_col, txt_col = st.columns([1, 2])
    with img_col:
        st.image("notebooks/data/reddit.png", width=70)
    with txt_col:
        st.markdown(
            "<div style='display:flex;align-items:center;height:70px;'>"
            "<span style='font-size:20px;font-weight:600;text-align:left;margin-left:8px;'>Reddit</span>"
            "</div>", unsafe_allow_html=True
        )

with col3:
    img_col, txt_col = st.columns([1, 2])
    with img_col:
        st.image("notebooks/data/tele.png", width=70)
    with txt_col:
        st.markdown(
            "<div style='display:flex;align-items:center;height:70px;'>"
            "<span style='font-size:20px;font-weight:600;text-align:left;margin-left:8px;'>Telegram</span>"
            "</div>", unsafe_allow_html=True
        )

st.markdown("<br>", unsafe_allow_html=True)

# ---------- DASHBOARD TOGGLE ----------
dashboard = st.radio(
    "📌 Choose sentiment dashboard:",
    ["YouTube", "Reddit", "Telegram"],
    horizontal=True,
    index=0
)

# ---------- CONDITIONAL DASHBOARD RENDERING ----------
if dashboard == "YouTube":
    import streamlit_youtube
    streamlit_youtube.youtube_dashboard()

elif dashboard == "Reddit":
    import streamlit_reddit
    streamlit_reddit.reddit_dashboard()

elif dashboard == "Telegram":
    import streamlit_telegram
    streamlit_telegram.telegram_dashboard()
