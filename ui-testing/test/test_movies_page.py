import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from util.web_driver_utils import WebDriverUtils


class LandingPageTest(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        self.driver.maximize_window()
        self.base_url = "http://localhost:8080/"
        self.driver.get(self.base_url)
        self.wait = WebDriverWait(self.driver, 10)

    def test_query_search(self):
        wbu = WebDriverUtils(driver=self.driver)
        text1 = wbu.get_element_text(
            xpath='//*[@id="con"]/div/div[1]/div[2]/h1')
        wbu.fill(xpath='//*[@id="search-dropdown"]', value="joker")
        wbu.click_and_sleep(
            xpath='//*[@id="app"]/div/div[2]/form/div/div/button', seconds=2)
        text2 = wbu.get_element_text(
            xpath='//*[@id="con"]/div/div[1]/div[2]/h1')

        assert text1 != text2

    def test_genres_search(self):
        wbu = WebDriverUtils(driver=self.driver)
        text1 = wbu.get_element_text(
            xpath='//*[@id="con"]/div/div[1]/div[2]/h1')
        wbu.click_and_sleep(
            xpath='//*[@id="app"]/div/div[2]/div[3]/section[1]/div[1]/ol/li[10]/p', seconds=2)
        text2 = wbu.get_element_text(
            xpath='//*[@id="con"]/div/div[1]/div[2]/h1')

        assert text1 != text2

    def test_sort_desc_by_num_votes(self):
        wbu = WebDriverUtils(driver=self.driver)
        text1 = wbu.get_element_text(
            xpath='//*[@id="con"]/div/div[1]/div[2]/h1')
        wbu.click_and_sleep(
            xpath='//*[@id="app"]/div/div[2]/div[3]/section[2]/div[1]/ol/li[2]/p', seconds=4)
        text2 = wbu.get_element_text(
            xpath='//*[@id="con"]/div/div[1]/div[2]/h1')

        assert text1 != text2

    def test_sort_asc_by_num_votes(self):
        wbu = WebDriverUtils(driver=self.driver)
        text1 = wbu.get_element_text(
            xpath='//*[@id="con"]/div/div[1]/div[2]/h1')
        wbu.click_and_sleep(
            xpath='//*[@id="app"]/div/div[2]/div[3]/section[2]/div[1]/ol/li[2]/p', seconds=4)
        wbu.click_and_sleep(
            xpath='//*[@id="app"]/div/div[2]/div[3]/section[2]/div[1]/ol/li[2]/p', seconds=4)
        text2 = wbu.get_element_text(
            xpath='//*[@id="con"]/div/div[1]/div[2]/h1')

        assert text1 != text2

    def test_no_sort_by_num_votes(self):
        wbu = WebDriverUtils(driver=self.driver)
        text1 = wbu.get_element_text(
            xpath='//*[@id="con"]/div/div[1]/div[2]/h1')
        wbu.click_and_sleep(
            xpath='//*[@id="app"]/div/div[2]/div[3]/section[2]/div[1]/ol/li[2]/p', seconds=4)
        wbu.click_and_sleep(
            xpath='//*[@id="app"]/div/div[2]/div[3]/section[2]/div[1]/ol/li[2]/p', seconds=4)
        wbu.click_and_sleep(
            xpath='//*[@id="app"]/div/div[2]/div[3]/section[2]/div[1]/ol/li[2]/p', seconds=4)
        text2 = wbu.get_element_text(
            xpath='//*[@id="con"]/div/div[1]/div[2]/h1')

        assert text1 == text2

    def test_sort_desc_by_avg_rating(self):
        wbu = WebDriverUtils(driver=self.driver)
        text1 = wbu.get_element_text(
            xpath='//*[@id="con"]/div/div[1]/div[2]/h1')
        wbu.click_and_sleep(
            xpath='//*[@id="app"]/div/div[2]/div[3]/section[2]/div[1]/ol/li[1]/p', seconds=4)
        text2 = wbu.get_element_text(
            xpath='//*[@id="con"]/div/div[1]/div[2]/h1')

        assert text1 != text2

    def test_sort_asc_by_avg_rating(self):
        wbu = WebDriverUtils(driver=self.driver)
        text1 = wbu.get_element_text(
            xpath='//*[@id="con"]/div/div[1]/div[2]/h1')
        wbu.click_and_sleep(
            xpath='//*[@id="app"]/div/div[2]/div[3]/section[2]/div[1]/ol/li[1]/p', seconds=4)
        wbu.click_and_sleep(
            xpath='//*[@id="app"]/div/div[2]/div[3]/section[2]/div[1]/ol/li[1]/p', seconds=4)
        text2 = wbu.get_element_text(
            xpath='//*[@id="con"]/div/div[1]/div[2]/h1')

        assert text1 != text2

    def test_no_sort_by_avg_rating(self):
        wbu = WebDriverUtils(driver=self.driver)
        text1 = wbu.get_element_text(
            xpath='//*[@id="con"]/div/div[1]/div[2]/h1')
        wbu.click_and_sleep(
            xpath='//*[@id="app"]/div/div[2]/div[3]/section[2]/div[1]/ol/li[1]/p', seconds=4)
        wbu.click_and_sleep(
            xpath='//*[@id="app"]/div/div[2]/div[3]/section[2]/div[1]/ol/li[1]/p', seconds=4)
        wbu.click_and_sleep(
            xpath='//*[@id="app"]/div/div[2]/div[3]/section[2]/div[1]/ol/li[1]/p', seconds=4)
        text2 = wbu.get_element_text(
            xpath='//*[@id="con"]/div/div[1]/div[2]/h1')

        assert text1 == text2

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
