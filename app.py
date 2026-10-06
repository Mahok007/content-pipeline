import re
import streamlit as st
from pipeline import run_pipeline
from tools.pdf_export import markdown_to_pdf

st.set_page_config(page_title="Content Creation Pipeline", page_icon="📝")
st.title("Multi-Agent Content Creation Pipeline")
st.write("Enter a topic. Six AI agents will research it, write and fact-check a draft, "
         "optimize it for SEO, generate images, and produce the final article.")

with st.form("topic_form"):
    topic = st.text_input("Topic", placeholder="Enter any topic, e.g. Renewable energy")
    submitted = st.form_submit_button("Generate content")

if submitted and topic.strip():
    with st.spinner("Agents are working... this takes 3-5 minutes"):
        try:
            final = run_pipeline(topic.strip())
            pdf_bytes = markdown_to_pdf(final)
            slug = re.sub(r"[^a-z0-9]+", "-", topic.lower()).strip("-")
            st.session_state["result"] = {"markdown": final, "pdf": pdf_bytes, "name": slug}
        except Exception as e:
            st.error(f"Something went wrong: {e}")

result = st.session_state.get("result")
if result:
    st.success("Done!")
    st.download_button("Download as PDF", result["pdf"],
                       file_name=f"{result['name']}.pdf", mime="application/pdf")
    st.markdown(result["markdown"])