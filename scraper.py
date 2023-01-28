import json
import os
from bs4 import BeautifulSoup

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

print(os.environ)


def parse_events(content: BeautifulSoup) -> str:
    """
    Parse WhoScore Content
    Return data string
    """
    search_keys = {"class": "max-content", "id": "layout-wrapper"}
    content = content.find("div", search_keys)
    content = content.find_all("script")
    return str(max([l for l in content], key=lambda x: len(str(x))))


def parse_fixtures(content: BeautifulSoup) -> list:
    """
    Parse Whoscore fixtures
    """
    fixtures = []
    search_key_id = {"id": "tournament-fixture"}
    search_key_fixtures = {
        "class": "col12-lg-1 col12-m-1 col12-s-0 col12-xs-0 result divtable-data"
    }
    data = content.find("div", search_key_id)
    data = data.find_all("div", search_key_fixtures)
    for item in data:
        fixture = item.find("a").get("href", None)
        if "Live" in fixture:
            fixtures.append(fixture)
        else:
            print("Fixture is up-todate")
            break
    return fixtures


def preprocess(input: str = "") -> dict:
    """
    Preprocess WhoScored Data
    returns dict of data
    """
    len_match_centre = 17
    len_trailing = -1
    data = max(input.split("\n"), key=len)
    data = data.lstrip()[len_match_centre:len_trailing]
    return json.loads(data)


def scrapper(target_url: str = None, mode: str = "events") -> None:
    """
    Scrap Function
    """

    chrome_service = Service(
        ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
    )
    chrome_options = Options()
    options = [
        "--headless",
        "--disable-gpu",
        "--window-size=1920,1200",
        "--ignore-certificate-errors",
        "--disable-extensions",
        "--no-sandbox",
        "--disable-dev-shm-usage",
    ]
    for option in options:
        chrome_options.add_argument(option)
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    driver.get(target_url)
    content = BeautifulSoup(driver.page_source, features="html.parser")

    data = preprocess(parse_events(content))
    file_name = "data.json"
    with open(file_name, "w") as f:
        json.dump(data, f, indent=4)
        print("file saved.")
    return None


if __name__ == "__main__":

    urls = [
        "https://www.whoscored.com/Matches/1640876/Live/England-Premier-League-2022-2023-Arsenal-Manchester-United"
    ]
    for url in urls:
        print(scrapper(target_url=url))
