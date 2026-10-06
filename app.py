import streamlit as st
from pipeline import run_pipeline

st.set_page_config(page_title="Content Creation Pipeline", page_icon="📝")
st.title("Multi-Agent Content Creation Pipeline")
st.write("Enter a topic. Six AI agents will research it, write and fact-check a draft, "
         "optimize it for SEO, describe visuals, and produce the final article.")

topic = st.text_input("Topic", placeholder="Enter any topic, e.g. Renewable energy")

if st.button("Generate content") and topic.strip():
    with st.spinner("Agents are working... this takes 3-5 minutes"):
        try:
            final = run_pipeline(topic.strip())
            st.success("Done!")
            st.markdown(final)
            st.download_button("Download as Markdown", final, file_name="article.md")
        except Exception as e:
            st.error(f"Something went wrong: {e}")