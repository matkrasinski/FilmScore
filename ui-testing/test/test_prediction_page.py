import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from time import sleep
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

    def test_empty_form(self):
        wbu = WebDriverUtils(self.driver)
        wbu.click(xpath='//*[@id="app"]/div/div[1]/header/ul/li[3]/button')
        wbu.click(xpath='//*[@id="app"]/div/div[2]/form/div[12]/input')
        element = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable(
                (By.XPATH, '//*[@id="app"]/div/div[2]/form/div[13]/div[2]/div/div[2]/div/div[1]'))
        )

        assert element.is_displayed()

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
