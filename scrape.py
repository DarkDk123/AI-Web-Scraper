import logging
import os
from pprint import pp
from typing import Optional, Generator

from selenium.webdriver.firefox.service import Service
import selenium.webdriver as wb
from bs4 import BeautifulSoup

# For working with Bright data!
from selenium.webdriver import ChromeOptions, Remote
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection

# Build logger
logger: logging.Logger = logging.getLogger("scrape")
logging.basicConfig(level=logging.INFO)


def scrape_website(url: str) -> str:
    """
    Scrapes the HTML content of a website using Selenium and Firefox locally.

    Args:
        url (str): The URL of the website to scrape.

    Returns:
        str: The scraped HTML content of the website.
    """

    logger.info("Launching Firefox browser...")

    # Driver for the browser (Firefox in this case)
    # Download compatible geckodriver from https://github.com/mozilla/geckodriver/releases
    service = Service(executable_path="geckodriver")
    options = wb.FirefoxOptions()
    options.add_argument("--headless")
    driver = wb.Firefox(service=service, options=options)

    try:
        # Get the HTML content of the website
        driver.get(url)
        html: str = driver.page_source
        html = driver.page_source
        logger.info(f"Scraped HTML from {url}")

        return html

    finally:
        # Quit the driver after it's done
        driver.quit()  # may raise PermissionError


# I'm not using Bright Data's Captcha filling service yet!
# But anyone can use this function instead, if scraping with Captchas.
def scrape_website_captcha_support(
    url: str, SBR_WEBDRIVER: Optional[str] = None
) -> str:
    """
    Scrapes a website with Captcha fill support using Bright Data.

    Bright Data's Captcha filling service is used to solve any potential Captchas
    that may appear on the website. The service is configured via the
    `SBR_WEBDRIVER` parameter, which should contain the Bright Data Webdriver URL.
    If not provided, the value of the `SBR_WEBDRIVER` environment variable is used
    instead.

    Args:
        url (str): The URL of the website to scrape.
        SBR_WEBDRIVER (str | None): The Bright Data Webdriver URL. Defaults to the
            value of the `SBR_WEBDRIVER` environment variable if not provided.

    Returns:
        str: The scraped HTML content of the website.
    """
    # Connect to the Scraping Browser
    logger.info("Connecting to Scraping Browser...")
    sbr_connection = ChromiumRemoteConnection(
        SBR_WEBDRIVER or os.environ["SBR_WEBDRIVER"], "goog", "chrome"
    )
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        # Navigate to the website
        driver.get(url)
        # Wait for the Captcha to be solved
        logger.info("Waiting captcha to solve...")
        solve_res = driver.execute(
            "executeCdpCommand",
            {
                "cmd": "Captcha.waitForSolve",
                "params": {"detectTimeout": 10000},
            },
        )

        logger.critical("Captcha solve status:", solve_res["value"]["status"])
        logger.info("Navigated! Scraping page content...")

        html = driver.page_source
        return html


# The following 3 functions are used to retrieve only the essential text from the website!
def extract_body_content(html_content: str) -> str:
    """Get the page body HTML.

    Extracts the page body HTML from the given HTML content. If the page body
    exists, the function returns it as a string. Otherwise, an empty string is
    returned.

    Args:
        html_content (str): The HTML content of the page.

    Returns:
        str: The page body HTML as a string.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""


def clean_body_content(body_content: str) -> str:
    """
    Clean the page body content by removing `<script>` and `<style>` tags.

    Args:
        body_content (str): The page body content as a string.

    Returns:
        str: The cleaned page body content as a string.
    """
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    # Get text or further process the content
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content


def split_dom_content(dom_content, max_length=6000) -> Generator[str, None, None]:
    """
    Split the given DOM content into chunks of a given max_length.

    Useful for splitting large HTML pages into smaller chunks, for example for
    sending to a language model for processing.

    Args:
        dom_content (str): The HTML content of the page to split.
        max_length (int, optional): The maximum length of each chunk. Defaults to 6000.

    Yields:
        str: A chunk of the given HTML content, up to max_length characters long.
    """
    return (
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    )


# Template code!
if __name__ == "__main__":
    source = scrape_website("https://amazon.ca/")
    body = extract_body_content(source)
    clean_body = clean_body_content(body)

    pp(clean_body)
