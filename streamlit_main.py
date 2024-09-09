import re
import streamlit as st
from scrape import (
    scrape_website,
    extract_body_content,
    clean_body_content,
    split_dom_content,
)

# UI
st.title("AI Web Scraper 🤖")
st.subheader("An AI web scraper for your simple daily scraping needs!")

url = st.text_input("URL of the website you want to scrape")
button = st.button("Start scraping 🏌🏽")


if button:
    if not url or re.match(r"^(?:http|ftp)s?://([^/]+[.])*[^/]+/?.*$", url) is None:
        st.error("Please Enter a valid URL!")
    else:
        st.write("Scraping the website...")

        # Scrape the website
        html_page = scrape_website(url)
        html_body = extract_body_content(html_page)
        cleaned_content = clean_body_content(html_body)

        st.session_state["dom_content"] = cleaned_content

        with st.expander("View DOM Content 👁️"):
            st.text_area("DOM Content", cleaned_content, height=300)

