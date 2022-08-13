import unittest
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import TimeoutException
horaGlobal = time.strftime("%H%M%S")

class TestCase(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()

        # INGRESO A LA APP DE REGISTRO
        self.driver.get("http://opencart.abstracta.us/index.php?route=common/home")

    def test_001(self):
        #MAIN
        self.my_Account = self.driver.find_element(by=By.XPATH, value="//a[@title='My Account']").click()
        self.login = self.driver.find_element(by=By.XPATH,value="//a[normalize-space()='Login']").click()
        self.email_Address = self.driver.find_element(by=By.XPATH,value="//input[@id='input-email']")
        self.email_Address.send_keys("sanson121416@gmail.com")
        self.password = self.driver.find_element(by=By.XPATH, value="//input[@id='input-password']")
        self.password.send_keys("paramimascota14")
        self.button_Login = self.driver.find_element(by=By.XPATH,value="//input[@value='Login']").click()
        time.sleep(5)

        title = "Test_001"
        self.driver.get_screenshot_as_file(f"../data/capturas/{title}-{horaGlobal}.png")

    def tearDown(self):
        self.driver.close()

if __name__ == '__main__':
    unittest.main()
