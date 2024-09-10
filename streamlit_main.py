import re
import streamlit as st

from parse_LLM import parse_chunks_with_HF_LLM
from scrape import (
    clean_body_content,
    extract_body_content,
    scrape_website,
    split_dom_content,
)

# UI
st.title("AI Web Scraper 🤖")
st.subheader("An AI web scraper for your simple daily scraping needs!")

url = st.text_input("URL of the website you want to scrape")
button = st.button("Start scraping 👷🪓")

url_regex = re.match(r"^(?:http|ftp)s?://([^/]+[.])*[^/]+/?.*$", url)
if button and (not url or url_regex is None):
        st.error("Please Enter a valid URL!")

if button and url and url_regex:
    st.write("Scraping the website...")

    # Scrape the website
    html_page = scrape_website(url)
    html_body = extract_body_content(html_page)
    cleaned_content = clean_body_content(html_body)

    st.session_state["dom_content"] = cleaned_content

    with st.expander("View DOM Content 👁️"):
        st.text_area("DOM Content", cleaned_content, height=300)


if "dom_content" in st.session_state:
    parse_query = st.text_area("What do you want to parse?")

    if st.button("Parse ⚒️"):
        chunks = split_dom_content(st.session_state["dom_content"])
        st.write("Parsing the content...")

        # Parse the content with an LLM
        dom_chunks = split_dom_content(st.session_state.dom_content)
        parsed_result = parse_chunks_with_HF_LLM(dom_chunks, parse_query)
        st.write(parsed_result)
