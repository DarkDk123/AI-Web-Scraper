# AI Web Scraper 🤖

An **AI Web Scraper** using LangChain, HuggingFace, selenium etc.
## Usage

1. Install the required packages: `pip install -r requirements.txt`.
2. Set the environments variables as explained [below.](#environment-variables)
3. Run the Streamlit app: `streamlit run streamlit_main.py`.
4. Enter a URL and a description of what you want to parse from the website.
5. The app will scrape the website, extract the relevant text, and use the HuggingFace model to parse the text.


## Example: Scraping Github profiles

* URL: `https://github.com/techwithtim`
* query: `Provide info about the Github profile`

![demo](./example.gif)

## Environment Variables

The AI Web Scraper uses the following environment variables:

* `HUGGINGFACE_MODEL_ID`: The ID of the HuggingFace model to use for parsing the text.
* `UGGINGFACEHUB_API_TOKEN` : HuggingFace Hub API token.

* `SBR_WEBDRIVER` (Optional for captcha support): The URL of the Bright Data Webdriver to use for solving captchas.

## Development

The AI Web Scraper is built using the following technologies:

* `streamlit`: The web app framework.
* `langchain_huggingface`: The library for using HuggingFace models in langchain.
* `langchain`: Main langchain library.
* `selenium`: The library for interacting with the browser.
* `bs4`: The library for parsing HTML.
