# -*- coding: utf-8 -*-
from src.functions.Functions import Functions as Selenium
import unittest
import time
import pytest
class TestCase(unittest.TestCase):
    def setUp(self):
        Selenium.abrir_navegador(self)
        Selenium.get_json_file(self, "opencart")

    def test_009(self):
        # MAIN
        Selenium.get_elements(self, "my_Account").click()
        Selenium.get_elements(self, "register").click()
        Selenium.get_elements(self, "first_NameR").send_keys("yohann")
        Selenium.get_elements(self, "last_NameR").send_keys("romeroo")
        Selenium.get_elements(self, "emailR").send_keys("saulo@gmail.com")
        Selenium.get_elements(self, "telefonoR").send_keys("970747425")
        Selenium.get_elements(self, "passwordR").send_keys("hol")
        Selenium.get_elements(self, "button_ContinueR").click()

        Selenium.esperar(self, 5)
        Selenium.assert_text(self, "pass_HaveBetweenR", "Password must be between 4 and 20 characters!")

        title = "Test_009"
        Selenium.capturar_pantalla(self)



    def tearDown(self):
        Selenium.tearDown(self)



if __name__ == '__main__':
    unittest.main()