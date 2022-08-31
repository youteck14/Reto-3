# -*- coding: utf-8 -*-
from src.functions.Functions import Functions as Selenium
import unittest
import time
import pytest

class TestCase(unittest.TestCase):
    def setUp(self):
        Selenium.abrir_navegador(self)
        Selenium.get_json_file(self, "opencart")

    def test_004(self):
        # MAIN
        Selenium.get_elements(self, "my_Account").click()
        Selenium.get_elements(self, "login").click()

        Selenium.validar_elemento(self, "forgotten_PasswordL")
        Selenium.esperar(5)

        title = "Test_004"
        Selenium.capturar_pantalla(self)
    def tearDown(self):
        Selenium.tearDown(self)


if __name__ == '__main__':
    unittest.main()