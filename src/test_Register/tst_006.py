# -*- coding: utf-8 -*-
from src.functions.Functions import Functions as Selenium
import unittest
import time
import pytest

class TestCase(unittest.TestCase):
    def setUp(self):
        Selenium.abrir_navegador(self)
        Selenium.get_json_file(self, "opencart")

    def test_006(self):
        # MAIN
        Selenium.get_elements(self, "my_Account").click()
        Selenium.get_elements(self, "register").click()
        Selenium.get_elements(self, "first_NameR").send_keys("yohann")
        Selenium.get_elements(self, "last_NameR").send_keys("romeroo")
        Selenium.get_elements(self, "emailR").send_keys("yohanrr86@gmail.com")
        Selenium.get_elements(self, "telefonoR").send_keys("970747425")
        Selenium.get_elements(self, "passwordR").send_keys("HolaComoEstas")
        Selenium.get_elements(self, "password_ConfirmR").send_keys("HolaComoEstas")
        Selenium.get_elements(self, "checkbutton_AgreeR").click()
        Selenium.get_elements(self, "button_ContinueR").click()
        Selenium.esperar(self,5)
        title = "Test_006"
        Selenium.capturar_pantalla(self)

    def tearDown(self):
        Selenium.tearDown(self)


if __name__ == '__main__':
    unittest.main()