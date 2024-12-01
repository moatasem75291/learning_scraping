import json
import os
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException,
    WebDriverException,
    StaleElementReferenceException,
)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

CWD = os.path.dirname(__file__)
LOG_FILE = os.path.join(CWD, "scraper.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class AmazonAudibleScraper:
    def __init__(self, url, headless=False):
        self.url = url
        self.headless = headless
        try:
            self.driver = self._init_driver()
            self.driver.get(url)
            logging.info(f"Accessed URL: {url}")
            self.container = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "adbl-impression-container")
                )
            )
            self.items = self.container.find_elements(
                By.XPATH, "//li[contains(@class, 'productListItem')]"
            )
            logging.info(f"Found {len(self.items)} items on the page.")
        except WebDriverException as e:
            logging.error(f"WebDriverException occurred: {e}")
            self.driver.quit()
            raise

    def _init_driver(self):
        options = Options()
        if self.headless:
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
        return webdriver.Chrome(options=options)

    def _extract_pagination_pages(self):
        try:
            pagination = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//ul[contains(@class, 'pagingElements')]")
                )
            )
            pages = pagination.find_elements(By.TAG_NAME, "li")
            logging.info(f"Found {len(pages)} pagination pages.")
            return pages
        except NoSuchElementException:
            logging.info("No pagination found.")
            return None

    def _extract_data(self):

        data = []
        for item in self.items:
            try:
                title = item.find_element(By.CLASS_NAME, "bc-size-medium").text
                author = item.find_element(By.CLASS_NAME, "authorLabel").text
                length = item.find_element(By.CLASS_NAME, "runtimeLabel").text
                price = item.find_element(By.CLASS_NAME, "adblBuyBoxPrice").text
                release_date = item.find_element(By.CLASS_NAME, "releaseDateLabel").text
                language = item.find_element(By.CLASS_NAME, "languageLabel").text

                data.append(
                    {
                        "title": title,
                        "author": author,
                        "price": price,
                        "length": length,
                        "release_date": release_date,
                        "language": language,
                    }
                )
                logging.info(f"Scraped data for item: {title}")
            except NoSuchElementException as e:
                logging.warning(f"Element not found: {e}")
        return data

    def get_data(self):
        data = []
        pages = self._extract_pagination_pages()
        if pages:
            for page in pages[1:-1]:
                try:
                    WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable(page)
                    ).click()
                    logging.info(f"Clicked on pagination page.")
                    data.extend(self._extract_data())
                except StaleElementReferenceException as e:
                    logging.error(f"StaleElementReferenceException: {e}")
                except Exception as e:
                    logging.error(f"Error clicking pagination page: {e}")
        else:
            data.extend(self._extract_data())
        return data

    def close(self):
        self.driver.quit()
        logging.info("Closed the web driver.")


if __name__ == "__main__":
    url = "https://www.audible.com/search"
    try:
        scraper = AmazonAudibleScraper(url, headless=False)
        data = scraper.get_data()
        with open(os.path.join(CWD, "data.json"), "w") as f:
            json.dump(data, f, indent=4)
        logging.info("Data successfully scraped and saved to data.json")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        scraper.close()
