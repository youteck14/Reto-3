# Created by YOHAN at 30/08/2022
@selenium
Feature: Selenium Reto 3
  # Enter feature description here

  Scenario: TestCase Number 1
    Given Abrir la aplicacion
    And Cargo el DOM de la App: opencart
    When Hago click en my_Account
    And Hago click en login
    And En el campo email_AddressL escribo sanson121416@gmail.com
    And En el campo passwordL escribo hola como estas
    Then Cierro la app