import datetime
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pytest
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
cons_handler = logging.StreamHandler()
cons_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
cons_handler.setFormatter(formatter)
logger.addHandler(cons_handler)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
link = 'https://cv.parleto.io/jobs/task/c819935b-5e51-4f5d-bbf2-456012696024/'
date = datetime.datetime.today()

@pytest.fixture(scope="module")
def login():
    driver.implicitly_wait(7)
    driver.maximize_window()
    driver.get(link)


@pytest.fixture(scope="module")
def exit_web():
    yield
    driver.quit()


class Page:

    def __init__(self, driver):
        self.driver = driver

    def pick_date(self, days_delta):  # this function is designed to select a date only 100 years forward and backward
        for x in days_delta:
            logger.info('date picker')
            year_and_month = self.driver.find_element(By.XPATH, '//div[@class="accent--text"]//button[@type="button"]').get_attribute("textContent")
            button_year = self.driver.find_element(By.XPATH, '//div[@class="v-picker__title__btn v-date-picker-title__year"]')
            target_date = date + datetime.timedelta(days=x)
            if button_year.get_attribute("textContent") == target_date.strftime('%Y'):
                if datetime.datetime.strptime(year_and_month, "%B %Y").strftime('%b') == target_date.strftime('%b'):
                    button_day = self.driver.find_element(By.XPATH, '(//div[@class="v-btn__content"][text() = "{}"])'.format( target_date.strftime('%#d')))
                    button_day.click()
                else:
                    year_and_month.click()
                    months = self.driver.find_element(By.XPATH, '//div[@class="v-btn__content"][text() = "{}"]'.format(target_date.strftime('%b')))
                    months.click()
                    button_day = self.driver.find_element(By.XPATH, '(//div[@class="v-btn__content"][text() = "{}"])'.format(target_date.strftime('%#d')))
                    button_day.click()
            else:
                button_year.click()
                button_years = self.driver.find_element(By.XPATH, '//li[@class][text()="{}"]'.format(target_date.strftime('%Y')))
                button_years.click()
                button_months = self.driver.find_element(By.XPATH, '//div[@class="v-btn__content"][text() = "{}"]'.format(target_date.strftime('%b')))
                button_months.click()
                button_day = self.driver.find_element(By.XPATH, '(//div[@class="v-btn__content"][text() = "{}"])'.format(target_date.strftime('%#d')))
                button_day.click()
            logger.info('date selected')

    def get_dates(self):
        logger.info('search for selected date')
        date_lookup = self.driver.find_element(By.XPATH, '//div[@class="col-sm-6 col-12"][span]').get_attribute("textContent")
        clearing_date = date_lookup.replace('Selected dates: ', '')
        clearing_date = clearing_date.replace(',', '')
        split_dates = clearing_date.split()
        lists = []
        for x in split_dates:
            dates = datetime.datetime.strptime(x, "%Y-%m-%d")
            lists.append((dates - date).days + 1)
        logger.info('date found')
        return lists

    def scroll(self, text):
        get_text = self.driver.find_element(By.LINK_TEXT, text)
        driver.execute_script("arguments[0].focus();", get_text)

    # option #2
    # def scroll(self, text):
    #     target = self.driver.find_element(By.LINK_TEXT, text)
    #     actions = ActionChains(driver)
    #     actions.move_to_element(target)
    #     actions.perform()


page_data = Page(driver)


def test(login, exit_web):
    page_data.scroll('Test task')
    get = page_data.get_dates()
    page_data.pick_date(get)
    page_data.pick_date([3])
    pytest.assume(get not in page_data.get_dates())
    pytest.assume(3 in page_data.get_dates())
