# -*- coding: utf-8 -*-
from behave import *
import pytest
import unittest
from behave import *
from selenium.webdriver.common.keys import Keys
from functions.Functions import Functions as Selenium
from functions.Inicializar import Inicializar
use_step_matcher("re")

class StepsDefinitions():

    @given("Abrir la aplicacion")
    def step_impl(self):
        Selenium.abrir_navegador(self)
        Selenium.page_has_loaded(self)


    @step("Cargo el DOM de la App: (.*)")
    def step_impl(self,DOM):
        Selenium.get_json_file(self,DOM)


    @then("Cierro la app")
    def step_impl(self):
        Selenium.tearDown(self)

    @when("Hago click en (.*)")
    def step_impl(self,locator):
        Selenium.get_elements(self,locator).click()

    @step("En el campo (.*) escribo (.*)")
    def step_impl(self,locator,text):
        Selenium.esperar_elemento(self, locator)
        #text = Selenium.ReplaceWithContextValue((self, text))
        Selenium.get_elements(self, locator).send_keys(text)


