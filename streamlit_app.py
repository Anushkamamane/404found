import streamlit as st

st.title("Sentiment Dashboards for Tata Motors")

dashboard_choice = st.radio(
    "Choose sentiment dashboard:",
    ('YouTube', 'Reddit')
)

if dashboard_choice == 'YouTube':
    st.write("### YouTube Sentiment Dashboard")
    # You can import or directly include your previous YouTube dashboard code here
    import streamlit_youtube
    streamlit_youtube.youtube_dashboard()
elif dashboard_choice == 'Reddit':
    st.write("### Reddit Sentiment Dashboard")
    import streamlit_reddit
    streamlit_reddit.reddit_dashboard()
