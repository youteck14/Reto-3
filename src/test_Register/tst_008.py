# -*- coding: utf-8 -*-
from src.functions.Functions import Functions as Selenium
import unittest
import time
import pytest
class TestCase(unittest.TestCase):
    def setUp(self):
        Selenium.abrir_navegador(self)
        Selenium.get_json_file(self, "opencart")
    def test_008(self):
        # MAIN
        Selenium.get_elements(self, "my_Account").click()
        Selenium.get_elements(self, "register").click()
        Selenium.get_elements(self, "first_NameR").send_keys("yohannsdjfksjadklñfsjadklfñjsakdlñfjkaslñjdksalñfjsdkalññjfksdlña")
        Selenium.get_elements(self, "button_ContinueR").click()
        Selenium.esperar(self,5)
        Selenium.assert_text(self, "firstname_HaveBetweenR", "First Name must be between 1 and 32 characters!")

        title = "Test_008"
        Selenium.capturar_pantalla(self)

    def tearDown(self):
        Selenium.tearDown(self)

if __name__ == '__main__':
    unittest.main()