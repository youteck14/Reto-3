# -*- coding: utf-8 -*-
from src.functions.Functions import Functions as Selenium
import unittest
import time
import pytest

horaGlobal = time.strftime("%H%M%S")
class TestCase(unittest.TestCase):
    def setUp(self):
        Selenium.abrir_navegador(self)
        Selenium.get_json_file(self, "opencart")

    def test_003(self):
        Selenium.get_elements(self, "my_Account").click()
        Selenium.get_elements(self, "login").click()
        Selenium.get_elements(self, "email_AddressL").send_keys("sanson121416@gmail.com")
        Selenium.get_elements(self, "passwordL").send_keys("counter141412443623322324")
        Selenium.get_elements(self,"button_LoginL").click()

        Selenium.esperar(self, 10)


        Selenium.assert_text(self,"notmarchfor_Email_PasswordL","Warning: No match for E-Mail Address and/or Password.")

        title = "Test_003"
        Selenium.capturar_pantalla(self)

    def tearDown(self):
        Selenium.tearDown(self)


if __name__ == '__main__':
    unittest.main()