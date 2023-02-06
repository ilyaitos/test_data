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

    def click_button_day(self, date):
        logger.info('Click day button')
        button_day = self.driver.find_element(By.XPATH, '(//div[@class="v-btn__content"][text() = "{}"])'.format(date))
        button_day.click()
        logger.info('day button is clicked')
        return button_day.get_attribute("textContent")

    def pick_date(self, days_delta):
        logger.info('date picker')
        year_and_month = self.driver.find_element(By.XPATH, '//div[@class="accent--text"]//button[@type="button"]').get_attribute("textContent")
        button_year = self.driver.find_element(By.XPATH, '//div[@class="v-picker__title__btn v-date-picker-title__year"]')
        date = datetime.datetime.today()
        target_date = date + datetime.timedelta(days=days_delta)
        if button_year.get_attribute("textContent") == target_date.strftime('%Y'):
            if year_and_month.strftime('%b') == target_date.strftime('%b'):
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
        return target_date.strftime('%Y-%m-%d')

    def selected_date(self):
        logger.info('search for selected date')
        selected_date = self.driver.find_element(By.XPATH, '//div[@class="col-sm-6 col-12"][span]').get_attribute("textContent")
        logger.info('date found')
        return selected_date[17:27]


page_data = Page(driver)


def test(login, exit_web):
    page_data.click_button_day(15)
    page_data.click_button_day(20)
    get_data = page_data.pick_date(3)
    assert get_data == page_data.selected_date()
