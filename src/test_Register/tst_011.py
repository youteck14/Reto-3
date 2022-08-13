import unittest
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

horaGlobal = time.strftime("%H%M%S")

class TestCase(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()

        # INGRESO A LA APP DE REGISTRO
        self.driver.get("http://opencart.abstracta.us/index.php?route=common/home")

    def test_011(self):
        # MAIN
        self.my_Account = self.driver.find_element(by=By.XPATH, value="//a[@title='My Account']").click()
        self.register = self.driver.find_element(by=By.XPATH, value="//ul[@class='dropdown-menu dropdown-menu-right']//a[contains(text(),'Register')]").click()
        self.first_Name = self.driver.find_element(by=By.XPATH, value="//input[@id='input-firstname']")
        self.first_Name.send_keys("yohan")
        self.last_Name = self.driver.find_element(by=By.XPATH, value="//input[@id='input-lastname']")
        self.last_Name.send_keys("romeroo")
        self.email = self.driver.find_element(by=By.XPATH, value="//input[@id='input-email']")
        self.email.send_keys("yohanrr86@gmail.com")
        self.telefono = self.driver.find_element(by=By.XPATH, value="//input[@id='input-telephone']")
        self.telefono.send_keys("970747425")
        self.password = self.driver.find_element(by=By.XPATH, value="//input[@id='input-password']")
        self.password.send_keys("HolaComoEstas")
        self.confirmar = self.driver.find_element(by=By.XPATH, value="//input[@id='input-confirm']")
        self.confirmar.send_keys("HolaComoEstas")
        self.agree = self.driver.find_element(by=By.XPATH, value="//input[@name='agree']").click()

        self.continuar = self.driver.find_element(by=By.XPATH,value="//input[@value='Continue']").click()

        time.sleep(5)

        title = "Test_011"
        self.driver.get_screenshot_as_file(f"../data/capturas/{title}-{horaGlobal}.png")

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()