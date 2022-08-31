# -*- coding: utf-8 -*-
from src.functions.Functions import Functions as Selenium
import unittest
import time
import pytest
class TestCase(unittest.TestCase):
    def setUp(self):
        Selenium.abrir_navegador(self)
        Selenium.get_json_file(self, "opencart")

    def test_002(self):
        # MAIN
        Selenium.get_elements(self,"my_Account").click()
        Selenium.get_elements(self,"login").click()
        Selenium.get_elements(self,"button_LoginL").click()
        Selenium.esperar(self,10)
        Selenium.assert_text(self,"notmarchfor_Email_PasswordL","Warning: No match for E-Mail Address and/or Password.")

        title = "Test_002"
        Selenium.capturar_pantalla(self)
    def tearDown(self):
        Selenium.tearDown(self)

if __name__ == '__main__':
    unittest.main()