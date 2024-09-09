import logging
import os
from pprint import pp
from typing import Optional

from selenium.webdriver.firefox.service import Service
import selenium.webdriver as wb

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
    service = Service(executable_path=" geckodriver")
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


# Template code!
if __name__ == "__main__":
    source = scrape_website("https://amazon.ca/")
    pp(source)
