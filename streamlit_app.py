import streamlit as st

# Define language text dictionary
TEXTS = {
    "en": {
        "page_title": "Tata Motors Sentiment Dashboard",
        "header_title": "Tata Motors Social Sentiment Dashboard",
        "header_subtitle": "Real-time Sentiment Analysis across multiple platforms",
        "select_platform": "📊 Select a Platform",
        "youtube": "YouTube",
        "youtube_desc": "Video & comment sentiment analysis",
        "reddit": "Reddit",
        "reddit_desc": "Community discussions analytics",
        "telegram": "Telegram",
        "telegram_desc": "Group message sentiment & topics",
        "choose_dashboard": "📌 Choose sentiment dashboard:"
    },
    "hi": {
        "page_title": "टाटा मोटर्स सेंटिमेंट डैशबोर्ड",
        "header_title": "टाटा मोटर्स सोशल सेंटिमेंट डैशबोर्ड",
        "header_subtitle": "कई प्लेटफार्मों पर रीयल-टाइम सेंटिमेंट विश्लेषण",
        "select_platform": "📊 एक प्लेटफ़ॉर्म चुनें",
        "youtube": "यूट्यूब",
        "youtube_desc": "वीडियो और टिप्पणी भावना विश्लेषण",
        "reddit": "रेडिट",
        "reddit_desc": "समुदाय चर्चा विश्लेषण",
        "telegram": "टेलीग्राम",
        "telegram_desc": "ग्रुप संदेश भावना और विषय",
        "choose_dashboard": "📌 सेंटिमेंट डैशबोर्ड चुनें:"
    }
}

# Language selector
lang = st.selectbox("Language / भाषा", ["English", "Hindi"])
lang_code = "hi" if lang == "Hindi" else "en"



# Page config with selected language title
st.set_page_config(page_title=TEXTS[lang_code]["page_title"], layout="wide")

# Custom background CSS
page_bg = """
<style>
    .stApp {
        background-color: #e6f0fa; /* light blue shade */
    }
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# Header section
col_logo, col_header = st.columns([1, 8])
with col_logo:
    st.image("notebooks/data/tataimg.png", width=120)

with col_header:
    st.markdown(
        f"""
        <h1 style='text-align: left; color: #1769aa; margin-bottom:0px;'>
            {TEXTS[lang_code]["header_title"]}
        </h1>
        <p style='text-align: left; color: #222; font-size:16px; margin-top:0px;'>
            {TEXTS[lang_code]["header_subtitle"]}
        </p>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# Platform selection row
st.markdown(f"### {TEXTS[lang_code]['select_platform']}")

col1, col2, col3 = st.columns(3)

with col1:
    img_col, txt_col = st.columns([1, 3])
    with img_col:
        st.image("notebooks/data/yt.png", width=70)
    with txt_col:
        st.markdown(
            f"""
            <div style='display:flex;align-items:center;height:70px;'>
                <div>
                    <span style='font-size:20px;font-weight:600;text-align:left;margin-left:8px;'>{TEXTS[lang_code]['youtube']}</span><br>
                    <span style='font-size:15px;color:#666;'>{TEXTS[lang_code]['youtube_desc']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True
        )

with col2:
    img_col, txt_col = st.columns([1, 3])
    with img_col:
        st.image("notebooks/data/reddit.png", width=70)
    with txt_col:
        st.markdown(
            f"""
            <div style='display:flex;align-items:center;height:70px;'>
                <div>
                    <span style='font-size:20px;font-weight:600;text-align:left;margin-left:8px;'>{TEXTS[lang_code]['reddit']}</span><br>
                    <span style='font-size:15px;color:#666;'>{TEXTS[lang_code]['reddit_desc']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True
        )

with col3:
    img_col, txt_col = st.columns([1, 3])
    with img_col:
        st.image("notebooks/data/tele.png", width=70)
    with txt_col:
        st.markdown(
            f"""
            <div style='display:flex;align-items:center;height:70px;'>
                <div>
                    <span style='font-size:20px;font-weight:600;text-align:left;margin-left:8px;'>{TEXTS[lang_code]['telegram']}</span><br>
                    <span style='font-size:15px;color:#666;'>{TEXTS[lang_code]['telegram_desc']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True
        )

st.markdown("<br>", unsafe_allow_html=True)

# Dashboard toggle
dashboard = st.radio(
    f"{TEXTS[lang_code]['choose_dashboard']}",
    ["YouTube", "Reddit", "Telegram"],
    horizontal=True,
    index=0
)

# Conditional dashboard rendering
if dashboard == "YouTube":
    import streamlit_youtube
    streamlit_youtube.youtube_dashboard(lang=lang_code)

elif dashboard == "Reddit":
    import streamlit_reddit
    streamlit_reddit.reddit_dashboard(lang=lang_code)

elif dashboard == "Telegram":
    import streamlit_telegram
    streamlit_telegram.telegram_dashboard(lang=lang_code)
