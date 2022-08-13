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

    def test_010(self):
        # MAIN
        self.my_Account = self.driver.find_element(by=By.XPATH, value="//a[@title='My Account']").click()
        self.register = self.driver.find_element(by=By.XPATH, value="//ul[@class='dropdown-menu dropdown-menu-right']//a[contains(text(),'Register')]").click()
        self.first_Name = self.driver.find_element(by=By.XPATH, value="//input[@id='input-firstname']")
        self.first_Name.send_keys("yohannnn")
        self.last_Name = self.driver.find_element(by=By.XPATH, value="//input[@id='input-lastname']")
        self.last_Name.send_keys("romeroooo")
        self.email = self.driver.find_element(by=By.XPATH, value="//input[@id='input-email']")
        self.email.send_keys("ed.yohanr@hotmail.com")
        self.telefono = self.driver.find_element(by=By.XPATH, value="//input[@id='input-telephone']")
        self.telefono.send_keys("970747427")
        self.password = self.driver.find_element(by=By.XPATH, value="//input[@id='input-password']")
        self.password.send_keys("holacomoestas")
        self.confirmar = self.driver.find_element(by=By.XPATH, value="//input[@id='input-confirm']")
        self.confirmar.send_keys("ola")
        time.sleep(5)
        self.agree = self.driver.find_element(by=By.XPATH, value="//input[@name='agree']").click()
        time.sleep(5)
        self.continuar = self.driver.find_element(by=By.XPATH,value="//input[@value='Continue']").click()



        self.RESULTADO = self.driver.find_element(by=By.XPATH, value="//div[@class='text-danger']").text
        time.sleep(5)

        assert self.RESULTADO == "Password confirmation does not match password!", "El resultado es diferente al esperado"

        title = "Test_010"
        self.driver.get_screenshot_as_file(f"../data/capturas/{title}-{horaGlobal}.png")

    def tearDown(self):
        self.driver.close()



if __name__ == '__main__':
    unittest.main()