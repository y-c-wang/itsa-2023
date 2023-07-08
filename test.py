import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup


def get_options():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    return options


def check_loaded():
    try:
        driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=get_options())
        driver.get("http://localhost:8080")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.ID, "temperature-tr-0"))
        )
    except Exception:
        sys.exit("ERROR: failed to fetch the data from Open-Meteo")

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    try:
        tr_list = soup.find_all("tr")
        for tr in tr_list:
            th_list = tr.find_all("th")
            if len(th_list) == 3:
                continue

            td_list = tr.find_all("td")
            assert (len(td_list) == 3)

            for td in td_list:
                assert (td.text != "")
    except Exception:
        sys.exit("ERROR: fetch data in wrong format")

    driver.quit()


if __name__ == "__main__":
    check_loaded()
