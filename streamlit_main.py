import streamlit as st


# UI
st.title("AI Web Scraper 🤖")
st.subheader("This is an example of an AI web scraper.")

url = st.text_input("Enter the URL of the website you want to scrape")

if st.button("Scrape"):
    st.write("Scraping...")

st.write("Thanks for using this app!")